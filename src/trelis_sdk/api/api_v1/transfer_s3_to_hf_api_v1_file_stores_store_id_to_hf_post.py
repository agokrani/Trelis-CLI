from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.transfer_s3_to_hf_request import TransferS3ToHfRequest
from typing import cast


def _get_kwargs(
    store_id: str,
    *,
    body: TransferS3ToHfRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/file-stores/{store_id}/to-hf".format(
            store_id=quote(str(store_id), safe=""),
        ),
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
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TransferS3ToHfRequest,
) -> Response[Any | HTTPValidationError]:
    """Transfer S3 To Hf

     Push an S3-backed FileStore to a HuggingFace repo.

    Requires: project has HuggingFace output enabled and a valid HF token.
    Always pushes as private.

    Poll `GET /api/v1/data-prep/jobs/{job_id}` for progress.

    Args:
        store_id (str):
        body (TransferS3ToHfRequest): Push an S3 FileStore to a HuggingFace repo.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TransferS3ToHfRequest,
) -> Any | HTTPValidationError | None:
    """Transfer S3 To Hf

     Push an S3-backed FileStore to a HuggingFace repo.

    Requires: project has HuggingFace output enabled and a valid HF token.
    Always pushes as private.

    Poll `GET /api/v1/data-prep/jobs/{job_id}` for progress.

    Args:
        store_id (str):
        body (TransferS3ToHfRequest): Push an S3 FileStore to a HuggingFace repo.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TransferS3ToHfRequest,
) -> Response[Any | HTTPValidationError]:
    """Transfer S3 To Hf

     Push an S3-backed FileStore to a HuggingFace repo.

    Requires: project has HuggingFace output enabled and a valid HF token.
    Always pushes as private.

    Poll `GET /api/v1/data-prep/jobs/{job_id}` for progress.

    Args:
        store_id (str):
        body (TransferS3ToHfRequest): Push an S3 FileStore to a HuggingFace repo.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TransferS3ToHfRequest,
) -> Any | HTTPValidationError | None:
    """Transfer S3 To Hf

     Push an S3-backed FileStore to a HuggingFace repo.

    Requires: project has HuggingFace output enabled and a valid HF token.
    Always pushes as private.

    Poll `GET /api/v1/data-prep/jobs/{job_id}` for progress.

    Args:
        store_id (str):
        body (TransferS3ToHfRequest): Push an S3 FileStore to a HuggingFace repo.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            client=client,
            body=body,
        )
    ).parsed
