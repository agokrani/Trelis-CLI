from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="KeyResponse")


@_attrs_define
class KeyResponse:
    """Response with API key info.

    Attributes:
        id (str):
        key_prefix (str):
        name (str):
        requests_per_minute (int):
        max_concurrent_jobs (int):
        created_at (str):
        key (None | str | Unset):
        project_id (None | str | Unset):
        project_name (None | str | Unset):
        spend_limit (float | None | Unset):
        total_spend (float | Unset):  Default: 0.0.
        has_wandb_key (bool | Unset):  Default: False.
        last_used_at (None | str | Unset):
    """

    id: str
    key_prefix: str
    name: str
    requests_per_minute: int
    max_concurrent_jobs: int
    created_at: str
    key: None | str | Unset = UNSET
    project_id: None | str | Unset = UNSET
    project_name: None | str | Unset = UNSET
    spend_limit: float | None | Unset = UNSET
    total_spend: float | Unset = 0.0
    has_wandb_key: bool | Unset = False
    last_used_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key_prefix = self.key_prefix

        name = self.name

        requests_per_minute = self.requests_per_minute

        max_concurrent_jobs = self.max_concurrent_jobs

        created_at = self.created_at

        key: None | str | Unset
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        project_name: None | str | Unset
        if isinstance(self.project_name, Unset):
            project_name = UNSET
        else:
            project_name = self.project_name

        spend_limit: float | None | Unset
        if isinstance(self.spend_limit, Unset):
            spend_limit = UNSET
        else:
            spend_limit = self.spend_limit

        total_spend = self.total_spend

        has_wandb_key = self.has_wandb_key

        last_used_at: None | str | Unset
        if isinstance(self.last_used_at, Unset):
            last_used_at = UNSET
        else:
            last_used_at = self.last_used_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "key_prefix": key_prefix,
                "name": name,
                "requests_per_minute": requests_per_minute,
                "max_concurrent_jobs": max_concurrent_jobs,
                "created_at": created_at,
            }
        )
        if key is not UNSET:
            field_dict["key"] = key
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if spend_limit is not UNSET:
            field_dict["spend_limit"] = spend_limit
        if total_spend is not UNSET:
            field_dict["total_spend"] = total_spend
        if has_wandb_key is not UNSET:
            field_dict["has_wandb_key"] = has_wandb_key
        if last_used_at is not UNSET:
            field_dict["last_used_at"] = last_used_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        key_prefix = d.pop("key_prefix")

        name = d.pop("name")

        requests_per_minute = d.pop("requests_per_minute")

        max_concurrent_jobs = d.pop("max_concurrent_jobs")

        created_at = d.pop("created_at")

        def _parse_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        key = _parse_key(d.pop("key", UNSET))

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_project_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_name = _parse_project_name(d.pop("project_name", UNSET))

        def _parse_spend_limit(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        spend_limit = _parse_spend_limit(d.pop("spend_limit", UNSET))

        total_spend = d.pop("total_spend", UNSET)

        has_wandb_key = d.pop("has_wandb_key", UNSET)

        def _parse_last_used_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at", UNSET))

        key_response = cls(
            id=id,
            key_prefix=key_prefix,
            name=name,
            requests_per_minute=requests_per_minute,
            max_concurrent_jobs=max_concurrent_jobs,
            created_at=created_at,
            key=key,
            project_id=project_id,
            project_name=project_name,
            spend_limit=spend_limit,
            total_spend=total_spend,
            has_wandb_key=has_wandb_key,
            last_used_at=last_used_at,
        )

        key_response.additional_properties = d
        return key_response

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
