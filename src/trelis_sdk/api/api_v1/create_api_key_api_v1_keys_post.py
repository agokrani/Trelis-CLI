from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_key_request import CreateKeyRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.key_response import KeyResponse
from typing import cast


def _get_kwargs(
    *,
    body: CreateKeyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/keys",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | KeyResponse | None:
    if response.status_code == 200:
        response_200 = KeyResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | KeyResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateKeyRequest,
) -> Response[HTTPValidationError | KeyResponse]:
    """Create Api Key

     Create a new API key.

    The full key is only returned once on creation - store it securely.
    Keys use format: tsk_<32-byte-urlsafe-base64>

    Optionally attach a W&B API key — training jobs using this API key will
    use it instead of the user's account-level W&B token.

    Args:
        body (CreateKeyRequest): Request to create a new API key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | KeyResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: CreateKeyRequest,
) -> HTTPValidationError | KeyResponse | None:
    """Create Api Key

     Create a new API key.

    The full key is only returned once on creation - store it securely.
    Keys use format: tsk_<32-byte-urlsafe-base64>

    Optionally attach a W&B API key — training jobs using this API key will
    use it instead of the user's account-level W&B token.

    Args:
        body (CreateKeyRequest): Request to create a new API key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | KeyResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateKeyRequest,
) -> Response[HTTPValidationError | KeyResponse]:
    """Create Api Key

     Create a new API key.

    The full key is only returned once on creation - store it securely.
    Keys use format: tsk_<32-byte-urlsafe-base64>

    Optionally attach a W&B API key — training jobs using this API key will
    use it instead of the user's account-level W&B token.

    Args:
        body (CreateKeyRequest): Request to create a new API key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | KeyResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CreateKeyRequest,
) -> HTTPValidationError | KeyResponse | None:
    """Create Api Key

     Create a new API key.

    The full key is only returned once on creation - store it securely.
    Keys use format: tsk_<32-byte-urlsafe-base64>

    Optionally attach a W&B API key — training jobs using this API key will
    use it instead of the user's account-level W&B token.

    Args:
        body (CreateKeyRequest): Request to create a new API key.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | KeyResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
