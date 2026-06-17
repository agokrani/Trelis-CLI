"""Auth commands: login, logout, whoami."""

from __future__ import annotations

import typer
from rich.console import Console

from trelis_sdk.api.api_v1 import get_me_api_v1_me_get

from ..api_helpers import call_json
from ..auth import clear_token, make_client, store_token
from ..errors import handle_cli_errors
from ..output import emit

app = typer.Typer(name="auth", help="Authentication commands.")
_console = Console()


@app.command()
@handle_cli_errors
def login(
    api_key: str = typer.Option(
        ..., "--api-key", prompt=True, hide_input=True, help="Your Trelis API key."
    ),
) -> None:
    """Store an API key in the system keyring."""
    store_token(api_key)
    emit({"stored": True}, human_renderer=lambda _: _console.print("[green]Stored.[/green]"))


@app.command()
@handle_cli_errors
def logout() -> None:
    """Remove the stored API key from the system keyring."""
    clear_token()
    emit({"removed": True}, human_renderer=lambda _: _console.print("[green]Logged out.[/green]"))


@app.command()
@handle_cli_errors
def whoami(
    api_key: str | None = typer.Option(None, "--api-key", help="Override stored credential."),
) -> None:
    """Show the current authenticated user."""
    client = make_client(api_key)
    result = call_json(get_me_api_v1_me_get, client=client)
    emit(result, human_renderer=lambda r: _console.print(r))
