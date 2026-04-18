from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.file_store_draft_transcribe_request import FileStoreDraftTranscribeRequest
from ...models.http_validation_error import HTTPValidationError
from typing import cast


def _get_kwargs(
    store_id: str,
    *,
    body: FileStoreDraftTranscribeRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/file-stores/{store_id}/draft-transcribe".format(
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
    body: FileStoreDraftTranscribeRequest,
) -> Response[Any | HTTPValidationError]:
    r"""Draft Transcribe File Store

     Transcribe audio files in a FileStore using ASR.

    Input FileStore must be S3-backed (source: upload). Creates a new output
    FileStore (source: draft_transcribe, storage_backend: s3) containing
    audio + VTT file pairs ready for `POST /file-stores/{id}/process`.

    Use `model_id: \"router\"` + `router_model` for CPU-based transcription
    via the Trelis Router, or a Studio model ID for GPU transcription.

    Poll `GET /api/v1/data-prep/jobs/{job_id}` for progress.

    Args:
        store_id (str):
        body (FileStoreDraftTranscribeRequest):

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
    body: FileStoreDraftTranscribeRequest,
) -> Any | HTTPValidationError | None:
    r"""Draft Transcribe File Store

     Transcribe audio files in a FileStore using ASR.

    Input FileStore must be S3-backed (source: upload). Creates a new output
    FileStore (source: draft_transcribe, storage_backend: s3) containing
    audio + VTT file pairs ready for `POST /file-stores/{id}/process`.

    Use `model_id: \"router\"` + `router_model` for CPU-based transcription
    via the Trelis Router, or a Studio model ID for GPU transcription.

    Poll `GET /api/v1/data-prep/jobs/{job_id}` for progress.

    Args:
        store_id (str):
        body (FileStoreDraftTranscribeRequest):

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
    body: FileStoreDraftTranscribeRequest,
) -> Response[Any | HTTPValidationError]:
    r"""Draft Transcribe File Store

     Transcribe audio files in a FileStore using ASR.

    Input FileStore must be S3-backed (source: upload). Creates a new output
    FileStore (source: draft_transcribe, storage_backend: s3) containing
    audio + VTT file pairs ready for `POST /file-stores/{id}/process`.

    Use `model_id: \"router\"` + `router_model` for CPU-based transcription
    via the Trelis Router, or a Studio model ID for GPU transcription.

    Poll `GET /api/v1/data-prep/jobs/{job_id}` for progress.

    Args:
        store_id (str):
        body (FileStoreDraftTranscribeRequest):

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
    body: FileStoreDraftTranscribeRequest,
) -> Any | HTTPValidationError | None:
    r"""Draft Transcribe File Store

     Transcribe audio files in a FileStore using ASR.

    Input FileStore must be S3-backed (source: upload). Creates a new output
    FileStore (source: draft_transcribe, storage_backend: s3) containing
    audio + VTT file pairs ready for `POST /file-stores/{id}/process`.

    Use `model_id: \"router\"` + `router_model` for CPU-based transcription
    via the Trelis Router, or a Studio model ID for GPU transcription.

    Poll `GET /api/v1/data-prep/jobs/{job_id}` for progress.

    Args:
        store_id (str):
        body (FileStoreDraftTranscribeRequest):

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
