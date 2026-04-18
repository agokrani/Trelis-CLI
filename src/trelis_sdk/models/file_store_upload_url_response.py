from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


T = TypeVar("T", bound="FileStoreUploadUrlResponse")


@_attrs_define
class FileStoreUploadUrlResponse:
    """Presigned URL for a FileStore upload.

    Attributes:
        file_store_id (str):
        upload_url (str):
        content_type (str):
        expires_in (int):
    """

    file_store_id: str
    upload_url: str
    content_type: str
    expires_in: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file_store_id = self.file_store_id

        upload_url = self.upload_url

        content_type = self.content_type

        expires_in = self.expires_in

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_store_id": file_store_id,
                "upload_url": upload_url,
                "content_type": content_type,
                "expires_in": expires_in,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_store_id = d.pop("file_store_id")

        upload_url = d.pop("upload_url")

        content_type = d.pop("content_type")

        expires_in = d.pop("expires_in")

        file_store_upload_url_response = cls(
            file_store_id=file_store_id,
            upload_url=upload_url,
            content_type=content_type,
            expires_in=expires_in,
        )

        file_store_upload_url_response.additional_properties = d
        return file_store_upload_url_response

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
