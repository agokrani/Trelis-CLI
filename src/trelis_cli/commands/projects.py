"""Projects resource: list + get (read-only).

v2 of the spec removed POST/PATCH/DELETE for projects — they're now
dashboard-only. Same for `/projects/{id}/members`.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from trelis_sdk.api.api_v1 import (
    get_project_api_v1_projects_project_id_get as _get_project,
)
from trelis_sdk.api.api_v1 import (
    list_projects_api_v1_projects_get as _list_projects,
)

from ..api_helpers import call_json
from ..auth import make_client
from ..errors import handle_cli_errors
from ..output import emit

app = typer.Typer(name="projects", help="List and inspect projects (read-only).")
_console = Console()


def _render_project_list(payload: dict) -> None:
    items = (payload or {}).get("projects", []) if isinstance(payload, dict) else []
    if not items:
        _console.print("[yellow]No projects.[/yellow]")
        return
    table = Table(show_header=True, header_style="bold")
    for col in ("id", "name", "role", "credits_pool", "created_at"):
        table.add_column(col)
    for p in items:
        table.add_row(
            str(p.get("id", "")),
            str(p.get("name", "")),
            str(p.get("role", "")),
            str(p.get("credits_pool", "")),
            str(p.get("created_at", "")),
        )
    _console.print(table)


@app.command("list")
@handle_cli_errors
def list_(
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """List all projects the current user is a member of."""
    client = make_client(api_key)
    result = call_json(_list_projects, client=client)
    emit(result, human_renderer=_render_project_list)


@app.command("get")
@handle_cli_errors
def get(
    project_id: str = typer.Argument(..., help="Project UUID."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """Get a single project's details."""
    client = make_client(api_key)
    result = call_json(_get_project, client=client, project_id=project_id)
    emit(result)
