"""Models resource: list (read-only)."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from trelis_sdk.api.api_v1 import list_models_api_v1_models_get
from trelis_sdk.types import UNSET

from ..api_helpers import call_json
from ..auth import make_client
from ..errors import handle_cli_errors
from ..output import emit

app = typer.Typer(name="models", help="List and inspect available models.")
_console = Console()


def _render_table(rows: list[dict] | dict) -> None:
    items = rows if isinstance(rows, list) else rows.get("data", []) if isinstance(rows, dict) else []
    if not items:
        _console.print("[yellow]No models.[/yellow]")
        return
    table = Table(show_header=True, header_style="bold")
    columns = list(items[0].keys()) if isinstance(items[0], dict) else ["value"]
    for col in columns:
        table.add_column(col)
    for item in items:
        if isinstance(item, dict):
            table.add_row(*[str(item.get(c, "")) for c in columns])
        else:
            table.add_row(str(item))
    _console.print(table)


@app.command("list")
@handle_cli_errors
def list_(
    modality: str | None = typer.Option(None, help="Filter by modality (e.g. asr, tts)."),
    family: str | None = typer.Option(None, help="Filter by family."),
    trainable: bool | None = typer.Option(None, help="Show only trainable models."),
    api_key: str | None = typer.Option(None, "--api-key", help="Override stored credential."),
) -> None:
    """List available models."""
    client = make_client(api_key)
    result = call_json(
        list_models_api_v1_models_get,
        client=client,
        modality=modality if modality is not None else UNSET,
        family=family if family is not None else UNSET,
        trainable=trainable if trainable is not None else UNSET,
    )
    emit(result, human_renderer=_render_table)
