from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.speaker_similarity_v2_request_mode import SpeakerSimilarityV2RequestMode
from ..models.speaker_similarity_v2_request_output_target import (
    SpeakerSimilarityV2RequestOutputTarget,
)
from ..models.speaker_similarity_v2_request_sv_model import SpeakerSimilarityV2RequestSvModel
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="SpeakerSimilarityV2Request")


@_attrs_define
class SpeakerSimilarityV2Request:
    """v2 speaker-similarity request — FileStore or HF dataset, contract-validated.

    Attributes:
        mode (SpeakerSimilarityV2RequestMode | Unset): 'paired': dataset has both generated_audio and ref_audio columns
            (typical ZSVC eval output). 'single_ref': generated dataset + separate reference dataset. Default:
            SpeakerSimilarityV2RequestMode.PAIRED.
        file_store_id (None | str | Unset): FileStore holding generated_audio (paired mode: + ref_audio).
        dataset_id (None | str | Unset): HuggingFace dataset id with generated audio.
        split (str | Unset): Dataset split to evaluate. Default: 'train'.
        generated_audio_column (str | Unset):  Default: 'generated_audio'.
        ref_audio_column (str | Unset):  Default: 'ref_audio'.
        ref_dataset_id (None | str | Unset): Single-ref mode only: HF dataset with reference speaker audio.
        ref_split (str | Unset):  Default: 'train'.
        ref_column (str | Unset):  Default: 'audio'.
        num_ref_samples (int | Unset):  Default: 1.
        max_rows (int | Unset): 0 = all rows. Default: 0.
        push_results (bool | None | Unset): Push scored dataset to HF Hub. Defaults to True when HF token available.
        output_target (SpeakerSimilarityV2RequestOutputTarget | Unset): Where to write the scored dataset. Project
            permissions gate this. Default: SpeakerSimilarityV2RequestOutputTarget.HF.
        output_name (None | str | Unset): Custom name for the output HF dataset (if pushed).
        sv_model (SpeakerSimilarityV2RequestSvModel | Unset): 'wavlm_large_sv' (default): WavLM-Large + ECAPA-TDNN from
            seed-tts-eval. Paper-comparable 0.2–0.8 scale. 'ecapa': SpeechBrain ECAPA, Apache 2.0, commercial-safe,
            compressed 0.9–1.0 on TTS audio. Default: SpeakerSimilarityV2RequestSvModel.WAVLM_LARGE_SV.
    """

    mode: SpeakerSimilarityV2RequestMode | Unset = SpeakerSimilarityV2RequestMode.PAIRED
    file_store_id: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    split: str | Unset = "train"
    generated_audio_column: str | Unset = "generated_audio"
    ref_audio_column: str | Unset = "ref_audio"
    ref_dataset_id: None | str | Unset = UNSET
    ref_split: str | Unset = "train"
    ref_column: str | Unset = "audio"
    num_ref_samples: int | Unset = 1
    max_rows: int | Unset = 0
    push_results: bool | None | Unset = UNSET
    output_target: SpeakerSimilarityV2RequestOutputTarget | Unset = (
        SpeakerSimilarityV2RequestOutputTarget.HF
    )
    output_name: None | str | Unset = UNSET
    sv_model: SpeakerSimilarityV2RequestSvModel | Unset = (
        SpeakerSimilarityV2RequestSvModel.WAVLM_LARGE_SV
    )

    def to_dict(self) -> dict[str, Any]:
        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

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

        output_target: str | Unset = UNSET
        if not isinstance(self.output_target, Unset):
            output_target = self.output_target.value

        output_name: None | str | Unset
        if isinstance(self.output_name, Unset):
            output_name = UNSET
        else:
            output_name = self.output_name

        sv_model: str | Unset = UNSET
        if not isinstance(self.sv_model, Unset):
            sv_model = self.sv_model.value

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if mode is not UNSET:
            field_dict["mode"] = mode
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
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
        if output_target is not UNSET:
            field_dict["output_target"] = output_target
        if output_name is not UNSET:
            field_dict["output_name"] = output_name
        if sv_model is not UNSET:
            field_dict["sv_model"] = sv_model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _mode = d.pop("mode", UNSET)
        mode: SpeakerSimilarityV2RequestMode | Unset
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = SpeakerSimilarityV2RequestMode(_mode)

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

        _output_target = d.pop("output_target", UNSET)
        output_target: SpeakerSimilarityV2RequestOutputTarget | Unset
        if isinstance(_output_target, Unset):
            output_target = UNSET
        else:
            output_target = SpeakerSimilarityV2RequestOutputTarget(_output_target)

        def _parse_output_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_name = _parse_output_name(d.pop("output_name", UNSET))

        _sv_model = d.pop("sv_model", UNSET)
        sv_model: SpeakerSimilarityV2RequestSvModel | Unset
        if isinstance(_sv_model, Unset):
            sv_model = UNSET
        else:
            sv_model = SpeakerSimilarityV2RequestSvModel(_sv_model)

        speaker_similarity_v2_request = cls(
            mode=mode,
            file_store_id=file_store_id,
            dataset_id=dataset_id,
            split=split,
            generated_audio_column=generated_audio_column,
            ref_audio_column=ref_audio_column,
            ref_dataset_id=ref_dataset_id,
            ref_split=ref_split,
            ref_column=ref_column,
            num_ref_samples=num_ref_samples,
            max_rows=max_rows,
            push_results=push_results,
            output_target=output_target,
            output_name=output_name,
            sv_model=sv_model,
        )

        return speaker_similarity_v2_request
