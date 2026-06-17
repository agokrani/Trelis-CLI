from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="CreateUserRequest")


@_attrs_define
class CreateUserRequest:
    """
    Attributes:
        email (str):
        nickname (None | str | Unset):
        initial_credits (float | Unset):  Default: 0.0.
        invite_to_project_id (None | str | Unset):
        invite_role (str | Unset):  Default: 'member'.
    """

    email: str
    nickname: None | str | Unset = UNSET
    initial_credits: float | Unset = 0.0
    invite_to_project_id: None | str | Unset = UNSET
    invite_role: str | Unset = "member"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        nickname: None | str | Unset
        if isinstance(self.nickname, Unset):
            nickname = UNSET
        else:
            nickname = self.nickname

        initial_credits = self.initial_credits

        invite_to_project_id: None | str | Unset
        if isinstance(self.invite_to_project_id, Unset):
            invite_to_project_id = UNSET
        else:
            invite_to_project_id = self.invite_to_project_id

        invite_role = self.invite_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
            }
        )
        if nickname is not UNSET:
            field_dict["nickname"] = nickname
        if initial_credits is not UNSET:
            field_dict["initial_credits"] = initial_credits
        if invite_to_project_id is not UNSET:
            field_dict["invite_to_project_id"] = invite_to_project_id
        if invite_role is not UNSET:
            field_dict["invite_role"] = invite_role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        def _parse_nickname(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        nickname = _parse_nickname(d.pop("nickname", UNSET))

        initial_credits = d.pop("initial_credits", UNSET)

        def _parse_invite_to_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        invite_to_project_id = _parse_invite_to_project_id(d.pop("invite_to_project_id", UNSET))

        invite_role = d.pop("invite_role", UNSET)

        create_user_request = cls(
            email=email,
            nickname=nickname,
            initial_credits=initial_credits,
            invite_to_project_id=invite_to_project_id,
            invite_role=invite_role,
        )

        create_user_request.additional_properties = d
        return create_user_request

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
