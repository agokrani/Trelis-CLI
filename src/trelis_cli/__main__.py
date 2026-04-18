"""Trelis CLI entrypoint.

Top-level Typer app. Resource sub-apps live in `commands/`. Resource
groups are derived from path prefixes (the `api-v1` tag covers 112/116
operations and is therefore useless for grouping).
"""

from __future__ import annotations

import typer

from . import __version__
from .output import set_json_mode

app = typer.Typer(
    name="trelis",
    help="Command-line interface for Trelis Studio.",
    no_args_is_help=True,
    add_completion=True,
)


@app.callback(invoke_without_command=True)
def main(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit JSON on stdout (errors as JSON on stderr). Stable agent contract.",
    ),
    version: bool = typer.Option(
        False, "--version", help="Show version and exit.", is_eager=True
    ),
) -> None:
    if version:
        typer.echo(__version__)
        raise typer.Exit()
    set_json_mode(json_output)


# Resource sub-apps.
from .commands import auth as auth_cmd  # noqa: E402
from .commands import file_stores as file_stores_cmd  # noqa: E402
from .commands import models as models_cmd  # noqa: E402

app.add_typer(auth_cmd.app)
app.add_typer(file_stores_cmd.app, name="file-stores")
app.add_typer(models_cmd.app, name="models")


if __name__ == "__main__":
    app()
