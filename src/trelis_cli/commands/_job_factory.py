"""Factory that generates Typer sub-apps for the 10 job resources.

Every job resource exposes the same command surface:

    trelis <resource> submit --body body.json [--wait]
    trelis <resource> list
    trelis <resource> get <job_id>
    trelis <resource> cancel <job_id>
    trelis <resource> delete <job_id>     (only for resources that support it)

A resource is a `JobResource` descriptor. The factory wires each command
to the right generated SDK module. `cancel` is a uniform CLI verb that
the descriptor maps to whichever endpoint the server actually honors
(`/cancel` or `/stop`) — users never see the difference.

For `submit`, we bypass the generated SDK's typed body class and POST
the raw JSON from `--body` via httpx directly. This lets us ship a
command whose shape matches whatever the server accepts today without
adapting to each per-resource Pydantic class.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

import typer

from ..api_helpers import call_json
from ..auth import make_client
from ..errors import APIError, AuthError, handle_cli_errors
from ..jobs import poll_until_terminal
from ..output import emit


@dataclass(frozen=True)
class JobResource:
    name: str                          # CLI sub-app name, e.g. "training"
    help: str
    list_mod: ModuleType               # SDK module for GET list
    get_mod: ModuleType                # SDK module for GET {id}
    cancel_mod: ModuleType | None      # SDK module for cancel (or stop) — None if not exposed
    submit_path: str | None = None     # POST path, e.g. "/api/v1/training"; None if submit disabled
    delete_mod: ModuleType | None = None


def _submit_raw(client, path: str, payload: Any) -> Any:
    """POST raw JSON via the underlying httpx client and mirror call_json's errors."""
    resp = client.get_httpx_client().post(path, json=payload)
    status = int(resp.status_code)
    body = resp.content
    if 200 <= status < 300:
        if not body:
            return None
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return body.decode("utf-8", errors="replace")
    detail = _extract_api_error_message(body)
    msg = detail or f"API returned {status}"
    if status in (401, 403):
        raise AuthError(msg)
    raise APIError(msg, status_code=status)


def _extract_api_error_message(raw_body: bytes) -> str | None:
    if not raw_body:
        return None
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        return None

    if not isinstance(payload, dict):
        return None

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

def _make_submit(resource: JobResource):
    path = resource.submit_path
    get_mod = resource.get_mod

    @handle_cli_errors
    def submit(
        body: Path = typer.Option(
            ..., "--body", exists=True, dir_okay=False, readable=True,
            help="Path to a JSON file containing the request body.",
        ),
        wait: bool = typer.Option(False, "--wait", help="Block until the job reaches a terminal state."),
        timeout: float = typer.Option(1800.0, help="Max seconds to wait when --wait is set."),
        poll_interval: float = typer.Option(5.0, help="Seconds between status polls."),
        api_key: str | None = typer.Option(None, "--api-key"),
    ) -> None:
        client = make_client(api_key)
        payload = json.loads(body.read_text())
        result = _submit_raw(client, path, payload)

        if not wait:
            emit(result)
            return

        job_id = (result or {}).get("job_id") or (result or {}).get("id")
        if not job_id:
            emit(result)
            return

        def fetch() -> dict:
            return call_json(get_mod, client=client, job_id=job_id)

        final = poll_until_terminal(fetch, timeout=timeout, interval=poll_interval)
        emit({"submit": result, "final": final})

    return submit


def _make_list(resource: JobResource):
    list_mod = resource.list_mod

    @handle_cli_errors
    def list_(
        api_key: str | None = typer.Option(None, "--api-key"),
    ) -> None:
        client = make_client(api_key)
        emit(call_json(list_mod, client=client))

    return list_


def _make_get(resource: JobResource):
    get_mod = resource.get_mod

    @handle_cli_errors
    def get(
        job_id: str = typer.Argument(..., help="Job UUID."),
        api_key: str | None = typer.Option(None, "--api-key"),
    ) -> None:
        client = make_client(api_key)
        emit(call_json(get_mod, client=client, job_id=job_id))

    return get


def _make_cancel(resource: JobResource):
    cancel_mod = resource.cancel_mod

    @handle_cli_errors
    def cancel(
        job_id: str = typer.Argument(..., help="Job UUID."),
        api_key: str | None = typer.Option(None, "--api-key"),
    ) -> None:
        client = make_client(api_key)
        emit(call_json(cancel_mod, client=client, job_id=job_id))

    return cancel


def _make_delete(resource: JobResource):
    delete_mod = resource.delete_mod

    @handle_cli_errors
    def delete(
        job_id: str = typer.Argument(..., help="Job UUID."),
        api_key: str | None = typer.Option(None, "--api-key"),
    ) -> None:
        client = make_client(api_key)
        emit(call_json(delete_mod, client=client, job_id=job_id))

    return delete


def build_resource_app(resource: JobResource) -> typer.Typer:
    """Return a Typer sub-app for the given resource with standard verbs mounted."""
    sub = typer.Typer(name=resource.name, help=resource.help, no_args_is_help=True)

    if resource.submit_path is not None:
        sub.command("submit")(_make_submit(resource))
    sub.command("list")(_make_list(resource))
    sub.command("get")(_make_get(resource))
    if resource.cancel_mod is not None:
        sub.command("cancel")(_make_cancel(resource))
    if resource.delete_mod is not None:
        sub.command("delete")(_make_delete(resource))

    return sub
