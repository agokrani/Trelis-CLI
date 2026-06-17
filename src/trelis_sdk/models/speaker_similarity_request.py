from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.speaker_similarity_request_mode import SpeakerSimilarityRequestMode
from ..models.speaker_similarity_request_sv_model import SpeakerSimilarityRequestSvModel
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="SpeakerSimilarityRequest")


@_attrs_define
class SpeakerSimilarityRequest:
    """Request to start a speaker similarity evaluation job.

    Attributes:
        dataset_id (str): HuggingFace dataset ID with generated audio (e.g. 'Trelis/my-tts-output').
        mode (SpeakerSimilarityRequestMode | Unset): Evaluation mode: 'paired' (ref + gen columns in same dataset) or
            'single_ref' (separate ref dataset). Default: SpeakerSimilarityRequestMode.PAIRED.
        split (str | Unset): Dataset split to evaluate. Default: 'test'.
        generated_audio_column (str | Unset): Column containing generated audio. Default: 'generated_audio'.
        ref_audio_column (str | Unset): Column containing reference audio (paired mode only). Default: 'ref_audio'.
        ref_dataset_id (None | str | Unset): HuggingFace dataset ID with reference speaker audio (single_ref mode only).
        ref_split (str | Unset): Split of the reference dataset (single_ref mode only). Default: 'train'.
        ref_column (str | Unset): Audio column in the reference dataset (single_ref mode only). Default: 'audio'.
        num_ref_samples (int | Unset): Number of reference samples to average for centroid (single_ref mode, default 1).
            Default: 1.
        max_rows (int | Unset): Max rows to evaluate (0 = all). Default: 0.
        push_results (bool | None | Unset): Push scored dataset to HuggingFace. Defaults to True if HF token is
            available.
        output_org (None | str | Unset): HuggingFace organization for the output dataset.
        output_name (None | str | Unset): Custom name for the output dataset.
        sv_model (SpeakerSimilarityRequestSvModel | Unset): Speaker verification model. 'ecapa' (default): SpeechBrain
            ECAPA-TDNN, Apache 2.0, commercial-safe, compressed 0.9-1.0 scale on TTS audio. 'wavlm_large_sv': WavLM-Large +
            ECAPA-TDNN from seed-tts-eval (Chen et al. 2022b), paper-comparable 0.2-0.8 scale; checkpoint license unclear —
            check before commercial use. Default: SpeakerSimilarityRequestSvModel.ECAPA.
    """

    dataset_id: str
    mode: SpeakerSimilarityRequestMode | Unset = SpeakerSimilarityRequestMode.PAIRED
    split: str | Unset = "test"
    generated_audio_column: str | Unset = "generated_audio"
    ref_audio_column: str | Unset = "ref_audio"
    ref_dataset_id: None | str | Unset = UNSET
    ref_split: str | Unset = "train"
    ref_column: str | Unset = "audio"
    num_ref_samples: int | Unset = 1
    max_rows: int | Unset = 0
    push_results: bool | None | Unset = UNSET
    output_org: None | str | Unset = UNSET
    output_name: None | str | Unset = UNSET
    sv_model: SpeakerSimilarityRequestSvModel | Unset = SpeakerSimilarityRequestSvModel.ECAPA

    def to_dict(self) -> dict[str, Any]:
        dataset_id = self.dataset_id

        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        split = self.split

        generated_audio_column = self.generated_audio_column

        ref_audio_column = self.ref_audio_column

        ref_dataset_id: None | str | Unset
        if isinstance(self.ref_dataset_id, Unset):
            ref_dataset_id = UNSET
        else:
            ref_dataset_id = self.ref_dataset_id

        ref_split = self.ref_split

        ref_column = self.ref_column

        num_ref_samples = self.num_ref_samples

        max_rows = self.max_rows

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

        sv_model: str | Unset = UNSET
        if not isinstance(self.sv_model, Unset):
            sv_model = self.sv_model.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "dataset_id": dataset_id,
            }
        )
        if mode is not UNSET:
            field_dict["mode"] = mode
        if split is not UNSET:
            field_dict["split"] = split
        if generated_audio_column is not UNSET:
            field_dict["generated_audio_column"] = generated_audio_column
        if ref_audio_column is not UNSET:
            field_dict["ref_audio_column"] = ref_audio_column
        if ref_dataset_id is not UNSET:
            field_dict["ref_dataset_id"] = ref_dataset_id
        if ref_split is not UNSET:
            field_dict["ref_split"] = ref_split
        if ref_column is not UNSET:
            field_dict["ref_column"] = ref_column
        if num_ref_samples is not UNSET:
            field_dict["num_ref_samples"] = num_ref_samples
        if max_rows is not UNSET:
            field_dict["max_rows"] = max_rows
        if push_results is not UNSET:
            field_dict["push_results"] = push_results
        if output_org is not UNSET:
            field_dict["output_org"] = output_org
        if output_name is not UNSET:
            field_dict["output_name"] = output_name
        if sv_model is not UNSET:
            field_dict["sv_model"] = sv_model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dataset_id = d.pop("dataset_id")

        _mode = d.pop("mode", UNSET)
        mode: SpeakerSimilarityRequestMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = SpeakerSimilarityRequestMode(_mode)

        split = d.pop("split", UNSET)

        generated_audio_column = d.pop("generated_audio_column", UNSET)

        ref_audio_column = d.pop("ref_audio_column", UNSET)

        def _parse_ref_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ref_dataset_id = _parse_ref_dataset_id(d.pop("ref_dataset_id", UNSET))

        ref_split = d.pop("ref_split", UNSET)

        ref_column = d.pop("ref_column", UNSET)

        num_ref_samples = d.pop("num_ref_samples", UNSET)

        max_rows = d.pop("max_rows", UNSET)

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

        _sv_model = d.pop("sv_model", UNSET)
        sv_model: SpeakerSimilarityRequestSvModel | Unset
        if isinstance(_sv_model, Unset):
            sv_model = UNSET
        else:
            sv_model = SpeakerSimilarityRequestSvModel(_sv_model)

        speaker_similarity_request = cls(
            dataset_id=dataset_id,
            mode=mode,
            split=split,
            generated_audio_column=generated_audio_column,
            ref_audio_column=ref_audio_column,
            ref_dataset_id=ref_dataset_id,
            ref_split=ref_split,
            ref_column=ref_column,
            num_ref_samples=num_ref_samples,
            max_rows=max_rows,
            push_results=push_results,
            output_org=output_org,
            output_name=output_name,
            sv_model=sv_model,
        )

        return speaker_similarity_request
