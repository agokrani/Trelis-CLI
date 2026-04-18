from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="FileStoreResponse")


@_attrs_define
class FileStoreResponse:
    """A file store entry.

    Attributes:
        id (str):
        name (str):
        source (str):
        storage_backend (str):
        content_type (str):
        file_count (int):
        size_bytes (int):
        total_duration_seconds (float | None):
        created_at (None | str):
    """

    id: str
    name: str
    source: str
    storage_backend: str
    content_type: str
    file_count: int
    size_bytes: int
    total_duration_seconds: float | None
    created_at: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        source = self.source

        storage_backend = self.storage_backend

        content_type = self.content_type

        file_count = self.file_count

        size_bytes = self.size_bytes

        total_duration_seconds: float | None
        total_duration_seconds = self.total_duration_seconds

        created_at: None | str
        created_at = self.created_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "source": source,
                "storage_backend": storage_backend,
                "content_type": content_type,
                "file_count": file_count,
                "size_bytes": size_bytes,
                "total_duration_seconds": total_duration_seconds,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        source = d.pop("source")

        storage_backend = d.pop("storage_backend")

        content_type = d.pop("content_type")

        file_count = d.pop("file_count")

        size_bytes = d.pop("size_bytes")

        def _parse_total_duration_seconds(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total_duration_seconds = _parse_total_duration_seconds(d.pop("total_duration_seconds"))

        def _parse_created_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        created_at = _parse_created_at(d.pop("created_at"))

        file_store_response = cls(
            id=id,
            name=name,
            source=source,
            storage_backend=storage_backend,
            content_type=content_type,
            file_count=file_count,
            size_bytes=size_bytes,
            total_duration_seconds=total_duration_seconds,
            created_at=created_at,
        )

        file_store_response.additional_properties = d
        return file_store_response

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
