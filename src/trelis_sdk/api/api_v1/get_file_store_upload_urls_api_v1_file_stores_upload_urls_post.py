from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.file_store_batch_upload_request import FileStoreBatchUploadRequest
from ...models.file_store_batch_upload_url_response import FileStoreBatchUploadUrlResponse
from ...models.http_validation_error import HTTPValidationError
from typing import cast


def _get_kwargs(
    *,
    body: FileStoreBatchUploadRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/file-stores/upload-urls",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FileStoreBatchUploadUrlResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = FileStoreBatchUploadUrlResponse.from_dict(response.json())

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
) -> Response[FileStoreBatchUploadUrlResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: FileStoreBatchUploadRequest,
) -> Response[FileStoreBatchUploadUrlResponse | HTTPValidationError]:
    """Get File Store Upload Urls

     Get presigned PUT URLs for multiple files in one call (up to 5000).

    Returns the same `file_store_id` for all files — they all land in the
    same FileStore. Pass `file_store_id` to append to an existing store.

    The `content_type` in each response entry **must** be sent as the
    `Content-Type` header on the corresponding PUT request.

    Args:
        body (FileStoreBatchUploadRequest): Batch request for FileStore presigned upload URLs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileStoreBatchUploadUrlResponse | HTTPValidationError]
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
    body: FileStoreBatchUploadRequest,
) -> FileStoreBatchUploadUrlResponse | HTTPValidationError | None:
    """Get File Store Upload Urls

     Get presigned PUT URLs for multiple files in one call (up to 5000).

    Returns the same `file_store_id` for all files — they all land in the
    same FileStore. Pass `file_store_id` to append to an existing store.

    The `content_type` in each response entry **must** be sent as the
    `Content-Type` header on the corresponding PUT request.

    Args:
        body (FileStoreBatchUploadRequest): Batch request for FileStore presigned upload URLs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileStoreBatchUploadUrlResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: FileStoreBatchUploadRequest,
) -> Response[FileStoreBatchUploadUrlResponse | HTTPValidationError]:
    """Get File Store Upload Urls

     Get presigned PUT URLs for multiple files in one call (up to 5000).

    Returns the same `file_store_id` for all files — they all land in the
    same FileStore. Pass `file_store_id` to append to an existing store.

    The `content_type` in each response entry **must** be sent as the
    `Content-Type` header on the corresponding PUT request.

    Args:
        body (FileStoreBatchUploadRequest): Batch request for FileStore presigned upload URLs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FileStoreBatchUploadUrlResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: FileStoreBatchUploadRequest,
) -> FileStoreBatchUploadUrlResponse | HTTPValidationError | None:
    """Get File Store Upload Urls

     Get presigned PUT URLs for multiple files in one call (up to 5000).

    Returns the same `file_store_id` for all files — they all land in the
    same FileStore. Pass `file_store_id` to append to an existing store.

    The `content_type` in each response entry **must** be sent as the
    `Content-Type` header on the corresponding PUT request.

    Args:
        body (FileStoreBatchUploadRequest): Batch request for FileStore presigned upload URLs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FileStoreBatchUploadUrlResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
