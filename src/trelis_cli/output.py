"""Output formatting: human (rich) vs agent (--json) contract.

Every command writes through `emit()`. When `--json` is set, output is
JSON on stdout and errors are JSON on stderr. Otherwise we use rich.
"""

from __future__ import annotations

import json
import sys
from contextvars import ContextVar
from dataclasses import asdict, is_dataclass
from typing import Any

from rich.console import Console

_console = Console()
_err_console = Console(stderr=True)

_json_mode: ContextVar[bool] = ContextVar("json_mode", default=False)


def set_json_mode(enabled: bool) -> None:
    _json_mode.set(enabled)


def is_json_mode() -> bool:
    return _json_mode.get()


def _to_jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    if is_dataclass(value):
        return _to_jsonable(asdict(value))
    if hasattr(value, "to_dict"):
        return _to_jsonable(value.to_dict())
    if hasattr(value, "model_dump"):
        return _to_jsonable(value.model_dump())
    return str(value)


def emit(value: Any, *, human_renderer: Any = None) -> None:
    """Write a successful result.

    `value` is the agent-stable JSON shape. `human_renderer` is an optional
    callable that takes `value` and renders to rich for humans.
    """
    if is_json_mode():
        json.dump(_to_jsonable(value), sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
        return
    if human_renderer is not None:
        human_renderer(value)
        return
    _console.print(value)


def emit_error(message: str, *, exit_code: int, status_code: int | None = None) -> None:
    """Write an error and (caller is responsible for exiting)."""
    if is_json_mode():
        payload = {"error": message, "exit_code": exit_code}
        if status_code is not None:
            payload["status_code"] = status_code
        json.dump(payload, sys.stderr, indent=2)
        sys.stderr.write("\n")
        return
    _err_console.print(f"[red]Error:[/red] {message}")
