"""Exit codes, CLI exception types, and a per-command error decorator.

Exit code contract (documented for agents):
    0 - success
    1 - usage error (bad flag, missing argument)
    2 - API error (4xx/5xx that isn't auth)
    3 - auth error (401, 403, missing credentials)
    4 - timeout / poll exceeded

Errors are surfaced via `@handle_cli_errors` on each command function.
The decorator catches `CLIError`, routes the message through
`output.emit_error` (which respects `--json`), and re-raises as
`typer.Exit(exit_code)`. We avoid Click/Typer's rich-panel rendering of
`ClickException` because it cannot be reliably overridden when
`rich-click` is enabled.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, TypeVar

import typer

F = TypeVar("F", bound=Callable[..., Any])


class CLIError(Exception):
    exit_code: int = 1

    def __init__(self, message: str, *, exit_code: int | None = None) -> None:
        super().__init__(message)
        if exit_code is not None:
            self.exit_code = exit_code


class UsageError(CLIError):
    exit_code = 1


class APIError(CLIError):
    exit_code = 2

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class AuthError(CLIError):
    exit_code = 3


class TimeoutError(CLIError):  # noqa: A001 - intentional shadowing for CLI scope
    exit_code = 4


def handle_cli_errors(fn: F) -> F:
    """Wrap a Typer command to emit `CLIError`s as JSON-aware exits."""
    from .output import emit_error  # local import to avoid cycle

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return fn(*args, **kwargs)
        except CLIError as exc:
            emit_error(
                str(exc),
                exit_code=exc.exit_code,
                status_code=getattr(exc, "status_code", None),
            )
            raise typer.Exit(exc.exit_code) from None

    return wrapper  # type: ignore[return-value]
