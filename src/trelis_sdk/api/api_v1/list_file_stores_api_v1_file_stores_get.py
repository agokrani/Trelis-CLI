from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.file_store_list_response import FileStoreListResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    hide_empty: bool | Unset = True,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    search: str | Unset = "",
    sort: str | Unset = "newest",
    content_type: str | Unset = "",
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["hide_empty"] = hide_empty

    params["limit"] = limit

    params["offset"] = offset

    params["search"] = search

    params["sort"] = sort

    params["content_type"] = content_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/file-stores",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FileStoreListResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = FileStoreListResponse.from_dict(response.json())

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
) -> Response[FileStoreListResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    hide_empty: bool | Unset = True,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    search: str | Unset = "",
    sort: str | Unset = "newest",
    content_type: str | Unset = "",
) -> Response[FileStoreListResponse | HTTPValidationError]:
    """List File Stores

     List all active file stores for the current user, scoped to project.

    Args:
        hide_empty (bool | Unset): Hide file stores with zero files Default: True.
        limit (int | Unset): Max items to return (0 = all) Default: 20.
        offset (int | Unset): Items to skip Default: 0.
        search (str | Unset): Filter by name (case-insensitive substring match) Default: ''.
        sort (str | Unset): Sort order: newest, oldest, name Default: 'newest'.
        content_type (str | Unset): Filter by v2 ContentType enum value or comma-separated list
            (e.g. 'trained_model' or 'audio_text_pairs,generated_audio') Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileStoreListResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        hide_empty=hide_empty,
        limit=limit,
        offset=offset,
        search=search,
        sort=sort,
        content_type=content_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    hide_empty: bool | Unset = True,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    search: str | Unset = "",
    sort: str | Unset = "newest",
    content_type: str | Unset = "",
) -> FileStoreListResponse | HTTPValidationError | None:
    """List File Stores

     List all active file stores for the current user, scoped to project.

    Args:
        hide_empty (bool | Unset): Hide file stores with zero files Default: True.
        limit (int | Unset): Max items to return (0 = all) Default: 20.
        offset (int | Unset): Items to skip Default: 0.
        search (str | Unset): Filter by name (case-insensitive substring match) Default: ''.
        sort (str | Unset): Sort order: newest, oldest, name Default: 'newest'.
        content_type (str | Unset): Filter by v2 ContentType enum value or comma-separated list
            (e.g. 'trained_model' or 'audio_text_pairs,generated_audio') Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileStoreListResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        hide_empty=hide_empty,
        limit=limit,
        offset=offset,
        search=search,
        sort=sort,
        content_type=content_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    hide_empty: bool | Unset = True,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    search: str | Unset = "",
    sort: str | Unset = "newest",
    content_type: str | Unset = "",
) -> Response[FileStoreListResponse | HTTPValidationError]:
    """List File Stores

     List all active file stores for the current user, scoped to project.

    Args:
        hide_empty (bool | Unset): Hide file stores with zero files Default: True.
        limit (int | Unset): Max items to return (0 = all) Default: 20.
        offset (int | Unset): Items to skip Default: 0.
        search (str | Unset): Filter by name (case-insensitive substring match) Default: ''.
        sort (str | Unset): Sort order: newest, oldest, name Default: 'newest'.
        content_type (str | Unset): Filter by v2 ContentType enum value or comma-separated list
            (e.g. 'trained_model' or 'audio_text_pairs,generated_audio') Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileStoreListResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        hide_empty=hide_empty,
        limit=limit,
        offset=offset,
        search=search,
        sort=sort,
        content_type=content_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    hide_empty: bool | Unset = True,
    limit: int | Unset = 20,
    offset: int | Unset = 0,
    search: str | Unset = "",
    sort: str | Unset = "newest",
    content_type: str | Unset = "",
) -> FileStoreListResponse | HTTPValidationError | None:
    """List File Stores

     List all active file stores for the current user, scoped to project.

    Args:
        hide_empty (bool | Unset): Hide file stores with zero files Default: True.
        limit (int | Unset): Max items to return (0 = all) Default: 20.
        offset (int | Unset): Items to skip Default: 0.
        search (str | Unset): Filter by name (case-insensitive substring match) Default: ''.
        sort (str | Unset): Sort order: newest, oldest, name Default: 'newest'.
        content_type (str | Unset): Filter by v2 ContentType enum value or comma-separated list
            (e.g. 'trained_model' or 'audio_text_pairs,generated_audio') Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileStoreListResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            hide_empty=hide_empty,
            limit=limit,
            offset=offset,
            search=search,
            sort=sort,
            content_type=content_type,
        )
    ).parsed
