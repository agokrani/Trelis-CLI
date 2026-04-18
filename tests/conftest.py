"""Shared test fixtures: respx httpx mock + isolated env.

We mock the network, never the SDK. Tests should look like real CLI
invocations: respx receives a path/method, returns a canned response,
and the SDK + CLI run end-to-end against it.
"""

from __future__ import annotations

import pytest
import respx
from typer.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Isolate auth state — no real keyring or env leakage into tests."""
    monkeypatch.setenv("TRELIS_API_KEY", "test-key")
    monkeypatch.delenv("TRELIS_BASE_URL", raising=False)


@pytest.fixture
def mock_api(env: None) -> respx.Router:
    """Return an active respx router scoped to https://studio.trelis.com."""
    with respx.mock(base_url="https://studio.trelis.com", assert_all_called=False) as router:
        yield router
