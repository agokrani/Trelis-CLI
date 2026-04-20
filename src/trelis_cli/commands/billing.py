"""Billing resource: balance, tier, transactions (read-only)."""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from trelis_sdk.api.api_v1 import (
    get_credit_balance_api_v1_billing_balance_get as _balance,
)
from trelis_sdk.api.api_v1 import (
    get_tier_info_api_v1_billing_tier_get as _tier,
)
from trelis_sdk.api.api_v1 import (
    get_transaction_history_api_v1_billing_transactions_get as _transactions,
)

from ..api_helpers import call_json
from ..auth import make_client
from ..errors import handle_cli_errors
from ..output import emit

app = typer.Typer(name="billing", help="Credit balance, tier, and transaction history.")
_console = Console()


def _render_transactions(payload: dict) -> None:
    items = (payload or {}).get("transactions", []) if isinstance(payload, dict) else []
    if not items:
        _console.print("[yellow]No transactions.[/yellow]")
        return
    table = Table(show_header=True, header_style="bold")
    for col in ("created_at", "amount", "balance_after", "transaction_type", "description"):
        table.add_column(col)
    for t in items:
        table.add_row(
            str(t.get("created_at", "")),
            str(t.get("amount", "")),
            str(t.get("balance_after", "")),
            str(t.get("transaction_type", "")),
            str(t.get("description", "")),
        )
    _console.print(table)


@app.command()
@handle_cli_errors
def balance(
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """Show current credit balance for the caller's project."""
    client = make_client(api_key)
    emit(call_json(_balance, client=client))


@app.command()
@handle_cli_errors
def tier(
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """Show tier, job slots, timeouts, and upgrade path."""
    client = make_client(api_key)
    emit(call_json(_tier, client=client))


@app.command()
@handle_cli_errors
def transactions(
    limit: int = typer.Option(50, help="Max transactions to return."),
    api_key: str | None = typer.Option(None, "--api-key"),
) -> None:
    """Show recent credit transactions (usage, top-ups, migrations)."""
    client = make_client(api_key)
    result = call_json(_transactions, client=client, limit=limit)
    emit(result, human_renderer=_render_transactions)
