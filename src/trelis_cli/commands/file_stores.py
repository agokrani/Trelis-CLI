"""File-stores resource: list + upload helpers.

This module currently exposes:
- list
- upload-parquet
- upload-folder (raw audio/transcript files via presigned PUT URLs)
"""

from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import httpx
import typer
from rich.console import Console

from trelis_sdk.api.api_v1 import (
    delete_file_store_api_v1_file_stores_store_id_delete as delete_store_op,
    get_file_store_upload_urls_api_v1_file_stores_upload_urls_post as upload_urls_op,
    list_file_stores_api_v1_file_stores_get,
    list_file_store_files_api_v1_file_stores_store_id_files_get as list_files_op,
    upload_parquet_to_file_store_api_v1_file_stores_upload_parquet_post as upload_parquet_op,
)
from trelis_sdk.models.body_upload_parquet_to_file_store_api_v1_file_stores_upload_parquet_post import (
    BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost as ParquetBody,
)
from trelis_sdk.models.file_store_batch_upload_entry import FileStoreBatchUploadEntry
from trelis_sdk.models.file_store_batch_upload_request import FileStoreBatchUploadRequest
from trelis_sdk.types import UNSET, File

from ..api_helpers import call_json
from ..auth import make_client
from ..errors import APIError
from ..errors import TimeoutError as CLITimeoutError
from ..errors import UsageError, handle_cli_errors
from ..output import emit, is_json_mode

app = typer.Typer(name="file-stores", help="Manage file stores (datasets).")
_console = Console()

_CONTENT_TYPES = {
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
    ".m4a": "audio/mp4",
    ".sph": "audio/x-sphere",
    ".qta": "audio/quicktime",
    ".ogg": "audio/ogg",
    ".srt": "text/plain",
    ".vtt": "text/vtt",
    ".txt": "text/plain",
}
_SUPPORTED_EXTENSIONS = frozenset(_CONTENT_TYPES)
_BATCH_UPLOAD_LIMIT = 5000
_UPLOAD_TIMEOUT_SECONDS = 300.0
_DATASET_INFO_FILENAME = "dataset_info.json"


