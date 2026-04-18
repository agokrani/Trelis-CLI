from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.file_store_file_status_response import FileStoreFileStatusResponse
from ...models.http_validation_error import HTTPValidationError
from typing import cast


def _get_kwargs(
    store_id: str,
    filename: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/file-stores/{store_id}/files/{filename}/status".format(
            store_id=quote(str(store_id), safe=""),
            filename=quote(str(filename), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FileStoreFileStatusResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = FileStoreFileStatusResponse.from_dict(response.json())

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
) -> Response[FileStoreFileStatusResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    store_id: str,
    filename: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[FileStoreFileStatusResponse | HTTPValidationError]:
    """Get File Status

     Check whether an individual file exists in a FileStore (upload verification).

    For S3-backed stores, performs a HEAD request to confirm the file landed.

    Args:
        store_id (str):
        filename (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileStoreFileStatusResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        filename=filename,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    filename: str,
    *,
    client: AuthenticatedClient | Client,
) -> FileStoreFileStatusResponse | HTTPValidationError | None:
    """Get File Status

     Check whether an individual file exists in a FileStore (upload verification).

    For S3-backed stores, performs a HEAD request to confirm the file landed.

    Args:
        store_id (str):
        filename (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileStoreFileStatusResponse | HTTPValidationError
    """

    return sync_detailed(
        store_id=store_id,
        filename=filename,
        client=client,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    filename: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[FileStoreFileStatusResponse | HTTPValidationError]:
    """Get File Status

     Check whether an individual file exists in a FileStore (upload verification).

    For S3-backed stores, performs a HEAD request to confirm the file landed.

    Args:
        store_id (str):
        filename (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileStoreFileStatusResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        filename=filename,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    filename: str,
    *,
    client: AuthenticatedClient | Client,
) -> FileStoreFileStatusResponse | HTTPValidationError | None:
    """Get File Status

     Check whether an individual file exists in a FileStore (upload verification).

    For S3-backed stores, performs a HEAD request to confirm the file landed.

    Args:
        store_id (str):
        filename (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileStoreFileStatusResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            filename=filename,
            client=client,
        )
    ).parsed
