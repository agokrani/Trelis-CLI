"""Credential resolution and AuthenticatedClient construction.

Resolution order:
    1. Explicit `--api-key` flag (passed in by the command)
    2. `TRELIS_API_KEY` env var
    3. keyring (service=trelis-cli, user=default)

The upstream OpenAPI spec declares no security scheme; our overlay.yaml
patches in `BearerAuth`. The generated `AuthenticatedClient` accepts a
`token` kwarg and prepends `Bearer `.

Trelis API keys start with `tsk_`. We warn (not fail) on mismatch so a
prefix change upstream doesn't break the CLI.
"""

from __future__ import annotations

import os
import sys

import keyring

from trelis_sdk import AuthenticatedClient

from .config import KEYRING_SERVICE, KEYRING_USER, base_url
from .errors import AuthError
from .output import is_json_mode

TOKEN_PREFIX = "tsk_"


def _looks_like_trelis_key(token: str) -> bool:
    return token.startswith(TOKEN_PREFIX)


def _maybe_warn_prefix(token: str) -> None:
    """Emit a stderr warning if the token doesn't look like a Trelis key.

    Silent in --json mode to keep stderr machine-parseable.
    """
    if _looks_like_trelis_key(token) or is_json_mode():
        return
    sys.stderr.write(
        f"warning: API key does not start with '{TOKEN_PREFIX}'. "
        "Double-check you pasted a Trelis key (not, e.g., a HuggingFace token).\n"
    )


def resolve_token(explicit: str | None = None) -> str:
    if explicit:
        _maybe_warn_prefix(explicit)
        return explicit
    env = os.environ.get("TRELIS_API_KEY")
    if env:
        _maybe_warn_prefix(env)
        return env
    stored = keyring.get_password(KEYRING_SERVICE, KEYRING_USER)
    if stored:
        _maybe_warn_prefix(stored)
        return stored
    raise AuthError(
        "No Trelis API key found. Set TRELIS_API_KEY, run `trelis login`, "
        "or pass --api-key."
    )


def make_client(api_key: str | None = None) -> AuthenticatedClient:
    token = resolve_token(api_key)
    return AuthenticatedClient(base_url=base_url(), token=token)


def store_token(token: str) -> None:
    _maybe_warn_prefix(token)
    keyring.set_password(KEYRING_SERVICE, KEYRING_USER, token)


def clear_token() -> None:
    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_USER)
    except keyring.errors.PasswordDeleteError:
        pass

