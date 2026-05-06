"""Workflow-oriented ASR commands.

This command group sits above the low-level ``file-stores`` and
``transcription`` resource commands and gives users an ASR-centric CLI:

- discover ASR models + their routing/capabilities
- upload raw ASR inputs
- prepare raw file stores into dataset-shaped inputs
- submit transcription jobs with flag-based UX (no JSON body file)
- inspect jobs and outputs

The underlying API contracts stay unchanged; this module is a thin,
user-friendly orchestrator over existing endpoints.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

import typer
from rich.console import Console
from rich.table import Table
from trelis_sdk.api.api_v1 import (
    cancel_transcription_job_api_v1_transcription_jobs_job_id_cancel_post as cancel_transcription_job_op,
    get_data_prep_job_api_v1_data_prep_jobs_job_id_get as get_data_prep_job_op,
    get_file_store_api_v1_file_stores_store_id_get as get_file_store_op,
    get_me_api_v1_me_get,
    get_transcription_job_api_v1_transcription_jobs_job_id_get as get_transcription_job_op,
    list_models_api_v1_models_get,
    list_transcription_jobs_api_v1_transcription_jobs_get as list_transcription_jobs_op,
)
from trelis_sdk.types import UNSET

from ..api_helpers import call_json
from ..auth import make_client
from ..errors import APIError, AuthError, UsageError, handle_cli_errors
from ..jobs import poll_until_terminal
from ..output import emit, is_json_mode
from . import file_stores as file_stores_cmd

app = typer.Typer(name="asr", help="Workflow-oriented ASR commands.")
models_app = typer.Typer(name="models", help="Discover ASR models and routing capabilities.")
upload_app = typer.Typer(name="upload", help="Upload ASR inputs as file stores.")
prepare_app = typer.Typer(name="prepare", help="Prepare raw ASR inputs into dataset-shaped stores.")
transcribe_app = typer.Typer(name="transcribe", help="Submit ASR transcription jobs.")
jobs_app = typer.Typer(name="jobs", help="Inspect ASR transcription jobs.")
output_app = typer.Typer(name="output", help="Inspect/export ASR outputs.")
_console = Console()

_ROUTER_BATCH_PREFIXES = (
    "assemblyai/",
    "deepgram/",
    "elevenlabs/",
    "fireworks/",
    "google/",
    "mistral/",
    "sarvam/",
    "speechmatics/",
    "together/",
)
_NON_ROUTER_HF_MODELS = frozenset({"google/medasr"})
_S3_KEY_LOG_RE = re.compile(r"s3_key=([^\s)]+)")
_S3_URL_LOG_RE = re.compile(r"s3://[^\s)]+")


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------


def _extract_api_error_message(raw_body: bytes) -> str | None:
    if not raw_body:
        return None
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        return raw_body.decode("utf-8", errors="replace").strip() or None

    if not isinstance(payload, dict):
        try:
            return json.dumps(payload)
        except (TypeError, ValueError):
            return str(payload)

    detail = payload.get("detail")
    if isinstance(detail, dict):
        message = detail.get("message")
        code = detail.get("code")
        if isinstance(message, str) and isinstance(code, str):
            return f"{code}: {message}"
        if isinstance(message, str):
            return message
        if isinstance(code, str):
            return code
    if isinstance(detail, str):
        return detail

    for key in ("message", "error"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, (dict, list)):
            try:
                return json.dumps(value)
            except (TypeError, ValueError):
                return str(value)
    return None


def _request_json(client, method: str, path: str, *, json_body: Any | None = None) -> Any:
    resp = client.get_httpx_client().request(method, path, json=json_body)
    status = int(resp.status_code)
    body = resp.content
    if 200 <= status < 300:
        if not body:
            return None
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return body.decode("utf-8", errors="replace")
    msg = _extract_api_error_message(body) or f"API returned {status}"
    if status in (401, 403):
        raise AuthError(msg)
    raise APIError(msg, status_code=status)


def _warn(message: str) -> None:
    if is_json_mode():
        return
    sys.stderr.write(f"warning: {message}\n")


def _normalize_models_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        models = payload.get("models")
        if isinstance(models, list):
            return [m for m in models if isinstance(m, dict)]
    if isinstance(payload, list):
        return [m for m in payload if isinstance(m, dict)]
    raise APIError("Unexpected response from models endpoint")


def _infer_engine(model_id: str, *, known_router_model: bool | None = None) -> str:
    if known_router_model is True:
        return "router"
    lower = model_id.lower()
    if lower in _NON_ROUTER_HF_MODELS:
        return "internal"
    if any(lower.startswith(prefix) for prefix in _ROUTER_BATCH_PREFIXES):
        return "router"
    return "internal"


def _augment_asr_model_info(item: dict[str, Any]) -> dict[str, Any]:
    router_model = bool(item.get("router_model"))
    engine = _infer_engine(str(item.get("model_id", "")), known_router_model=router_model)
    enriched = dict(item)
    enriched.update(
        {
            "engine": engine,
            "supports_timestamps": engine != "router",
            "supports_filter_threshold": engine != "router",
            "supports_entities_column": engine != "router",
            "requires_router_key": engine == "router",
        }
    )
    return enriched


def _get_asr_models(client) -> list[dict[str, Any]]:
    payload = call_json(list_models_api_v1_models_get, client=client, modality="asr")
    return [_augment_asr_model_info(m) for m in _normalize_models_payload(payload)]


def _resolve_asr_model(model_id: str, client) -> dict[str, Any]:
    models = _get_asr_models(client)
    for item in models:
        if item.get("model_id") == model_id:
            return item
    return {
        "model_id": model_id,
        "known_model": False,
        "engine": _infer_engine(model_id),
        "supports_timestamps": _infer_engine(model_id) != "router",
        "supports_filter_threshold": _infer_engine(model_id) != "router",
        "supports_entities_column": _infer_engine(model_id) != "router",
        "requires_router_key": _infer_engine(model_id) == "router",
    }


def _render_model_table(payload: dict[str, Any] | list[dict[str, Any]]) -> None:
    items = payload.get("models", []) if isinstance(payload, dict) else payload
    if not items:
        _console.print("[yellow]No ASR models.[/yellow]")
        return
    table = Table(show_header=True, header_style="bold")
    for col in ("model_id", "family", "engine", "router_model", "trainable", "inference_only", "size"):
        table.add_column(col)
    for item in items:
        table.add_row(
            str(item.get("model_id", "")),
            str(item.get("family", "")),
            str(item.get("engine", "")),
            str(item.get("router_model", False)),
            str(item.get("trainable", "")),
            str(item.get("inference_only", "")),
            str(item.get("size", "")),
        )
    _console.print(table)


def _render_job_updates(result: dict[str, Any]) -> None:
    if is_json_mode():
        return
    status = result.get("status") or result.get("state") or "unknown"
    _console.print(f"[cyan]status:[/cyan] {status}")


def _preflight_router_requirements(
    *,
    client,
    model: dict[str, Any],
    enable_timestamps: bool,
    filter_threshold: float | None,
    entities_column: str | None,
) -> None:
    if model.get("engine") != "router":
        return
    if enable_timestamps:
        raise UsageError(
            "Router ASR does not support timestamps in this build. "
            "Use an internal ASR model if you need timestamp output."
        )
    if filter_threshold is not None:
        raise UsageError(
            "Router ASR does not support filter_threshold in this build. "
            "Transcribe first, then re-filter in a second step."
        )
    if entities_column is not None:
        raise UsageError(
            "Router ASR does not support entities_column in this build. "
            "Use an internal ASR model for entity-CER flows."
        )

    whoami = call_json(get_me_api_v1_me_get, client=client)
    if isinstance(whoami, dict) and not bool(whoami.get("router_key_present")):
        raise UsageError(
            "The selected model routes through Trelis Router, but the active project has no router key configured."
        )


def _preflight_filestore_source(*, client, file_store_id: str) -> dict[str, Any] | None:
    try:
        store = call_json(get_file_store_op, client=client, store_id=file_store_id)
    except APIError:
        return None
    if not isinstance(store, dict):
        return None

    source = str(store.get("source") or "")
    if source == "upload":
        raise UsageError(
            f"FileStore {file_store_id} is a raw upload store (flat audio/text files). "
            "Run `trelis asr prepare file-store <id>` first."
        )
    if source == "parquet_upload":
        _warn(
            f"FileStore {file_store_id} is a parquet-upload store. Some parquet uploads lack manifest metadata "
            "and may fail contract validation on transcription submit."
        )
    return store


def _extract_output_store_id(job_payload: dict[str, Any], *, role: str = "primary") -> str | None:
    result = job_payload.get("result") if isinstance(job_payload, dict) else None
    if not isinstance(result, dict):
        return None
    output_stores = result.get("output_file_stores")
    if isinstance(output_stores, dict):
        value = output_stores.get(role)
        if isinstance(value, str):
            return value
    value = result.get("output_file_store_id")
    return value if isinstance(value, str) else None


def _extract_s3_locations(job_payload: dict[str, Any]) -> list[str]:
    logs = job_payload.get("logs") if isinstance(job_payload, dict) else None
    if not isinstance(logs, str) or not logs:
        return []
    matches = set(_S3_KEY_LOG_RE.findall(logs))
    matches.update(_S3_URL_LOG_RE.findall(logs))
    return sorted(matches)


def _transcription_payload(
    *,
    model_id: str,
    language: str,
    dataset_id: str | None,
    dataset_split: str,
    dataset_config: str | None,
    file_store_id: str | None,
    parquet_urls: list[str],
    num_samples: int | None,
    max_duration: float,
    enable_timestamps: bool,
    reference_column: str | None,
    entities_column: str | None,
    normalizer: str,
    filter_threshold: float | None,
    output_target: str,
    output_dataset_name: str | None,
    router_max_concurrency: int,
    router_provider_options: dict[str, str] | None = None,
) -> dict[str, Any]:
    sources = [bool(dataset_id), bool(file_store_id), bool(parquet_urls)]
    if sum(1 for s in sources if s) != 1:
        raise UsageError("Provide exactly one of --dataset-id, --file-store-id, or --parquet-url.")

    payload: dict[str, Any] = {
        "model_id": model_id,
        "language": language,
        "dataset_split": dataset_split,
        "max_duration": max_duration,
        "enable_timestamps": enable_timestamps,
        "normalizer": normalizer,
        "output_target": output_target,
        "router_max_concurrency": router_max_concurrency,
    }
    if dataset_id:
        payload["dataset_id"] = dataset_id
    if dataset_config:
        payload["dataset_config"] = dataset_config
    if file_store_id:
        payload["file_store_id"] = file_store_id
    if parquet_urls:
        payload["parquet_urls"] = parquet_urls
    if num_samples is not None:
        payload["num_samples"] = num_samples
    if reference_column is not None:
        payload["reference_column"] = reference_column
    if entities_column is not None:
        payload["entities_column"] = entities_column
    if filter_threshold is not None:
        payload["filter_threshold"] = filter_threshold
    if output_dataset_name is not None:
        payload["output_dataset_name"] = output_dataset_name
    if router_provider_options:
        payload["router_provider_options"] = router_provider_options
    return payload


def _submit_transcription_request(
    *,
    client,
    payload: dict[str, Any],
    resolved_engine: str,
    wait: bool,
    timeout: float,
    poll_interval: float,
) -> None:
    result = _request_json(client, "POST", "/api/v1/transcription", json_body=payload)
    if isinstance(result, dict):
        result = {**result, "resolved_engine": resolved_engine}
    if not wait:
        emit(result)
        return

    job_id = (result or {}).get("job_id") if isinstance(result, dict) else None
    if not isinstance(job_id, str):
        emit(result)
        return

    final = poll_until_terminal(
        lambda: call_json(get_transcription_job_op, client=client, job_id=job_id),
        timeout=timeout,
        interval=poll_interval,
        on_update=_render_job_updates,
    )
    emit({"submit": result, "final": final})


# ---------------------------------------------------------------------------
# asr models
# ---------------------------------------------------------------------------


@models_app.command("list")
@handle_cli_errors
def list_models(
    engine: str = typer.Option("all", help="Filter by engine: all, internal, or router."),
    trainable: bool | None = typer.Option(None, help="Filter by trainable models."),
    family: str | None = typer.Option(None, help="Filter by family."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    client = make_client(api_key)
    items = _get_asr_models(client)
    engine_norm = engine.strip().lower()
    if engine_norm not in {"all", "internal", "router"}:
        raise UsageError("--engine must be one of: all, internal, router")
    if engine_norm != "all":
        items = [m for m in items if m.get("engine") == engine_norm]
    if trainable is not None:
        items = [m for m in items if bool(m.get("trainable")) == trainable]
    if family:
        items = [m for m in items if str(m.get("family", "")).lower() == family.lower()]
    emit({"models": items, "total": len(items)}, human_renderer=_render_model_table)


@models_app.command("show")
@handle_cli_errors
def show_model(
    model_id: str = typer.Argument(..., help="ASR model id."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    client = make_client(api_key)
    emit(_resolve_asr_model(model_id, client))


# ---------------------------------------------------------------------------
# asr prepare
# ---------------------------------------------------------------------------


@prepare_app.command("file-store")
@handle_cli_errors
def prepare_file_store(
    store_id: str = typer.Argument(..., help="Raw upload FileStore id."),
    name: str | None = typer.Option(None, "--name", help="Output dataset/file-store name."),
    output_target: str | None = typer.Option(
        "s3", help="Output target: s3, hf, or s3+hf."
    ),
    split_option: str = typer.Option(
        "train_only",
        help="Split strategy: create_validation, train_only, validation_only, or test_only.",
    ),
    language: str = typer.Option("english", help="Language hint for data prep."),
    wait: bool = typer.Option(False, "--wait", help="Block until the preparation job completes."),
    timeout: float = typer.Option(1800.0, help="Max seconds to wait when --wait is set."),
    poll_interval: float = typer.Option(5.0, help="Seconds between status polls."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    client = make_client(api_key)
    output_name = name or f"prepared-{store_id[:8]}"
    body = {
        "output_dataset_name": output_name,
        "split_option": split_option,
        "language": language,
    }
    if output_target is not None:
        body["output_target"] = output_target

    result = _request_json(client, "POST", f"/api/v1/file-stores/{store_id}/process", json_body=body)
    if not wait:
        emit(result)
        return

    job_id = (result or {}).get("job_id") if isinstance(result, dict) else None
    if not isinstance(job_id, str):
        emit(result)
        return
    final = poll_until_terminal(
        lambda: call_json(get_data_prep_job_op, client=client, job_id=job_id),
        timeout=timeout,
        interval=poll_interval,
        on_update=_render_job_updates,
    )
    summary = {
        "submit": result,
        "final": final,
        "prepared_file_store_id": _extract_output_store_id(final),
        "dataset_id": ((final.get("result") or {}).get("dataset_id") if isinstance(final, dict) else None),
    }
    emit(summary)


# ---------------------------------------------------------------------------
# asr transcribe
# ---------------------------------------------------------------------------


@transcribe_app.command("submit")
@handle_cli_errors
def transcribe_submit(
    model_id: str = typer.Option(..., "--model", help="ASR model id."),
    language: str = typer.Option(..., "--language", help="Language code or language name."),
    dataset_id: str | None = typer.Option(None, "--dataset-id", help="HF dataset id."),
    dataset_split: str = typer.Option("test", "--split", help="Dataset split."),
    dataset_config: str | None = typer.Option(None, "--config", help="HF dataset config/subset."),
    file_store_id: str | None = typer.Option(None, "--file-store-id", help="FileStore id."),
    parquet_urls: list[str] = typer.Option(None, "--parquet-url", help="Repeatable parquet URL input."),
    num_samples: int | None = typer.Option(None, help="Optional sample limit."),
    max_duration: float = typer.Option(30.0, help="Maximum audio duration per item (seconds)."),
    enable_timestamps: bool = typer.Option(False, "--timestamps/--no-timestamps", help="Request timestamps."),
    reference_column: str | None = typer.Option(None, help="Reference column for CER/WER."),
    entities_column: str | None = typer.Option(None, help="Entities column for entity-CER."),
    normalizer: str = typer.Option("auto", help="Text normalizer."),
    filter_threshold: float | None = typer.Option(None, help="Optional CER filter threshold."),
    output_target: str = typer.Option("s3", help="Output target: s3, hf, or s3+hf."),
    output_dataset_name: str | None = typer.Option(None, help="Optional output dataset/FileStore name."),
    router_max_concurrency: int = typer.Option(16, help="Router concurrency when a Router model is selected."),
    sarvam_mode: str | None = typer.Option(
        None,
        "--sarvam-mode",
        help="Sarvam Saaras v3 mode: transcribe, translate, verbatim, translit, or codemix.",
    ),
    sarvam_input_audio_codec: str | None = typer.Option(
        None,
        "--sarvam-input-audio-codec",
        help="Optional Sarvam input_audio_codec. Studio sends WAV chunks; omit this unless instructed.",
    ),
    wait: bool = typer.Option(False, "--wait", help="Block until the transcription job completes."),
    timeout: float = typer.Option(1800.0, help="Max seconds to wait when --wait is set."),
    poll_interval: float = typer.Option(5.0, help="Seconds between status polls."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    client = make_client(api_key)
    model = _resolve_asr_model(model_id, client)
    _preflight_router_requirements(
        client=client,
        model=model,
        enable_timestamps=enable_timestamps,
        filter_threshold=filter_threshold,
        entities_column=entities_column,
    )
    if file_store_id:
        _preflight_filestore_source(client=client, file_store_id=file_store_id)

    router_provider_options: dict[str, str] = {}
    if sarvam_mode:
        router_provider_options["mode"] = sarvam_mode
    if sarvam_input_audio_codec:
        router_provider_options["input_audio_codec"] = sarvam_input_audio_codec
    if router_provider_options and model_id != "sarvam/saaras-v3":
        raise UsageError("--sarvam-mode/--sarvam-input-audio-codec require --model sarvam/saaras-v3")

    payload = _transcription_payload(
        model_id=model_id,
        language=language,
        dataset_id=dataset_id,
        dataset_split=dataset_split,
        dataset_config=dataset_config,
        file_store_id=file_store_id,
        parquet_urls=parquet_urls or [],
        num_samples=num_samples,
        max_duration=max_duration,
        enable_timestamps=enable_timestamps,
        reference_column=reference_column,
        entities_column=entities_column,
        normalizer=normalizer,
        filter_threshold=filter_threshold,
        output_target=output_target,
        output_dataset_name=output_dataset_name,
        router_max_concurrency=router_max_concurrency,
        router_provider_options=router_provider_options or None,
    )
    _submit_transcription_request(
        client=client,
        payload=payload,
        resolved_engine=str(model.get("engine") or "internal"),
        wait=wait,
        timeout=timeout,
        poll_interval=poll_interval,
    )


# ---------------------------------------------------------------------------
# asr jobs
# ---------------------------------------------------------------------------


@jobs_app.command("list")
@handle_cli_errors
def list_jobs(
    limit: int = typer.Option(20, help="Max jobs to return."),
    status: str | None = typer.Option(None, help="Optional status filter."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    client = make_client(api_key)
    result = call_json(
        list_transcription_jobs_op,
        client=client,
        limit=limit,
        status=status if status is not None else UNSET,
    )
    emit(result)


@jobs_app.command("get")
@handle_cli_errors
def get_job(
    job_id: str = typer.Argument(..., help="Transcription job id."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    client = make_client(api_key)
    emit(call_json(get_transcription_job_op, client=client, job_id=job_id))


@jobs_app.command("watch")
@handle_cli_errors
def watch_job(
    job_id: str = typer.Argument(..., help="Transcription job id."),
    timeout: float = typer.Option(1800.0, help="Max seconds to wait."),
    poll_interval: float = typer.Option(5.0, help="Seconds between polls."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    client = make_client(api_key)
    final = poll_until_terminal(
        lambda: call_json(get_transcription_job_op, client=client, job_id=job_id),
        timeout=timeout,
        interval=poll_interval,
        on_update=_render_job_updates,
    )
    emit(final)


@jobs_app.command("cancel")
@handle_cli_errors
def cancel_job(
    job_id: str = typer.Argument(..., help="Transcription job id."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    client = make_client(api_key)
    emit(call_json(cancel_transcription_job_op, client=client, job_id=job_id))


# ---------------------------------------------------------------------------
# asr output
# ---------------------------------------------------------------------------


@output_app.command("show")
@handle_cli_errors
def show_output(
    job_id: str = typer.Argument(..., help="Completed transcription job id."),
    role: str = typer.Option("primary", help="Output role to inspect (primary/kept/dropped/unscored)."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    client = make_client(api_key)
    job = call_json(get_transcription_job_op, client=client, job_id=job_id)
    if not isinstance(job, dict):
        raise APIError("Unexpected transcription job payload")
    store_id = _extract_output_store_id(job, role=role)
    store = None
    if store_id:
        try:
            store = call_json(get_file_store_op, client=client, store_id=store_id)
        except APIError as exc:
            store = {"id": store_id, "warning": str(exc)}
    emit(
        {
            "job_id": job_id,
            "status": job.get("status"),
            "role": role,
            "output_file_store_id": store_id,
            "output_file_stores": ((job.get("result") or {}).get("output_file_stores") if isinstance(job.get("result"), dict) else None),
            "store": store,
            "s3_locations": _extract_s3_locations(job),
            "result": job.get("result"),
        }
    )


@output_app.command("push-hf")
@handle_cli_errors
def push_output_to_hf(
    repo_id: str = typer.Option(..., "--repo-id", help="Destination HF dataset repo id (org/name)."),
    job_id: str | None = typer.Option(None, "--job-id", help="Transcription job id to resolve the output file store from."),
    file_store_id: str | None = typer.Option(None, "--file-store-id", help="Output FileStore id to push."),
    role: str = typer.Option("primary", help="Output role when resolving from --job-id."),
    wait: bool = typer.Option(False, "--wait", help="Block until the HF push finishes."),
    timeout: float = typer.Option(1800.0, help="Max seconds to wait when --wait is set."),
    poll_interval: float = typer.Option(5.0, help="Seconds between status polls."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    if bool(job_id) == bool(file_store_id):
        raise UsageError("Provide exactly one of --job-id or --file-store-id.")

    client = make_client(api_key)
    resolved_store_id = file_store_id
    if job_id:
        job = call_json(get_transcription_job_op, client=client, job_id=job_id)
        if not isinstance(job, dict):
            raise APIError("Unexpected transcription job payload")
        resolved_store_id = _extract_output_store_id(job, role=role)
        if not resolved_store_id:
            raise UsageError(f"No output file store found for role={role!r} on job {job_id}.")

    result = _request_json(
        client,
        "POST",
        f"/api/v1/file-stores/{resolved_store_id}/to-hf",
        json_body={"repo_id": repo_id, "repo_type": "dataset"},
    )
    if not wait:
        emit({
            "file_store_id": resolved_store_id,
            "repo_id": repo_id,
            "submit": result,
        })
        return

    transfer_job_id = (result or {}).get("job_id") if isinstance(result, dict) else None
    if not isinstance(transfer_job_id, str):
        emit(result)
        return

    final = poll_until_terminal(
        lambda: call_json(get_data_prep_job_op, client=client, job_id=transfer_job_id),
        timeout=timeout,
        interval=poll_interval,
        on_update=_render_job_updates,
    )
    emit({
        "file_store_id": resolved_store_id,
        "repo_id": repo_id,
        "submit": result,
        "final": final,
    })


# ---------------------------------------------------------------------------
# Mount sub-apps
# ---------------------------------------------------------------------------


upload_app.command("folder")(file_stores_cmd.upload_folder)
upload_app.command("parquet")(file_stores_cmd.upload_parquet)

app.add_typer(models_app)
app.add_typer(upload_app)
app.add_typer(prepare_app)
app.add_typer(transcribe_app)
app.add_typer(jobs_app)
app.add_typer(output_app)
