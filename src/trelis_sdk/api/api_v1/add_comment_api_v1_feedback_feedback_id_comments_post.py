from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.comment_request import CommentRequest
from ...models.http_validation_error import HTTPValidationError
from typing import cast


def _get_kwargs(
    feedback_id: str,
    *,
    body: CommentRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/feedback/{feedback_id}/comments".format(
            feedback_id=quote(str(feedback_id), safe=""),
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
    feedback_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CommentRequest,
) -> Response[Any | HTTPValidationError]:
    """Add Comment

     Add a comment to a feedback post (admin only).

    Use this to respond to user feedback or add internal notes.

    Args:
        feedback_id (str):
        body (CommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        feedback_id=feedback_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    feedback_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CommentRequest,
) -> Any | HTTPValidationError | None:
    """Add Comment

     Add a comment to a feedback post (admin only).

    Use this to respond to user feedback or add internal notes.

    Args:
        feedback_id (str):
        body (CommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        feedback_id=feedback_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    feedback_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CommentRequest,
) -> Response[Any | HTTPValidationError]:
    """Add Comment

     Add a comment to a feedback post (admin only).

    Use this to respond to user feedback or add internal notes.

    Args:
        feedback_id (str):
        body (CommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        feedback_id=feedback_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    feedback_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CommentRequest,
) -> Any | HTTPValidationError | None:
    """Add Comment

     Add a comment to a feedback post (admin only).

    Use this to respond to user feedback or add internal notes.

    Args:
        feedback_id (str):
        body (CommentRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            feedback_id=feedback_id,
            client=client,
            body=body,
        )
    ).parsed
