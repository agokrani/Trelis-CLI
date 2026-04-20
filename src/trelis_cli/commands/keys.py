"""API keys resource: list (read-only).

v2 of the spec removed POST (create), PATCH (update), and DELETE
(revoke) — key management is now dashboard-only.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from trelis_sdk.api.api_v1 import (
    list_api_keys_api_v1_keys_get as _list_keys,
)
from trelis_sdk.types import UNSET

from ..api_helpers import call_json
from ..auth import make_client
from ..errors import handle_cli_errors
from ..output import emit

app = typer.Typer(name="keys", help="List API keys (read-only).")
_console = Console()


def _render_key_list(payload: dict) -> None:
    items = (payload or {}).get("keys", []) if isinstance(payload, dict) else []
    if not items:
        _console.print("[yellow]No keys.[/yellow]")
        return
    table = Table(show_header=True, header_style="bold")
    for col in ("key_prefix", "name", "project_name", "total_spend", "last_used_at"):
        table.add_column(col)
    for k in items:
        table.add_row(
            str(k.get("key_prefix", "")),
            str(k.get("name", "")),
            str(k.get("project_name", "")),
            str(k.get("total_spend", "")),
            str(k.get("last_used_at", "")),
        )
    _console.print(table)


@app.command("list")
@handle_cli_errors
def list_(
    project_id: str | None = typer.Option(None, help="Filter keys by project UUID."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """List API keys. Full key values are never returned — only prefixes."""
    client = make_client(api_key)
    result = call_json(
        _list_keys,
        client=client,
        project_id=project_id if project_id is not None else UNSET,
    )
    emit(result, human_renderer=_render_key_list)
