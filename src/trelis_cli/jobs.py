"""Shared job-lifecycle primitives.

The Trelis API has 13 resources that follow submit→poll. Every submit
command exposes the same flags via `wait_options()`, and the polling
behaviour is implemented once here.

Terminal states are derived from a small set; the CLI defaults to
`{"completed", "failed", "cancelled", "succeeded", "error"}`. Override by
passing `terminal_states=` to `poll_until_terminal()`.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from .errors import TimeoutError as CLITimeoutError

DEFAULT_TERMINAL = frozenset(
    {"completed", "failed", "cancelled", "canceled", "succeeded", "success", "error"}
)


def poll_until_terminal(
    fetch: Callable[[], dict[str, Any]],
    *,
    timeout: float = 1800.0,
    interval: float = 5.0,
    terminal_states: frozenset[str] = DEFAULT_TERMINAL,
    on_update: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Poll `fetch` until status is terminal or `timeout` seconds elapse.

    `fetch` should return a dict with a `status` (or `state`) field.
    `on_update` is invoked on every poll for --watch UX.
    """
    deadline = time.monotonic() + timeout
    while True:
        result = fetch()
        if on_update is not None:
            on_update(result)
        status = (result.get("status") or result.get("state") or "").lower()
        if status in terminal_states:
            return result
        if time.monotonic() >= deadline:
            raise CLITimeoutError(
                f"Job did not reach a terminal state within {timeout:.0f}s "
                f"(last status: {status or 'unknown'})"
            )
        time.sleep(interval)
