from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.file_store_response import FileStoreResponse


T = TypeVar("T", bound="FileStoreListResponse")


@_attrs_define
class FileStoreListResponse:
    """Paginated list of file stores.

    Attributes:
        stores (list[FileStoreResponse]):
        total (int):
        limit (int):
        offset (int):
    """

    stores: list[FileStoreResponse]
    total: int
    limit: int
    offset: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.file_store_response import FileStoreResponse

        stores = []
        for stores_item_data in self.stores:
            stores_item = stores_item_data.to_dict()
            stores.append(stores_item)

        total = self.total

        limit = self.limit

        offset = self.offset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stores": stores,
                "total": total,
                "limit": limit,
                "offset": offset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.file_store_response import FileStoreResponse

        d = dict(src_dict)
        stores = []
        _stores = d.pop("stores")
        for stores_item_data in _stores:
            stores_item = FileStoreResponse.from_dict(stores_item_data)

            stores.append(stores_item)

        total = d.pop("total")

        limit = d.pop("limit")

        offset = d.pop("offset")

        file_store_list_response = cls(
            stores=stores,
            total=total,
            limit=limit,
            offset=offset,
        )

        file_store_list_response.additional_properties = d
        return file_store_list_response

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
