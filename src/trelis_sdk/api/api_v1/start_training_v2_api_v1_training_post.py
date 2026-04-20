from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.training_asrv2_request import TrainingASRV2Request
from ...models.training_ttsv2_request import TrainingTTSV2Request
from typing import cast


def _get_kwargs(
    *,
    body: TrainingASRV2Request | TrainingTTSV2Request,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/training",
    }

    if isinstance(body, TrainingASRV2Request):
        _kwargs["json"] = body.to_dict()
    else:
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
    body: TrainingASRV2Request | TrainingTTSV2Request,
) -> Response[Any | HTTPValidationError]:
    """Submit a v2 training job (ASR or TTS)

     Submit a v2 training job (§11 + #685 Phase 5).

    Unified endpoint for ASR + TTS. ``job_type`` discriminates; ASR
    dispatches to ``start_training`` (5 backends: whisper / moonshine /
    voxtral / qwen / parakeet). TTS dispatches to ``start_tts_training``
    for single-GPU runs and ``start_tts_training_ddp`` when
    ``num_gpus > 1`` (absorption decision A on #685 — formerly the
    DDP variants required posting to ``/api/v1/tts-training-ddp/jobs``
    directly). The DDP route is kept live for API back-compat but
    the v2 endpoint is now the canonical way to submit DDP jobs.

    v2 delta over the legacy ``/api/v1/training/jobs`` +
    ``/api/v1/tts-training/jobs`` routes:

    - FileStore inputs are contract-validated (§3.2) against the
      training service contract BEFORE the Job row is minted.
      Bad ``content_type`` or missing required columns (``audio``,
      ``text``) return 400 here — no wasted Modal spin-up.
    - Consistent response envelope: whatever the legacy handler
      returned (``{job_id, status, message, ...}``) plus ``v2: True``.
      The ``balance`` key is included when the legacy handler returns
      it (i.e. when credits are decremented on job creation); callers
      should treat it as optional.

    Args:
        body (TrainingASRV2Request | TrainingTTSV2Request):

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
    body: TrainingASRV2Request | TrainingTTSV2Request,
) -> Any | HTTPValidationError | None:
    """Submit a v2 training job (ASR or TTS)

     Submit a v2 training job (§11 + #685 Phase 5).

    Unified endpoint for ASR + TTS. ``job_type`` discriminates; ASR
    dispatches to ``start_training`` (5 backends: whisper / moonshine /
    voxtral / qwen / parakeet). TTS dispatches to ``start_tts_training``
    for single-GPU runs and ``start_tts_training_ddp`` when
    ``num_gpus > 1`` (absorption decision A on #685 — formerly the
    DDP variants required posting to ``/api/v1/tts-training-ddp/jobs``
    directly). The DDP route is kept live for API back-compat but
    the v2 endpoint is now the canonical way to submit DDP jobs.

    v2 delta over the legacy ``/api/v1/training/jobs`` +
    ``/api/v1/tts-training/jobs`` routes:

    - FileStore inputs are contract-validated (§3.2) against the
      training service contract BEFORE the Job row is minted.
      Bad ``content_type`` or missing required columns (``audio``,
      ``text``) return 400 here — no wasted Modal spin-up.
    - Consistent response envelope: whatever the legacy handler
      returned (``{job_id, status, message, ...}``) plus ``v2: True``.
      The ``balance`` key is included when the legacy handler returns
      it (i.e. when credits are decremented on job creation); callers
      should treat it as optional.

    Args:
        body (TrainingASRV2Request | TrainingTTSV2Request):

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
    body: TrainingASRV2Request | TrainingTTSV2Request,
) -> Response[Any | HTTPValidationError]:
    """Submit a v2 training job (ASR or TTS)

     Submit a v2 training job (§11 + #685 Phase 5).

    Unified endpoint for ASR + TTS. ``job_type`` discriminates; ASR
    dispatches to ``start_training`` (5 backends: whisper / moonshine /
    voxtral / qwen / parakeet). TTS dispatches to ``start_tts_training``
    for single-GPU runs and ``start_tts_training_ddp`` when
    ``num_gpus > 1`` (absorption decision A on #685 — formerly the
    DDP variants required posting to ``/api/v1/tts-training-ddp/jobs``
    directly). The DDP route is kept live for API back-compat but
    the v2 endpoint is now the canonical way to submit DDP jobs.

    v2 delta over the legacy ``/api/v1/training/jobs`` +
    ``/api/v1/tts-training/jobs`` routes:

    - FileStore inputs are contract-validated (§3.2) against the
      training service contract BEFORE the Job row is minted.
      Bad ``content_type`` or missing required columns (``audio``,
      ``text``) return 400 here — no wasted Modal spin-up.
    - Consistent response envelope: whatever the legacy handler
      returned (``{job_id, status, message, ...}``) plus ``v2: True``.
      The ``balance`` key is included when the legacy handler returns
      it (i.e. when credits are decremented on job creation); callers
      should treat it as optional.

    Args:
        body (TrainingASRV2Request | TrainingTTSV2Request):

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
    body: TrainingASRV2Request | TrainingTTSV2Request,
) -> Any | HTTPValidationError | None:
    """Submit a v2 training job (ASR or TTS)

     Submit a v2 training job (§11 + #685 Phase 5).

    Unified endpoint for ASR + TTS. ``job_type`` discriminates; ASR
    dispatches to ``start_training`` (5 backends: whisper / moonshine /
    voxtral / qwen / parakeet). TTS dispatches to ``start_tts_training``
    for single-GPU runs and ``start_tts_training_ddp`` when
    ``num_gpus > 1`` (absorption decision A on #685 — formerly the
    DDP variants required posting to ``/api/v1/tts-training-ddp/jobs``
    directly). The DDP route is kept live for API back-compat but
    the v2 endpoint is now the canonical way to submit DDP jobs.

    v2 delta over the legacy ``/api/v1/training/jobs`` +
    ``/api/v1/tts-training/jobs`` routes:

    - FileStore inputs are contract-validated (§3.2) against the
      training service contract BEFORE the Job row is minted.
      Bad ``content_type`` or missing required columns (``audio``,
      ``text``) return 400 here — no wasted Modal spin-up.
    - Consistent response envelope: whatever the legacy handler
      returned (``{job_id, status, message, ...}``) plus ``v2: True``.
      The ``balance`` key is included when the legacy handler returns
      it (i.e. when credits are decremented on job creation); callers
      should treat it as optional.

    Args:
        body (TrainingASRV2Request | TrainingTTSV2Request):

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
