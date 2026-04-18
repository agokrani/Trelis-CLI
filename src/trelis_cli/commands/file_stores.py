"""File-stores resource: list + hand-written upload-parquet UX.

The spec exposes three upload pathways (direct multipart, single presigned,
batch presigned). For now we implement the direct-multipart path; the
heuristic to switch to presigned for large/many files is a Phase B item
once we can calibrate against the live server.
"""

from __future__ import annotations

import time
from pathlib import Path

import typer
from rich.console import Console

from trelis_sdk.api.api_v1 import (
    list_file_stores_api_v1_file_stores_get,
    upload_parquet_to_file_store_api_v1_file_stores_upload_parquet_post as upload_parquet_op,
)
from trelis_sdk.models.body_upload_parquet_to_file_store_api_v1_file_stores_upload_parquet_post import (
    BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost as ParquetBody,
)
from trelis_sdk.types import UNSET, File

from ..api_helpers import call_json
from ..auth import make_client
from ..errors import TimeoutError as CLITimeoutError
from ..errors import UsageError, handle_cli_errors
from ..output import emit

app = typer.Typer(name="file-stores", help="Manage file stores (datasets).")
_console = Console()


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


@app.command("upload-parquet")
@handle_cli_errors
def upload_parquet(
    path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    name: str | None = typer.Option(None, help="Optional store name (defaults to filename stem)."),
    wait: bool = typer.Option(False, "--wait", help="Block until processing finishes."),
    timeout: float = typer.Option(1800.0, help="Max seconds to wait when --wait is set."),
    poll_interval: float = typer.Option(5.0, help="Seconds between polls."),
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

    if not wait:
        emit(result)
        return

    # The upload response includes the new store ID; poll its file status to
    # completion. Real status-state vocabulary will be confirmed in Phase B.
    store_id = (result or {}).get("file_store_id") or (result or {}).get("id")
    filename = (result or {}).get("name") or path.name
    if not store_id:
        emit(result)
        return

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
