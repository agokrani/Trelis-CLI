"""Credential resolution and AuthenticatedClient construction.

Resolution order:
    1. Explicit `--api-key` flag (passed in by the command)
    2. `TRELIS_API_KEY` env var
    3. keyring (service=trelis-cli, user=default)

The upstream OpenAPI spec declares no security scheme; our overlay.yaml
patches in `BearerAuth`. The generated `AuthenticatedClient` accepts a
`token` kwarg and prepends `Bearer `.
"""

from __future__ import annotations

import os

import keyring

from trelis_sdk import AuthenticatedClient

from .config import KEYRING_SERVICE, KEYRING_USER, base_url
from .errors import AuthError


def resolve_token(explicit: str | None = None) -> str:
    if explicit:
        return explicit
    env = os.environ.get("TRELIS_API_KEY")
    if env:
        return env
    stored = keyring.get_password(KEYRING_SERVICE, KEYRING_USER)
    if stored:
        return stored
    raise AuthError(
        "No Trelis API key found. Set TRELIS_API_KEY, run `trelis login`, "
        "or pass --api-key."
    )


def make_client(api_key: str | None = None) -> AuthenticatedClient:
    token = resolve_token(api_key)
    return AuthenticatedClient(base_url=base_url(), token=token)


def store_token(token: str) -> None:
    keyring.set_password(KEYRING_SERVICE, KEYRING_USER, token)


def clear_token() -> None:
    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_USER)
    except keyring.errors.PasswordDeleteError:
        pass
