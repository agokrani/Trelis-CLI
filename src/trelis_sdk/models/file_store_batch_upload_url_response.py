from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.file_store_batch_upload_url_entry import FileStoreBatchUploadUrlEntry


T = TypeVar("T", bound="FileStoreBatchUploadUrlResponse")


@_attrs_define
class FileStoreBatchUploadUrlResponse:
    """Response from POST /file-stores/upload-urls with pre-signed upload URLs.

    Attributes:
        file_store_id (str):
        files (list[FileStoreBatchUploadUrlEntry]): List of pre-signed upload URLs, one per requested filename.
    """

    file_store_id: str
    files: list[FileStoreBatchUploadUrlEntry]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.file_store_batch_upload_url_entry import FileStoreBatchUploadUrlEntry

        file_store_id = self.file_store_id

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_store_id": file_store_id,
                "files": files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_store_batch_upload_url_entry import FileStoreBatchUploadUrlEntry

        d = dict(src_dict)
        file_store_id = d.pop("file_store_id")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = FileStoreBatchUploadUrlEntry.from_dict(files_item_data)

            files.append(files_item)

        file_store_batch_upload_url_response = cls(
            file_store_id=file_store_id,
            files=files,
        )

        file_store_batch_upload_url_response.additional_properties = d
        return file_store_batch_upload_url_response

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
