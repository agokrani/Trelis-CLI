from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="UpdateKeyRequest")


@_attrs_define
class UpdateKeyRequest:
    """Request to update an API key's spend limit.

    Attributes:
        spend_limit (float | None | Unset):
        wandb_api_key (None | str | Unset):
    """

    spend_limit: float | None | Unset = UNSET
    wandb_api_key: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        spend_limit: float | None | Unset
        if isinstance(self.spend_limit, Unset):
            spend_limit = UNSET
        else:
            spend_limit = self.spend_limit

        wandb_api_key: None | str | Unset
        if isinstance(self.wandb_api_key, Unset):
            wandb_api_key = UNSET
        else:
            wandb_api_key = self.wandb_api_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if spend_limit is not UNSET:
            field_dict["spend_limit"] = spend_limit
        if wandb_api_key is not UNSET:
            field_dict["wandb_api_key"] = wandb_api_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_spend_limit(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        spend_limit = _parse_spend_limit(d.pop("spend_limit", UNSET))

        def _parse_wandb_api_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        wandb_api_key = _parse_wandb_api_key(d.pop("wandb_api_key", UNSET))

        update_key_request = cls(
            spend_limit=spend_limit,
            wandb_api_key=wandb_api_key,
        )

        update_key_request.additional_properties = d
        return update_key_request

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
