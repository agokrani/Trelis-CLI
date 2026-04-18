from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.body_upload_parquet_to_file_store_api_v1_file_stores_upload_parquet_post import (
    BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.parquet_upload_response import ParquetUploadResponse
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    body: BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost,
    name: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_name: None | str | Unset
    if isinstance(name, Unset):
        json_name = UNSET
    else:
        json_name = name
    params["name"] = json_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/file-stores/upload-parquet",
        "params": params,
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ParquetUploadResponse | None:
    if response.status_code == 200:
        response_200 = ParquetUploadResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ParquetUploadResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost,
    name: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ParquetUploadResponse]:
    """Upload Parquet To File Store

     Upload a .parquet file and create a project-scoped FileStore.

    The parquet is stored at the standard FileStore layout
    (`file-stores/{id}/files/data/train-00000-of-00001.parquet`) and a
    `dataset_info.json` sidecar is generated with column schema and row count.

    The resulting FileStore is reusable as input to any pipeline
    (evaluation, training, filtering, data prep) — same as an HF-imported
    FileStore.

    Args:
        name (None | str | Unset):
        body (BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ParquetUploadResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        name=name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost,
    name: None | str | Unset = UNSET,
) -> HTTPValidationError | ParquetUploadResponse | None:
    """Upload Parquet To File Store

     Upload a .parquet file and create a project-scoped FileStore.

    The parquet is stored at the standard FileStore layout
    (`file-stores/{id}/files/data/train-00000-of-00001.parquet`) and a
    `dataset_info.json` sidecar is generated with column schema and row count.

    The resulting FileStore is reusable as input to any pipeline
    (evaluation, training, filtering, data prep) — same as an HF-imported
    FileStore.

    Args:
        name (None | str | Unset):
        body (BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ParquetUploadResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        name=name,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost,
    name: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ParquetUploadResponse]:
    """Upload Parquet To File Store

     Upload a .parquet file and create a project-scoped FileStore.

    The parquet is stored at the standard FileStore layout
    (`file-stores/{id}/files/data/train-00000-of-00001.parquet`) and a
    `dataset_info.json` sidecar is generated with column schema and row count.

    The resulting FileStore is reusable as input to any pipeline
    (evaluation, training, filtering, data prep) — same as an HF-imported
    FileStore.

    Args:
        name (None | str | Unset):
        body (BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ParquetUploadResponse]
    """

    kwargs = _get_kwargs(
        body=body,
        name=name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost,
    name: None | str | Unset = UNSET,
) -> HTTPValidationError | ParquetUploadResponse | None:
    """Upload Parquet To File Store

     Upload a .parquet file and create a project-scoped FileStore.

    The parquet is stored at the standard FileStore layout
    (`file-stores/{id}/files/data/train-00000-of-00001.parquet`) and a
    `dataset_info.json` sidecar is generated with column schema and row count.

    The resulting FileStore is reusable as input to any pipeline
    (evaluation, training, filtering, data prep) — same as an HF-imported
    FileStore.

    Args:
        name (None | str | Unset):
        body (BodyUploadParquetToFileStoreApiV1FileStoresUploadParquetPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ParquetUploadResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            name=name,
        )
    ).parsed
