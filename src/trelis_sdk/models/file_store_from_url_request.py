from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="FileStoreFromUrlRequest")


@_attrs_define
class FileStoreFromUrlRequest:
    """Fetch a remote URL directly into a new or existing FileStore (no session needed).

    Attributes:
        url (None | str | Unset): Single HTTPS URL of a ZIP, TAR, or audio file. Mutually exclusive with 'urls'.
        urls (list[str] | None | Unset): List of HTTPS URLs to fetch into the same FileStore. Mutually exclusive with
            'url'.
        name (None | str | Unset):
        file_store_id (None | str | Unset): Existing FileStore ID to append files to. If omitted, a new FileStore is
            created.
    """

    url: None | str | Unset = UNSET
    urls: list[str] | None | Unset = UNSET
    name: None | str | Unset = UNSET
    file_store_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        urls: list[str] | None | Unset
        if isinstance(self.urls, Unset):
            urls = UNSET
        elif isinstance(self.urls, list):
            urls = self.urls

        else:
            urls = self.urls

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        file_store_id: None | str | Unset
        if isinstance(self.file_store_id, Unset):
            file_store_id = UNSET
        else:
            file_store_id = self.file_store_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if urls is not UNSET:
            field_dict["urls"] = urls
        if name is not UNSET:
            field_dict["name"] = name
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        def _parse_urls(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                urls_type_0 = cast(list[str], data)

                return urls_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        urls = _parse_urls(d.pop("urls", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_file_store_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_store_id = _parse_file_store_id(d.pop("file_store_id", UNSET))

        file_store_from_url_request = cls(
            url=url,
            urls=urls,
            name=name,
            file_store_id=file_store_id,
        )

        file_store_from_url_request.additional_properties = d
        return file_store_from_url_request

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
