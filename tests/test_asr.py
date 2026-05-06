"""ASR workflow command smoke tests."""

from __future__ import annotations

import json

import respx
from httpx import Response

from trelis_cli.__main__ import app


_ASR_MODELS_PAYLOAD = {
    "models": [
        {
            "model_id": "openai/whisper-small",
            "family": "whisper",
            "modality": "asr",
            "size": "244M",
            "trainable": True,
            "inference_only": False,
            "router_model": False,
        },
        {
            "model_id": "fireworks/whisper-v3",
            "family": "router",
            "modality": "asr",
            "size": None,
            "trainable": False,
            "inference_only": False,
            "router_model": True,
        },
        {
            "model_id": "sarvam/saaras-v3",
            "family": "router",
            "modality": "asr",
            "size": None,
            "trainable": False,
            "inference_only": False,
            "router_model": True,
        },
    ],
    "total": 3,
}


def test_asr_models_list_router_filter(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/models").mock(return_value=Response(200, json=_ASR_MODELS_PAYLOAD))

    result = runner.invoke(app, ["--json", "asr", "models", "list", "--engine", "router"])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["total"] == 2
    assert payload["models"][0]["model_id"] == "fireworks/whisper-v3"
    assert payload["models"][0]["engine"] == "router"
    assert payload["models"][0]["requires_router_key"] is True


def test_asr_models_show_unknown_model_infers_engine(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/models").mock(return_value=Response(200, json=_ASR_MODELS_PAYLOAD))

    result = runner.invoke(app, ["--json", "asr", "models", "show", "assemblyai/custom-asr"])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["known_model"] is False
    assert payload["engine"] == "router"
    assert payload["requires_router_key"] is True


def test_asr_transcribe_submit_rejects_router_timestamps(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/models").mock(return_value=Response(200, json=_ASR_MODELS_PAYLOAD))

    result = runner.invoke(
        app,
        [
            "--json",
            "asr",
            "transcribe",
            "submit",
            "--model",
            "fireworks/whisper-v3",
            "--language",
            "en",
            "--dataset-id",
            "Trelis/demo-ds",
            "--timestamps",
        ],
    )
    assert result.exit_code == 1
    err = json.loads(result.stderr)
    assert "Router ASR does not support timestamps" in err["error"]


def test_asr_transcribe_submit_rejects_router_without_project_key(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/models").mock(return_value=Response(200, json=_ASR_MODELS_PAYLOAD))
    mock_api.get("/api/v1/me/").mock(
        return_value=Response(200, json={"email": "user@example.com", "router_key_present": False})
    )

    result = runner.invoke(
        app,
        [
            "--json",
            "asr",
            "transcribe",
            "submit",
            "--model",
            "fireworks/whisper-v3",
            "--language",
            "en",
            "--dataset-id",
            "Trelis/demo-ds",
        ],
    )
    assert result.exit_code == 1
    err = json.loads(result.stderr)
    assert "has no router key configured" in err["error"]



def test_asr_transcribe_submit_sarvam_mode_payload(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/models").mock(return_value=Response(200, json=_ASR_MODELS_PAYLOAD))
    mock_api.get("/api/v1/me/").mock(
        return_value=Response(200, json={"email": "user@example.com", "router_key_present": True})
    )
    route = mock_api.post("/api/v1/transcription").mock(
        return_value=Response(200, json={"job_id": "tx-sarvam", "status": "pending", "message": "started"})
    )

    result = runner.invoke(
        app,
        [
            "--json",
            "asr",
            "transcribe",
            "submit",
            "--model",
            "sarvam/saaras-v3",
            "--language",
            "auto",
            "--dataset-id",
            "Trelis/demo-ds",
            "--sarvam-mode",
            "codemix",
        ],
    )
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["resolved_engine"] == "router"
    sent = json.loads(route.calls.last.request.content.decode())
    assert sent["router_provider_options"] == {"mode": "codemix"}



def test_asr_transcribe_submit_internal_success(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/models").mock(return_value=Response(200, json=_ASR_MODELS_PAYLOAD))
    route = mock_api.post("/api/v1/transcription").mock(
        return_value=Response(200, json={"job_id": "tx-1", "status": "pending", "message": "started"})
    )

    result = runner.invoke(
        app,
        [
            "--json",
            "asr",
            "transcribe",
            "submit",
            "--model",
            "openai/whisper-small",
            "--language",
            "en",
            "--dataset-id",
            "Trelis/demo-ds",
            "--split",
            "train",
            "--num-samples",
            "25",
        ],
    )
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["job_id"] == "tx-1"
    assert payload["resolved_engine"] == "internal"
    sent = json.loads(route.calls.last.request.content.decode())
    assert sent["dataset_id"] == "Trelis/demo-ds"
    assert sent["dataset_split"] == "train"
    assert sent["num_samples"] == 25


def test_asr_transcribe_submit_rejects_raw_upload_filestore(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/models").mock(return_value=Response(200, json=_ASR_MODELS_PAYLOAD))
    mock_api.get("/api/v1/file-stores/fs_raw").mock(
        return_value=Response(
            200,
            json={
                "id": "fs_raw",
                "name": "raw-upload",
                "source": "upload",
                "storage_backend": "s3",
                "content_type": "audio_text_pairs",
                "file_count": 20,
                "size_bytes": 1024,
                "total_duration_seconds": None,
                "created_at": "2026-04-22T00:00:00Z",
            },
        )
    )

    result = runner.invoke(
        app,
        [
            "--json",
            "asr",
            "transcribe",
            "submit",
            "--model",
            "openai/whisper-small",
            "--language",
            "en",
            "--file-store-id",
            "fs_raw",
        ],
    )
    assert result.exit_code == 1
    err = json.loads(result.stderr)
    assert "Run `trelis asr prepare file-store <id>` first" in err["error"]


def test_asr_prepare_file_store_wait_returns_output_store(runner, mock_api: respx.Router) -> None:
    mock_api.post("/api/v1/file-stores/store-1/process").mock(
        return_value=Response(200, json={"job_id": "dp-1", "status": "pending"})
    )
    mock_api.get("/api/v1/data-prep/jobs/dp-1").mock(
        side_effect=[
            Response(200, json={"id": "dp-1", "status": "running"}),
            Response(
                200,
                json={
                    "id": "dp-1",
                    "status": "completed",
                    "result": {
                        "output_file_store_id": "fs-prepared",
                        "dataset_id": "Trelis/prepared-demo",
                    },
                },
            ),
        ]
    )

    result = runner.invoke(
        app,
        ["--json", "asr", "prepare", "file-store", "store-1", "--wait"],
    )
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["prepared_file_store_id"] == "fs-prepared"
    assert payload["dataset_id"] == "Trelis/prepared-demo"
    assert payload["final"]["status"] == "completed"



def test_asr_jobs_watch_and_cancel(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/transcription/jobs/watch-1").mock(
        side_effect=[
            Response(200, json={"id": "watch-1", "status": "running"}),
            Response(200, json={"id": "watch-1", "status": "completed", "result": {"ok": True}}),
        ]
    )
    mock_api.post("/api/v1/transcription/jobs/cancel-1/cancel").mock(
        return_value=Response(200, json={"id": "cancel-1", "status": "cancelled"})
    )

    watch_result = runner.invoke(app, ["--json", "asr", "jobs", "watch", "watch-1", "--poll-interval", "0.01"])
    assert watch_result.exit_code == 0, watch_result.stderr
    watch_payload = json.loads(watch_result.stdout)
    assert watch_payload["status"] == "completed"

    cancel_result = runner.invoke(app, ["--json", "asr", "jobs", "cancel", "cancel-1"])
    assert cancel_result.exit_code == 0, cancel_result.stderr
    cancel_payload = json.loads(cancel_result.stdout)
    assert cancel_payload["status"] == "cancelled"


def test_asr_output_show_extracts_store_and_s3_key(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/transcription/jobs/job-1").mock(
        return_value=Response(
            200,
            json={
                "id": "job-1",
                "status": "completed",
                "result": {"output_file_stores": {"primary": "fs-out"}},
                "logs": "Shard done (s3_key=projects/p/transcription/job-1/shard-00000.parquet)",
            },
        )
    )
    mock_api.get("/api/v1/file-stores/fs-out").mock(
        return_value=Response(
            200,
            json={
                "id": "fs-out",
                "name": "transcribed-demo",
                "source": "transcription",
                "storage_backend": "s3",
                "content_type": "transcribed_dataset",
                "file_count": 1,
                "size_bytes": 0,
                "total_duration_seconds": None,
                "created_at": "2026-04-22T00:00:00Z",
            },
        )
    )

    result = runner.invoke(app, ["--json", "asr", "output", "show", "job-1"])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["output_file_store_id"] == "fs-out"
    assert payload["store"]["content_type"] == "transcribed_dataset"
    assert payload["s3_locations"] == ["projects/p/transcription/job-1/shard-00000.parquet"]



def test_asr_output_push_hf_requires_exactly_one_locator(runner) -> None:
    result = runner.invoke(
        app,
        [
            "--json",
            "asr",
            "output",
            "push-hf",
            "--repo-id",
            "Trelis/demo-output",
            "--job-id",
            "job-1",
            "--file-store-id",
            "fs-1",
        ],
    )
    assert result.exit_code == 1
    err = json.loads(result.stderr)
    assert "exactly one of --job-id or --file-store-id" in err["error"]


def test_asr_output_push_hf_wait_from_job(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/transcription/jobs/job-2").mock(
        return_value=Response(
            200,
            json={
                "id": "job-2",
                "status": "completed",
                "result": {"output_file_stores": {"primary": "fs-out-2"}},
            },
        )
    )
    mock_api.post("/api/v1/file-stores/fs-out-2/to-hf").mock(
        return_value=Response(200, json={"job_id": "hf-1", "status": "pending"})
    )
    mock_api.get("/api/v1/data-prep/jobs/hf-1").mock(
        return_value=Response(
            200,
            json={
                "id": "hf-1",
                "status": "completed",
                "result": {
                    "success": True,
                    "repo_id": "Trelis/demo-output",
                    "repo_url": "https://huggingface.co/datasets/Trelis/demo-output",
                },
            },
        )
    )

    result = runner.invoke(
        app,
        [
            "--json",
            "asr",
            "output",
            "push-hf",
            "--job-id",
            "job-2",
            "--repo-id",
            "Trelis/demo-output",
            "--wait",
        ],
    )
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["file_store_id"] == "fs-out-2"
    assert payload["final"]["result"]["repo_id"] == "Trelis/demo-output"



def test_asr_jobs_list_and_get(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/transcription/jobs").mock(
        return_value=Response(200, json={"jobs": [{"id": "job-a", "status": "completed"}]})
    )
    mock_api.get("/api/v1/transcription/jobs/job-a").mock(
        return_value=Response(200, json={"id": "job-a", "status": "completed", "result": {"ok": True}})
    )

    list_result = runner.invoke(app, ["--json", "asr", "jobs", "list", "--limit", "5"])
    assert list_result.exit_code == 0, list_result.stderr
    list_payload = json.loads(list_result.stdout)
    assert list_payload["jobs"][0]["id"] == "job-a"

    get_result = runner.invoke(app, ["--json", "asr", "jobs", "get", "job-a"])
    assert get_result.exit_code == 0, get_result.stderr
    get_payload = json.loads(get_result.stdout)
    assert get_payload["id"] == "job-a"
    assert get_payload["result"]["ok"] is True
