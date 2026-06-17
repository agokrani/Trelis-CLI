from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Unset
from typing import cast


def _get_kwargs(
    *,
    dataset_id: str,
    config: str | Unset = "default",
    split: str | Unset = "test",
    n: int | Unset = 5,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["dataset_id"] = dataset_id

    params["config"] = config

    params["split"] = split

    params["n"] = n

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/datasets/preview",
        "params": params,
    }

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
    dataset_id: str,
    config: str | Unset = "default",
    split: str | Unset = "test",
    n: int | Unset = 5,
) -> Response[Any | HTTPValidationError]:
    """Dataset Preview

     Preview rows from a HuggingFace dataset.

    Returns the first `n` rows from the specified dataset split.
    Useful for inspecting dataset contents without leaving the API workflow.
    Requires a HuggingFace token (set in Settings) for private datasets.

    Args:
        dataset_id (str): HuggingFace dataset ID (e.g., 'Trelis/ai-terms-public')
        config (str | Unset): Dataset config name Default: 'default'.
        split (str | Unset): Dataset split Default: 'test'.
        n (int | Unset): Number of rows to return Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        config=config,
        split=split,
        n=n,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    dataset_id: str,
    config: str | Unset = "default",
    split: str | Unset = "test",
    n: int | Unset = 5,
) -> Any | HTTPValidationError | None:
    """Dataset Preview

     Preview rows from a HuggingFace dataset.

    Returns the first `n` rows from the specified dataset split.
    Useful for inspecting dataset contents without leaving the API workflow.
    Requires a HuggingFace token (set in Settings) for private datasets.

    Args:
        dataset_id (str): HuggingFace dataset ID (e.g., 'Trelis/ai-terms-public')
        config (str | Unset): Dataset config name Default: 'default'.
        split (str | Unset): Dataset split Default: 'test'.
        n (int | Unset): Number of rows to return Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        dataset_id=dataset_id,
        config=config,
        split=split,
        n=n,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    dataset_id: str,
    config: str | Unset = "default",
    split: str | Unset = "test",
    n: int | Unset = 5,
) -> Response[Any | HTTPValidationError]:
    """Dataset Preview

     Preview rows from a HuggingFace dataset.

    Returns the first `n` rows from the specified dataset split.
    Useful for inspecting dataset contents without leaving the API workflow.
    Requires a HuggingFace token (set in Settings) for private datasets.

    Args:
        dataset_id (str): HuggingFace dataset ID (e.g., 'Trelis/ai-terms-public')
        config (str | Unset): Dataset config name Default: 'default'.
        split (str | Unset): Dataset split Default: 'test'.
        n (int | Unset): Number of rows to return Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        config=config,
        split=split,
        n=n,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    dataset_id: str,
    config: str | Unset = "default",
    split: str | Unset = "test",
    n: int | Unset = 5,
) -> Any | HTTPValidationError | None:
    """Dataset Preview

     Preview rows from a HuggingFace dataset.

    Returns the first `n` rows from the specified dataset split.
    Useful for inspecting dataset contents without leaving the API workflow.
    Requires a HuggingFace token (set in Settings) for private datasets.

    Args:
        dataset_id (str): HuggingFace dataset ID (e.g., 'Trelis/ai-terms-public')
        config (str | Unset): Dataset config name Default: 'default'.
        split (str | Unset): Dataset split Default: 'test'.
        n (int | Unset): Number of rows to return Default: 5.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            dataset_id=dataset_id,
            config=config,
            split=split,
            n=n,
        )
    ).parsed
