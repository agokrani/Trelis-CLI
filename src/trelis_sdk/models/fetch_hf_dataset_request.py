from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="FetchHFDatasetRequest")


@_attrs_define
class FetchHFDatasetRequest:
    """Request to load a HuggingFace dataset to the upload volume.

    Attributes:
        dataset_id (str): HuggingFace dataset ID (org/name)
        split (str | Unset): Dataset split Default: 'train'.
        config (None | str | Unset): Dataset config/subset name
        name (None | str | Unset): Optional name for the resulting file store
        audio_column (str | Unset): Column containing audio data Default: 'audio'.
        text_column (None | str | Unset): Column containing text/transcript. Set to null for audio-only import. Default:
            'text'.
        max_rows (int | None | Unset): Max rows to load
    """

    dataset_id: str
    split: str | Unset = "train"
    config: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    audio_column: str | Unset = "audio"
    text_column: None | str | Unset = "text"
    max_rows: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset_id = self.dataset_id

        split = self.split

        config: None | str | Unset
        if isinstance(self.config, Unset):
            config = UNSET
        else:
            config = self.config

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        audio_column = self.audio_column

        text_column: None | str | Unset
        if isinstance(self.text_column, Unset):
            text_column = UNSET
        else:
            text_column = self.text_column

        max_rows: int | None | Unset
        if isinstance(self.max_rows, Unset):
            max_rows = UNSET
        else:
            max_rows = self.max_rows

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset_id": dataset_id,
            }
        )
        if split is not UNSET:
            field_dict["split"] = split
        if config is not UNSET:
            field_dict["config"] = config
        if name is not UNSET:
            field_dict["name"] = name
        if audio_column is not UNSET:
            field_dict["audio_column"] = audio_column
        if text_column is not UNSET:
            field_dict["text_column"] = text_column
        if max_rows is not UNSET:
            field_dict["max_rows"] = max_rows

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dataset_id = d.pop("dataset_id")

        split = d.pop("split", UNSET)

        def _parse_config(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        config = _parse_config(d.pop("config", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        audio_column = d.pop("audio_column", UNSET)

        def _parse_text_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        text_column = _parse_text_column(d.pop("text_column", UNSET))

        def _parse_max_rows(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_rows = _parse_max_rows(d.pop("max_rows", UNSET))

        fetch_hf_dataset_request = cls(
            dataset_id=dataset_id,
            split=split,
            config=config,
            name=name,
            audio_column=audio_column,
            text_column=text_column,
            max_rows=max_rows,
        )

        fetch_hf_dataset_request.additional_properties = d
        return fetch_hf_dataset_request

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
