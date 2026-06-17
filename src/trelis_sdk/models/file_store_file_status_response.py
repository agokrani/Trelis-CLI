from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="FileStoreFileStatusResponse")


@_attrs_define
class FileStoreFileStatusResponse:
    """S3 HEAD result for an individual file in a FileStore.

    Attributes:
        filename (str):
        exists (bool):
        size_bytes (int | None):
        storage_backend (str):
    """

    filename: str
    exists: bool
    size_bytes: int | None
    storage_backend: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        exists = self.exists

        size_bytes: int | None
        size_bytes = self.size_bytes

        storage_backend = self.storage_backend

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filename": filename,
                "exists": exists,
                "size_bytes": size_bytes,
                "storage_backend": storage_backend,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filename = d.pop("filename")

        exists = d.pop("exists")

        def _parse_size_bytes(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        size_bytes = _parse_size_bytes(d.pop("size_bytes"))

        storage_backend = d.pop("storage_backend")

        file_store_file_status_response = cls(
            filename=filename,
            exists=exists,
            size_bytes=size_bytes,
            storage_backend=storage_backend,
        )

        file_store_file_status_response.additional_properties = d
        return file_store_file_status_response

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
