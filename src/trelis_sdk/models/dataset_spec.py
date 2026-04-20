from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="DatasetSpec")


@_attrs_define
class DatasetSpec:
    """Specification for a single training dataset.

    Attributes:
        dataset_id (None | str | Unset): HuggingFace dataset ID, e.g. 'my-org/my-dataset'. Mutually exclusive with
            file_store_id.
        file_store_id (None | str | Unset): FileStore UUID for S3-backed dataset. Mutually exclusive with dataset_id.
        split (str | Unset): Dataset split to use, e.g. 'train'. Default: 'train'.
        config (None | str | Unset): Dataset config name, for datasets with multiple subsets (e.g. 'en_us' in
            google/fleurs).
        samples_per_epoch (int | None | Unset): Number of samples to draw from this dataset per epoch (cap / sub-
            sample). If unset, the full dataset is used once per epoch. Must be ≤ the dataset's row count — oversampling is
            not supported. Requests exceeding the dataset size are rejected at the API layer (or clamped at train time for
            FileStore/parquet inputs whose size is unknown upfront).
    """

    dataset_id: None | str | Unset = UNSET
    file_store_id: None | str | Unset = UNSET
    split: str | Unset = "train"
    config: None | str | Unset = UNSET
    samples_per_epoch: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dataset_id: None | str | Unset
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        file_store_id: None | str | Unset
        if isinstance(self.file_store_id, Unset):
            file_store_id = UNSET
        else:
            file_store_id = self.file_store_id

        split = self.split

        config: None | str | Unset
        if isinstance(self.config, Unset):
            config = UNSET
        else:
            config = self.config

        samples_per_epoch: int | None | Unset
        if isinstance(self.samples_per_epoch, Unset):
            samples_per_epoch = UNSET
        else:
            samples_per_epoch = self.samples_per_epoch

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if split is not UNSET:
            field_dict["split"] = split
        if config is not UNSET:
            field_dict["config"] = config
        if samples_per_epoch is not UNSET:
            field_dict["samples_per_epoch"] = samples_per_epoch

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_file_store_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_store_id = _parse_file_store_id(d.pop("file_store_id", UNSET))

        split = d.pop("split", UNSET)

        def _parse_config(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        config = _parse_config(d.pop("config", UNSET))

        def _parse_samples_per_epoch(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        samples_per_epoch = _parse_samples_per_epoch(d.pop("samples_per_epoch", UNSET))

        dataset_spec = cls(
            dataset_id=dataset_id,
            file_store_id=file_store_id,
            split=split,
            config=config,
            samples_per_epoch=samples_per_epoch,
        )

        dataset_spec.additional_properties = d
        return dataset_spec

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
