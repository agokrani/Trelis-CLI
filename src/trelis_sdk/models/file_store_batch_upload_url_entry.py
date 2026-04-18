from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset


T = TypeVar("T", bound="FileStoreBatchUploadUrlEntry")


@_attrs_define
class FileStoreBatchUploadUrlEntry:
    """A single pre-signed upload URL entry.

    Attributes:
        filename (str): Original filename from the request.
        upload_url (str): Pre-signed PUT URL. Use as the PUT target.
        content_type (str): Must be sent as the Content-Type header on the PUT request.
        expires_in (int): URL validity in seconds.
    """

    filename: str
    upload_url: str
    content_type: str
    expires_in: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        upload_url = self.upload_url

        content_type = self.content_type

        expires_in = self.expires_in

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "filename": filename,
                "upload_url": upload_url,
                "content_type": content_type,
                "expires_in": expires_in,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filename = d.pop("filename")

        upload_url = d.pop("upload_url")

        content_type = d.pop("content_type")

        expires_in = d.pop("expires_in")

        file_store_batch_upload_url_entry = cls(
            filename=filename,
            upload_url=upload_url,
            content_type=content_type,
            expires_in=expires_in,
        )

        file_store_batch_upload_url_entry.additional_properties = d
        return file_store_batch_upload_url_entry

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
