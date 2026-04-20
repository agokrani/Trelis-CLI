from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.file_store_transcript_response import FileStoreTranscriptResponse
from ...models.http_validation_error import HTTPValidationError
from typing import cast


def _get_kwargs(
    store_id: str,
    stem: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/file-stores/{store_id}/transcripts/{stem}".format(
            store_id=quote(str(store_id), safe=""),
            stem=quote(str(stem), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FileStoreTranscriptResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = FileStoreTranscriptResponse.from_dict(response.json())

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
) -> Response[FileStoreTranscriptResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    store_id: str,
    stem: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[FileStoreTranscriptResponse | HTTPValidationError]:
    """Get transcript content + paired audio URL for a file

     Return the VTT/TXT body paired with a stem, plus a short-lived audio
    GET URL the editor can point an ``<audio>`` element at.

    Args:
        store_id (str):
        stem (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileStoreTranscriptResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        stem=stem,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    stem: str,
    *,
    client: AuthenticatedClient | Client,
) -> FileStoreTranscriptResponse | HTTPValidationError | None:
    """Get transcript content + paired audio URL for a file

     Return the VTT/TXT body paired with a stem, plus a short-lived audio
    GET URL the editor can point an ``<audio>`` element at.

    Args:
        store_id (str):
        stem (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileStoreTranscriptResponse | HTTPValidationError
    """

    return sync_detailed(
        store_id=store_id,
        stem=stem,
        client=client,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    stem: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[FileStoreTranscriptResponse | HTTPValidationError]:
    """Get transcript content + paired audio URL for a file

     Return the VTT/TXT body paired with a stem, plus a short-lived audio
    GET URL the editor can point an ``<audio>`` element at.

    Args:
        store_id (str):
        stem (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileStoreTranscriptResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        stem=stem,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    stem: str,
    *,
    client: AuthenticatedClient | Client,
) -> FileStoreTranscriptResponse | HTTPValidationError | None:
    """Get transcript content + paired audio URL for a file

     Return the VTT/TXT body paired with a stem, plus a short-lived audio
    GET URL the editor can point an ``<audio>`` element at.

    Args:
        store_id (str):
        stem (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileStoreTranscriptResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            stem=stem,
            client=client,
        )
    ).parsed
