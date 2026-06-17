from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.job_response import JobResponse
from ...models.transcription_request import TranscriptionRequest
from typing import cast


def _get_kwargs(
    *,
    body: TranscriptionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/transcription",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | JobResponse | None:
    if response.status_code == 200:
        response_200 = JobResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | JobResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: TranscriptionRequest,
) -> Response[HTTPValidationError | JobResponse]:
    """Submit a v2 transcription job

     Submit a v2 Transcription job (§4.6).

    Stage 1: authentication (``require_api_key``) + credits + concurrency
             + credential resolution + S3 config.
    Stage 2: input validation via ``resolve_input_source`` (§3.2 contract
             check + FileStore ownership scoping + HF dataset features
             probe).
    Stage 3: pre-mint ``job_id`` + commit ``Job`` row (credentials
             EXCLUDED) + ``background_tasks.add_task`` with the
             ephemeral credentials dict.

    Args:
        body (TranscriptionRequest): POST /api/v1/transcription request body (§4.6).

            Required: ``model_id``, ``language``.
            Exactly one input source: ``dataset_id``, ``parquet_urls``, or
            ``file_store_id``.

            Project-scoped parameters — NEVER in the request body per §4.6:
            ``hf_token``, ``router_api_key``, ``s3_config``, ``output_target``.
            Those arrive via the project's stored credentials + settings; a
            request body that tries to override them is rejected by the
            strict (``extra="forbid"``) config below.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | JobResponse]
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
    body: TranscriptionRequest,
) -> HTTPValidationError | JobResponse | None:
    """Submit a v2 transcription job

     Submit a v2 Transcription job (§4.6).

    Stage 1: authentication (``require_api_key``) + credits + concurrency
             + credential resolution + S3 config.
    Stage 2: input validation via ``resolve_input_source`` (§3.2 contract
             check + FileStore ownership scoping + HF dataset features
             probe).
    Stage 3: pre-mint ``job_id`` + commit ``Job`` row (credentials
             EXCLUDED) + ``background_tasks.add_task`` with the
             ephemeral credentials dict.

    Args:
        body (TranscriptionRequest): POST /api/v1/transcription request body (§4.6).

            Required: ``model_id``, ``language``.
            Exactly one input source: ``dataset_id``, ``parquet_urls``, or
            ``file_store_id``.

            Project-scoped parameters — NEVER in the request body per §4.6:
            ``hf_token``, ``router_api_key``, ``s3_config``, ``output_target``.
            Those arrive via the project's stored credentials + settings; a
            request body that tries to override them is rejected by the
            strict (``extra="forbid"``) config below.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | JobResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: TranscriptionRequest,
) -> Response[HTTPValidationError | JobResponse]:
    """Submit a v2 transcription job

     Submit a v2 Transcription job (§4.6).

    Stage 1: authentication (``require_api_key``) + credits + concurrency
             + credential resolution + S3 config.
    Stage 2: input validation via ``resolve_input_source`` (§3.2 contract
             check + FileStore ownership scoping + HF dataset features
             probe).
    Stage 3: pre-mint ``job_id`` + commit ``Job`` row (credentials
             EXCLUDED) + ``background_tasks.add_task`` with the
             ephemeral credentials dict.

    Args:
        body (TranscriptionRequest): POST /api/v1/transcription request body (§4.6).

            Required: ``model_id``, ``language``.
            Exactly one input source: ``dataset_id``, ``parquet_urls``, or
            ``file_store_id``.

            Project-scoped parameters — NEVER in the request body per §4.6:
            ``hf_token``, ``router_api_key``, ``s3_config``, ``output_target``.
            Those arrive via the project's stored credentials + settings; a
            request body that tries to override them is rejected by the
            strict (``extra="forbid"``) config below.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | JobResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: TranscriptionRequest,
) -> HTTPValidationError | JobResponse | None:
    """Submit a v2 transcription job

     Submit a v2 Transcription job (§4.6).

    Stage 1: authentication (``require_api_key``) + credits + concurrency
             + credential resolution + S3 config.
    Stage 2: input validation via ``resolve_input_source`` (§3.2 contract
             check + FileStore ownership scoping + HF dataset features
             probe).
    Stage 3: pre-mint ``job_id`` + commit ``Job`` row (credentials
             EXCLUDED) + ``background_tasks.add_task`` with the
             ephemeral credentials dict.

    Args:
        body (TranscriptionRequest): POST /api/v1/transcription request body (§4.6).

            Required: ``model_id``, ``language``.
            Exactly one input source: ``dataset_id``, ``parquet_urls``, or
            ``file_store_id``.

            Project-scoped parameters — NEVER in the request body per §4.6:
            ``hf_token``, ``router_api_key``, ``s3_config``, ``output_target``.
            Those arrive via the project's stored credentials + settings; a
            request body that tries to override them is rejected by the
            strict (``extra="forbid"``) config below.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | JobResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
