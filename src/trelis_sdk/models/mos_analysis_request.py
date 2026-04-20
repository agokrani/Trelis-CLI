from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.mos_analysis_request_output_target import MOSAnalysisRequestOutputTarget
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="MOSAnalysisRequest")


@_attrs_define
class MOSAnalysisRequest:
    """v2 MOS request — FileStore or HF dataset, contract-validated.

    Attributes:
        file_store_id (None | str | Unset): FileStore holding audio to score (contract: must accept mos input types).
        dataset_id (None | str | Unset): HuggingFace dataset id with audio column.
        split (str | Unset): Dataset split to score. Default: 'test'.
        audio_column (str | Unset): Column name containing audio data. Default: 'audio'.
        num_samples (int | Unset): Max samples to score (UTMOS22 skips samples >30s). Default: 500.
        push_results (bool | None | Unset): Push scored dataset to HF Hub. Defaults to True when HF token available.
        output_target (MOSAnalysisRequestOutputTarget | Unset): Where to write the scored dataset: S3 (project bucket),
            HF Hub, or both. Default: MOSAnalysisRequestOutputTarget.HF.
        output_name (None | str | Unset): Custom name for the output HF dataset (if pushed).
    """

    file_store_id: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    split: str | Unset = "test"
    audio_column: str | Unset = "audio"
    num_samples: int | Unset = 500
    push_results: bool | None | Unset = UNSET
    output_target: MOSAnalysisRequestOutputTarget | Unset = MOSAnalysisRequestOutputTarget.HF
    output_name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        file_store_id: None | str | Unset
        if isinstance(self.file_store_id, Unset):
            file_store_id = UNSET
        else:
            file_store_id = self.file_store_id

        dataset_id: None | str | Unset
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        split = self.split

        audio_column = self.audio_column

        num_samples = self.num_samples

        push_results: bool | None | Unset
        if isinstance(self.push_results, Unset):
            push_results = UNSET
        else:
            push_results = self.push_results

        output_target: str | Unset = UNSET
        if not isinstance(self.output_target, Unset):
            output_target = self.output_target.value

        output_name: None | str | Unset
        if isinstance(self.output_name, Unset):
            output_name = UNSET
        else:
            output_name = self.output_name

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if split is not UNSET:
            field_dict["split"] = split
        if audio_column is not UNSET:
            field_dict["audio_column"] = audio_column
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if push_results is not UNSET:
            field_dict["push_results"] = push_results
        if output_target is not UNSET:
            field_dict["output_target"] = output_target
        if output_name is not UNSET:
            field_dict["output_name"] = output_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_file_store_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_store_id = _parse_file_store_id(d.pop("file_store_id", UNSET))

        def _parse_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        split = d.pop("split", UNSET)

        audio_column = d.pop("audio_column", UNSET)

        num_samples = d.pop("num_samples", UNSET)

        def _parse_push_results(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        push_results = _parse_push_results(d.pop("push_results", UNSET))

        _output_target = d.pop("output_target", UNSET)
        output_target: MOSAnalysisRequestOutputTarget | Unset
        if isinstance(_output_target, Unset):
            output_target = UNSET
        else:
            output_target = MOSAnalysisRequestOutputTarget(_output_target)

        def _parse_output_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_name = _parse_output_name(d.pop("output_name", UNSET))

        mos_analysis_request = cls(
            file_store_id=file_store_id,
            dataset_id=dataset_id,
            split=split,
            audio_column=audio_column,
            num_samples=num_samples,
            push_results=push_results,
            output_target=output_target,
            output_name=output_name,
        )

        return mos_analysis_request
