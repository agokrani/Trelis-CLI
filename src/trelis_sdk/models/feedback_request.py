from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.feedback_request_type import FeedbackRequestType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.feedback_request_context_type_0 import FeedbackRequestContextType0


T = TypeVar("T", bound="FeedbackRequest")


@_attrs_define
class FeedbackRequest:
    """Request to submit feedback.

    Attributes:
        type_ (FeedbackRequestType):
        title (None | str | Unset):
        description (None | str | Unset):
        message (None | str | Unset):
        context (FeedbackRequestContextType0 | None | Unset):
    """

    type_: FeedbackRequestType
    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    message: None | str | Unset = UNSET
    context: FeedbackRequestContextType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.feedback_request_context_type_0 import FeedbackRequestContextType0

        type_ = self.type_.value

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        message: None | str | Unset
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        context: dict[str, Any] | None | Unset
        if isinstance(self.context, Unset):
            context = UNSET
        elif isinstance(self.context, FeedbackRequestContextType0):
            context = self.context.to_dict()
        else:
            context = self.context

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if message is not UNSET:
            field_dict["message"] = message
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feedback_request_context_type_0 import FeedbackRequestContextType0

        d = dict(src_dict)
        type_ = FeedbackRequestType(d.pop("type"))

        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        message = _parse_message(d.pop("message", UNSET))

        def _parse_context(data: object) -> FeedbackRequestContextType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                context_type_0 = FeedbackRequestContextType0.from_dict(data)

                return context_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FeedbackRequestContextType0 | None | Unset, data)

        context = _parse_context(d.pop("context", UNSET))

        feedback_request = cls(
            type_=type_,
            title=title,
            description=description,
            message=message,
            context=context,
        )

        feedback_request.additional_properties = d
        return feedback_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
