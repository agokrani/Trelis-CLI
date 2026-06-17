from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="MOSEvaluationRequest")


@_attrs_define
class MOSEvaluationRequest:
    """Request to start a MOS evaluation job.

    Attributes:
        dataset_id (str): HuggingFace dataset ID containing audio samples to score (e.g. 'Trelis/my-audio-dataset').
        split (str | Unset): Dataset split to score (e.g. 'test', 'validation', 'train'). Default: 'test'.
        audio_column (str | Unset): Name of the column containing audio data. Default: 'audio'.
        num_samples (int | Unset): Maximum number of samples to score. Default: 500.
        push_results (bool | None | Unset): Push scored dataset to HuggingFace. Defaults to True if HF token is
            available.
        output_org (None | str | Unset): HuggingFace organization for the output dataset.
        output_name (None | str | Unset): Custom name for the output dataset. Defaults to '{dataset}-mos-eval'.
    """

    dataset_id: str
    split: str | Unset = "test"
    audio_column: str | Unset = "audio"
    num_samples: int | Unset = 500
    push_results: bool | None | Unset = UNSET
    output_org: None | str | Unset = UNSET
    output_name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        dataset_id = self.dataset_id

        split = self.split

        audio_column = self.audio_column

        num_samples = self.num_samples

        push_results: bool | None | Unset
        if isinstance(self.push_results, Unset):
            push_results = UNSET
        else:
            push_results = self.push_results

        output_org: None | str | Unset
        if isinstance(self.output_org, Unset):
            output_org = UNSET
        else:
            output_org = self.output_org

        output_name: None | str | Unset
        if isinstance(self.output_name, Unset):
            output_name = UNSET
        else:
            output_name = self.output_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "dataset_id": dataset_id,
            }
        )
        if split is not UNSET:
            field_dict["split"] = split
        if audio_column is not UNSET:
            field_dict["audio_column"] = audio_column
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if push_results is not UNSET:
            field_dict["push_results"] = push_results
        if output_org is not UNSET:
            field_dict["output_org"] = output_org
        if output_name is not UNSET:
            field_dict["output_name"] = output_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dataset_id = d.pop("dataset_id")

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

        def _parse_output_org(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_org = _parse_output_org(d.pop("output_org", UNSET))

        def _parse_output_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_name = _parse_output_name(d.pop("output_name", UNSET))

        mos_evaluation_request = cls(
            dataset_id=dataset_id,
            split=split,
            audio_column=audio_column,
            num_samples=num_samples,
            push_results=push_results,
            output_org=output_org,
            output_name=output_name,
        )

        return mos_evaluation_request