@app.command("list")
@handle_cli_errors
def list_(
    limit: int = typer.Option(50, help="Max results to return."),
    offset: int = typer.Option(0, help="Pagination offset."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """List file stores."""
    client = make_client(api_key)
    result = call_json(
        list_file_stores_api_v1_file_stores_get,
        client=client,
        limit=limit,
        offset=offset,
    )
    emit(result)


@app.command("delete")
@handle_cli_errors
def delete_(
    store_id: list[str] = typer.Argument(
        ...,
        help="One or more file store IDs to delete.",
    ),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """Delete one or more file stores by ID."""
    client = make_client(api_key)
    deleted: list[dict[str, str | bool]] = []
    for one_id in store_id:
        result = call_json(delete_store_op, client=client, store_id=one_id)
        if isinstance(result, dict):
            deleted.append(result)
        else:
            deleted.append({"id": one_id, "deleted": True})
    emit({"deleted": deleted})


@app.command("delete-by-name")
@handle_cli_errors
def delete_by_name(
    names: list[str] = typer.Argument(..., help="One or more file store names to delete."),
    limit: int = typer.Option(200, help="Page size for listing file stores while resolving names."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """Delete file stores by exact display name (all matches per name)."""
    if not names:
        raise UsageError("Provide at least one file store name.")

    client = make_client(api_key)
    target_names = set(names)

    to_delete: list[str] = []
    found_names: set[str] = set()
    offset = 0
    total = None

    while True:
        listing = call_json(
            list_file_stores_api_v1_file_stores_get,
            client=client,
            limit=limit,
            offset=offset,
        )
        if not isinstance(listing, dict):
            raise APIError("Unexpected response from file-stores list endpoint")

        stores = listing.get("stores")
        if not isinstance(stores, list):
            raise APIError("Unexpected list payload: missing stores")

        for store in stores:
            if not isinstance(store, dict):
                continue
            store_name = store.get("name")
            if isinstance(store_name, str) and store_name in target_names:
                found_names.add(store_name)
                store_id_value = store.get("id")
                if isinstance(store_id_value, str):
                    to_delete.append(store_id_value)

        if total is None:
            total = listing.get("total")
            if not isinstance(total, int):
                total = 0

        if offset + len(stores) >= total:
            break
        offset += limit

    missing = sorted(name for name in target_names if name not in found_names)
    if missing:
        raise UsageError(f"No file stores found for: {', '.join(missing)}")

    if not to_delete:
        raise UsageError("No file stores matched the provided names.")

    deleted: list[dict[str, str | bool]] = []
    for one_id in to_delete:
        result = call_json(delete_store_op, client=client, store_id=one_id)
        if isinstance(result, dict):
            deleted.append(result)
        else:
            deleted.append({"id": one_id, "deleted": True})

    emit({"deleted": deleted, "requested_names": sorted(target_names)})


@app.command("upload-parquet")
@handle_cli_errors
def upload_parquet(
    path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    name: str | None = typer.Option(None, help="Optional store name (defaults to filename stem)."),
    wait: bool = typer.Option(False, "--wait", help="Block until processing finishes."),
    timeout: float = typer.Option(1800.0, help="Max seconds to wait when --wait is set."),
    poll_interval: float = typer.Option(5.0, help="Seconds between polls."),
    ensure_dataset_info: bool = typer.Option(
        True,
        "--ensure-dataset-info/--skip-dataset-info",
        help=(
            "Check for missing dataset_info.json and upload it as a sidecar "
            "when absent. Does not fix backend contract metadata stored in DB."
        ),
    ),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """Upload a .parquet file as a new file store.

    Currently uses the direct-multipart pathway
    (`POST /api/v1/file-stores/upload-parquet`). Presigned-URL pathway will
    kick in for large files in a later iteration.
    """
    if path.suffix.lower() != ".parquet":
        raise UsageError(f"Expected a .parquet file, got {path.suffix}")

    client = make_client(api_key)
    with path.open("rb") as fh:
        body = ParquetBody(file=File(payload=fh, file_name=path.name, mime_type="application/octet-stream"))
        result = call_json(
            upload_parquet_op,
            client=client,
            body=body,
            name=name if name is not None else UNSET,
        )

    dataset_info_status: str | None = None
    if ensure_dataset_info and isinstance(result, dict):
        dataset_info_status = _ensure_dataset_info_sidecar(
            client=client,
            store_id=(result or {}).get("file_store_id") or (result or {}).get("id"),
            upload_result=result,
        )
        result["dataset_info_status"] = dataset_info_status

    if not wait:
        if not is_json_mode() and ensure_dataset_info and isinstance(dataset_info_status, str):
            _render_dataset_info_notice(dataset_info_status, (result or {}).get("file_store_id"))
        emit(result)
        return

    # The upload response includes the new store ID; poll its file status to
    # completion. Real status-state vocabulary will be confirmed in Phase B.
    store_id = (result or {}).get("file_store_id") or (result or {}).get("id")
    filename = (result or {}).get("name") or path.name
    if not store_id:
        if not is_json_mode() and ensure_dataset_info and isinstance(dataset_info_status, str):
            _render_dataset_info_notice(dataset_info_status, None)
        emit(result)
        return

    if not is_json_mode() and ensure_dataset_info and isinstance(dataset_info_status, str):
        _render_dataset_info_notice(dataset_info_status, store_id)

    deadline = time.monotonic() + timeout
    last: dict | None = None
    while True:
        # TODO(phase-b): swap to the typed file-status endpoint once the
        # response shape is captured against staging.
        status_resp = client.get_httpx_client().get(
            f"/api/v1/file-stores/{store_id}/files/{filename}/status"
        )
        last = status_resp.json() if status_resp.content else {}
        state = (last.get("status") or last.get("state") or "").lower()
        if state in {"completed", "failed", "error", "ready"}:
            emit({"upload": result, "status": last})
            return
        if time.monotonic() >= deadline:
            raise CLITimeoutError(
                f"Upload processing did not finish within {timeout:.0f}s "
                f"(last state: {state or 'unknown'})"
            )
        time.sleep(poll_interval)


@app.command("upload-folder")
@handle_cli_errors
def upload_folder(
    path: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True, readable=True),
    name: str | None = typer.Option(None, help="Optional store name (defaults to folder name)."),
    ignore_unsupported: bool = typer.Option(
        False,
        "--ignore-unsupported",
        help="Skip unsupported files instead of failing.",
    ),
    include_hidden: bool = typer.Option(
        False,
        "--include-hidden",
        help="Include dotfiles and files under hidden directories.",
    ),
    batch_size: int = typer.Option(
        _BATCH_UPLOAD_LIMIT,
        min=1,
        max=_BATCH_UPLOAD_LIMIT,
        help="Files per presigned-URL batch request.",
    ),
    concurrency: int = typer.Option(
        8,
        min=1,
        max=64,
        help="Parallel uploads per batch.",
    ),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """Upload a local folder of raw audio/transcript files.

    Files are scanned recursively and uploaded via
    `POST /api/v1/file-stores/upload-urls` + presigned PUTs.

    Important: the server stores files by basename only, so duplicate
    filenames across subdirectories are rejected by this command.
    """
    files, unsupported = _collect_upload_files(path, include_hidden=include_hidden)
    if unsupported and not ignore_unsupported:
        preview = ", ".join(str(p.relative_to(path)) for p in unsupported[:10])
        raise UsageError(
            "Unsupported files found. Supported extensions: "
            f"{', '.join(sorted(_SUPPORTED_EXTENSIONS))}. "
            f"Examples: {preview}"
        )
    if ignore_unsupported:
        files = [p for p in files if p.suffix.lower() in _SUPPORTED_EXTENSIONS]

    if not files:
        raise UsageError("No supported files found in the folder.")

    zero_bytes = [p for p in files if p.stat().st_size <= 0]
    if zero_bytes:
        preview = ", ".join(str(p.relative_to(path)) for p in zero_bytes[:10])
        raise UsageError(f"Zero-byte files are not supported. Examples: {preview}")

    duplicates = _find_duplicate_basenames(files)
    if duplicates:
        examples = []
        for name_, paths in list(duplicates.items())[:10]:
            rels = ", ".join(str(p.relative_to(path)) for p in paths[:3])
            examples.append(f"{name_}: {rels}")
        raise UsageError(
            "Duplicate basenames found. Folder upload is flattened to filenames on the server, "
            "so files from different subdirectories would collide. "
            f"Examples: {'; '.join(examples)}"
        )

    client = make_client(api_key)
    total_bytes = sum(p.stat().st_size for p in files)
    total_batches = (len(files) + batch_size - 1) // batch_size
    store_name = name or path.name

    if not is_json_mode():
        _console.print(
            f"[cyan]Uploading {len(files)} files ({total_bytes} bytes) from[/cyan] {path}"
        )
        if ignore_unsupported and unsupported:
            _console.print(f"[yellow]Skipping {len(unsupported)} unsupported files.[/yellow]")

    store_id: str | None = None
    uploaded_files = 0
    uploaded_bytes = 0

    for batch_index, batch in enumerate(_chunked(files, batch_size), start=1):
        if not is_json_mode():
            _console.print(
                f"[cyan]Batch {batch_index}/{total_batches}:[/cyan] requesting upload URLs for {len(batch)} files"
            )

        entries = [
            FileStoreBatchUploadEntry(
                filename=file_path.name,
                size_bytes=file_path.stat().st_size,
                content_type=_CONTENT_TYPES[file_path.suffix.lower()],
            )
            for file_path in batch
        ]
        body = FileStoreBatchUploadRequest(
            files=entries,
            file_store_id=store_id if store_id is not None else UNSET,
            name=store_name if store_id is None else UNSET,
        )
        response = call_json(upload_urls_op, client=client, body=body)
        if not isinstance(response, dict) or "file_store_id" not in response or "files" not in response:
            raise APIError("Unexpected response from upload-urls endpoint")

        store_id = response["file_store_id"]
        returned_files = {
            item["filename"]: item
            for item in response.get("files", [])
            if isinstance(item, dict) and "filename" in item and "upload_url" in item
        }
        missing = [file_path.name for file_path in batch if file_path.name not in returned_files]
        if missing:
            raise APIError(
                "Upload URL response did not include all requested files. "
                f"Missing examples: {', '.join(missing[:10])}"
            )

        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = {
                pool.submit(
                    _upload_presigned_file,
                    file_path,
                    returned_files[file_path.name]["upload_url"],
                    returned_files[file_path.name]["content_type"],
                ): file_path
                for file_path in batch
            }
            for future in as_completed(futures):
                file_path = futures[future]
                future.result()
                uploaded_files += 1
                uploaded_bytes += file_path.stat().st_size
                if not is_json_mode() and (
                    uploaded_files == len(files) or uploaded_files % 100 == 0
                ):
                    _console.print(
                        f"[green]Uploaded {uploaded_files}/{len(files)} files[/green]"
                    )

    result = {
        "file_store_id": store_id,
        "name": store_name,
        "uploaded_files": uploaded_files,
        "total_bytes": total_bytes,
        "batches": total_batches,
        "skipped_unsupported": len(unsupported) if ignore_unsupported else 0,
    }
    emit(result, human_renderer=_render_upload_folder_result)


def _render_upload_folder_result(payload: dict) -> None:
    _console.print(
        f"[green]Uploaded {payload.get('uploaded_files', 0)} files to FileStore "
        f"{payload.get('file_store_id', '?')}[/green]"
    )
    _console.print(
        f"name={payload.get('name', '')}  bytes={payload.get('total_bytes', 0)}  "
        f"batches={payload.get('batches', 0)}"
    )
    skipped = int(payload.get("skipped_unsupported", 0) or 0)
    if skipped:
        _console.print(f"[yellow]Skipped unsupported files:[/yellow] {skipped}")


def _collect_upload_files(root: Path, *, include_hidden: bool) -> tuple[list[Path], list[Path]]:
    supported: list[Path] = []
    unsupported: list[Path] = []
    for file_path in sorted(root.rglob("*")):
        if not file_path.is_file():
            continue
        rel = file_path.relative_to(root)
        if not include_hidden and any(part.startswith(".") for part in rel.parts):
            continue
        if file_path.suffix.lower() in _SUPPORTED_EXTENSIONS:
            supported.append(file_path)
        else:
            unsupported.append(file_path)
    return supported, unsupported


def _find_duplicate_basenames(files: list[Path]) -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = {}
    for file_path in files:
        grouped.setdefault(file_path.name, []).append(file_path)
    return {name: paths for name, paths in grouped.items() if len(paths) > 1}


def _chunked(items: list[Path], size: int) -> list[list[Path]]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def _ensure_dataset_info_sidecar(
    *,
    client,
    store_id: str | None,
    upload_result: dict,
) -> str:
    """Ensure ``dataset_info.json`` exists in the file store.

    This is a CLI convenience for legacy/parquet-created stores that may miss
    the file-level companion metadata used by some workflows. It can only upload
    ``dataset_info.json`` if the upload result exposes enough schema hints.
    """
    if not store_id:
        return "skipped: no file_store_id in upload response"

    try:
        listing = call_json(list_files_op, client=client, store_id=store_id)
    except APIError as exc:
        return f"warning: failed to read file list for {store_id}: {exc}"

    if _has_dataset_info_file(listing):
        return "present"

    payload = _build_dataset_info_payload(upload_result)
    if payload is None:
        return "warning: could not build dataset_info.json from upload response"

    payload_bytes = json.dumps(payload).encode("utf-8")
    entry = FileStoreBatchUploadEntry(
        filename=_DATASET_INFO_FILENAME,
        size_bytes=len(payload_bytes),
        content_type="application/json",
    )
    request = FileStoreBatchUploadRequest(
        files=[entry],
        file_store_id=store_id,
    )
    try:
        upload_urls = call_json(upload_urls_op, client=client, body=request)
    except APIError as exc:
        return f"warning: could not request upload URL for {_DATASET_INFO_FILENAME}: {exc}"

    if not isinstance(upload_urls, dict):
        return "warning: unexpected upload-url response while adding dataset_info.json"

    file_items = upload_urls.get("files")
    if not isinstance(file_items, list):
        return "warning: missing file entry in upload-url response while adding dataset_info.json"

    match = None
    for item in file_items:
        if isinstance(item, dict) and item.get("filename") == _DATASET_INFO_FILENAME:
            match = item
            break
    if not isinstance(match, dict):
        return "warning: upload-url response omitted dataset_info.json entry"

    upload_url = match.get("upload_url")
    content_type = match.get("content_type")
    if not isinstance(upload_url, str):
        return "warning: invalid upload_url for dataset_info.json"

    try:
        _upload_presigned_bytes(
            _DATASET_INFO_FILENAME,
            upload_url=upload_url,
            payload=payload_bytes,
            content_type=content_type or "application/json",
        )
        return "uploaded"
    except APIError as exc:
        return f"warning: dataset_info.json upload failed: {exc}"


def _has_dataset_info_file(listing: object) -> bool:
    if not isinstance(listing, dict):
        return False
    files = listing.get("files")
    if not isinstance(files, list):
        return False
    for item in files:
        if isinstance(item, dict) and item.get("filename") == _DATASET_INFO_FILENAME:
            return True
    return False


def _build_dataset_info_payload(upload_result: dict) -> dict | None:
    num_rows = upload_result.get("num_rows")
    columns = upload_result.get("columns")
    if not isinstance(columns, list) or not columns:
        return None
    return {
        "columns": columns,
        "splits": {
            "train": num_rows,
        },
        "total_rows": num_rows,
    }


def _render_dataset_info_notice(status: str, file_store_id: str | None) -> None:
    if status.startswith("present"):
        return
    if status == "skipped: no file_store_id in upload response":
        return

    if status.startswith("warning:"):
        suffix = f" for {file_store_id}" if file_store_id else ""
        _console.print(f"[yellow]{status}{suffix}[/yellow]")
    elif status == "uploaded":
        location = f" to {file_store_id}" if file_store_id else ""
        _console.print(
            f"[green]Uploaded missing {_DATASET_INFO_FILENAME} sidecar{location}.[/green]"
        )
    else:
        _console.print(f"[yellow]{status}[/yellow]")


def _upload_presigned_bytes(
    filename: str,
    *,
    upload_url: str,
    payload: bytes,
    content_type: str = "application/octet-stream",
) -> None:
    try:
        response = httpx.put(
            upload_url,
            headers={"Content-Type": content_type},
            content=payload,
            follow_redirects=True,
            timeout=_UPLOAD_TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as exc:
        raise APIError(f"Upload failed for {filename}: {exc}") from exc

    if not 200 <= response.status_code < 300:
        detail = response.text.strip()
        suffix = f" HTTP {response.status_code}"
        if detail:
            suffix += f": {detail[:200]}"
        raise APIError(f"Upload failed for {filename}:{suffix}")


def _upload_presigned_file(file_path: Path, upload_url: str, content_type: str) -> None:
    try:
        response = httpx.put(
            upload_url,
            headers={"Content-Type": content_type},
            content=file_path.read_bytes(),
            follow_redirects=True,
            timeout=_UPLOAD_TIMEOUT_SECONDS,
        )
    except httpx.HTTPError as exc:
        raise APIError(f"Upload failed for {file_path.name}: {exc}") from exc

    if not 200 <= response.status_code < 300:
        detail = response.text.strip()
        suffix = f" HTTP {response.status_code}"
        if detail:
            suffix += f": {detail[:200]}"
        raise APIError(f"Upload failed for {file_path.name}:{suffix}")
