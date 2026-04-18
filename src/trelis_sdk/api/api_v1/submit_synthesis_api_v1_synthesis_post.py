from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.synthesis_request import SynthesisRequest
from typing import cast


def _get_kwargs(
    *,
    body: SynthesisRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/synthesis",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SynthesisRequest,
) -> Response[Any | HTTPValidationError]:
    r"""Submit a v2 synthesis job

     Submit a v2 synthesis job (§5.4).

    Input is one of: inline text, HF dataset, or FileStore. Batch inputs are
    streamed in chunks (§5.8) — see PR #696 for the orchestrator-side pipeline.
    The result carries `content_type=\"generated_audio\"` with a §3.2 column
    manifest; when ``filter_threshold`` is set, kept/dropped/unscored sibling
    FileStores are linked via `extra_metadata.sibling_file_store_id` (each
    non-primary sibling points at the primary, per the kept > dropped >
    unscored priority).

    Args:
        body (SynthesisRequest): v2 synthesis request — one input source, params grouped per §5.4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
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
    body: SynthesisRequest,
) -> Any | HTTPValidationError | None:
    r"""Submit a v2 synthesis job

     Submit a v2 synthesis job (§5.4).

    Input is one of: inline text, HF dataset, or FileStore. Batch inputs are
    streamed in chunks (§5.8) — see PR #696 for the orchestrator-side pipeline.
    The result carries `content_type=\"generated_audio\"` with a §3.2 column
    manifest; when ``filter_threshold`` is set, kept/dropped/unscored sibling
    FileStores are linked via `extra_metadata.sibling_file_store_id` (each
    non-primary sibling points at the primary, per the kept > dropped >
    unscored priority).

    Args:
        body (SynthesisRequest): v2 synthesis request — one input source, params grouped per §5.4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SynthesisRequest,
) -> Response[Any | HTTPValidationError]:
    r"""Submit a v2 synthesis job

     Submit a v2 synthesis job (§5.4).

    Input is one of: inline text, HF dataset, or FileStore. Batch inputs are
    streamed in chunks (§5.8) — see PR #696 for the orchestrator-side pipeline.
    The result carries `content_type=\"generated_audio\"` with a §3.2 column
    manifest; when ``filter_threshold`` is set, kept/dropped/unscored sibling
    FileStores are linked via `extra_metadata.sibling_file_store_id` (each
    non-primary sibling points at the primary, per the kept > dropped >
    unscored priority).

    Args:
        body (SynthesisRequest): v2 synthesis request — one input source, params grouped per §5.4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: SynthesisRequest,
) -> Any | HTTPValidationError | None:
    r"""Submit a v2 synthesis job

     Submit a v2 synthesis job (§5.4).

    Input is one of: inline text, HF dataset, or FileStore. Batch inputs are
    streamed in chunks (§5.8) — see PR #696 for the orchestrator-side pipeline.
    The result carries `content_type=\"generated_audio\"` with a §3.2 column
    manifest; when ``filter_threshold`` is set, kept/dropped/unscored sibling
    FileStores are linked via `extra_metadata.sibling_file_store_id` (each
    non-primary sibling points at the primary, per the kept > dropped >
    unscored priority).

    Args:
        body (SynthesisRequest): v2 synthesis request — one input source, params grouped per §5.4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
