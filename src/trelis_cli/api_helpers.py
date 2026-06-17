"""Bridge between the generated SDK and the CLI.

The Trelis spec leaves 92% of `2xx` responses as `schema: {}`, which OPC
parses to `None` and discards the body. We bypass OPC's `_parse_response`
by always calling `sync_detailed`/`asyncio_detailed` and reading
`Response.content` ourselves.

Use `call_json(operation_module, client=..., **op_kwargs)` for any
operation. It returns a parsed dict (or list, depending on the endpoint).
"""

from __future__ import annotations

import json
from typing import Any

from trelis_sdk import AuthenticatedClient, Client

from .errors import APIError, AuthError


def call_json(operation_module: Any, *, client: Client | AuthenticatedClient, **kwargs: Any) -> Any:
    """Invoke `operation_module.sync_detailed(client=..., **kwargs)` and parse JSON."""
    response = operation_module.sync_detailed(client=client, **kwargs)
    status = int(response.status_code)
    body = response.content

    if 200 <= status < 300:
        if not body:
            return None
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return body.decode("utf-8", errors="replace")

    if status in (401, 403):
        raise AuthError(_extract_message(body) or f"Unauthorized ({status})")

    raise APIError(_extract_message(body) or f"API returned {status}", status_code=status)


def _extract_message(body: bytes) -> str | None:
    if not body:
        return None
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return body.decode("utf-8", errors="replace").strip() or None
    if isinstance(data, dict):
        for key in ("detail", "message", "error"):
            value = data.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, list) and value:
                return "; ".join(str(item) for item in value)
    return json.dumps(data)
