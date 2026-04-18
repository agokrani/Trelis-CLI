from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.filter_request_audio_cleaning import FilterRequestAudioCleaning
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="FilterRequest")


@_attrs_define
class FilterRequest:
    """Request to start a filtering job.

    Attributes:
        model_id (str | Unset):  Default: 'openai/whisper-large-v3-turbo'.
        dataset_id (None | str | Unset): HuggingFace dataset ID. Mutually exclusive with file_store_id.
        file_store_id (None | str | Unset): FileStore UUID for S3-backed dataset. Mutually exclusive with dataset_id.
        split (str | Unset): Dataset split to filter. Use 'train', 'validation', 'test', or 'all' to filter every
            available split sequentially in a single job. Default: 'train'.
        cer_threshold (float | None | Unset): CER threshold for filtering. Samples with CER >= threshold are removed. If
            omitted, an optimal threshold is auto-detected using Otsu's method.
        output_dataset_id (None | str | Unset): HuggingFace dataset ID for filtered output. When omitted, defaults to
            '{dataset_id}-filtered'. If the output dataset already has a 'filter_cer' column from a previous run with the
            same model (and the corresponding '-dropped' companion dataset exists), the job will re-split using the stored
            CER scores at the new threshold — no inference is re-run.
        language (str | Unset):  Default: 'auto'.
        private (bool | Unset):  Default: True.
        audio_cleaning (FilterRequestAudioCleaning | Unset): Audio pre-processing applied before ASR inference. 'none':
            no processing. 'basic': highpass 80Hz + RMS normalization. 'denoise': basic + spectral gating noise reduction.
            Default: FilterRequestAudioCleaning.NONE.
        save_dropped (bool | Unset): Save filtered-out samples as a separate dataset for review. Default: True.
        normalizer (str | Unset): Text normalizer applied before CER calculation. 'auto' selects based on language
            (default). 'generic' is Unicode-aware for any language. 'whisper-english' is OpenAI Whisper's aggressive English
            normalizer (numbers, abbreviations, contractions). 'none' skips normalization (raw text). Or pass a language
            name (e.g. 'greek') to force a language-specific normalizer. Default: 'auto'.
        router_max_concurrency (int | Unset): Max parallel requests to Trelis Router for proprietary ASR models. Lower
            this if your Router API key has a low requests-per-minute limit. Default: 16.
    """

    model_id: str | Unset = "openai/whisper-large-v3-turbo"
    dataset_id: None | str | Unset = UNSET
    file_store_id: None | str | Unset = UNSET
    split: str | Unset = "train"
    cer_threshold: float | None | Unset = UNSET
    output_dataset_id: None | str | Unset = UNSET
    language: str | Unset = "auto"
    private: bool | Unset = True
    audio_cleaning: FilterRequestAudioCleaning | Unset = FilterRequestAudioCleaning.NONE
    save_dropped: bool | Unset = True
    normalizer: str | Unset = "auto"
    router_max_concurrency: int | Unset = 16

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id

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

        cer_threshold: float | None | Unset
        if isinstance(self.cer_threshold, Unset):
            cer_threshold = UNSET
        else:
            cer_threshold = self.cer_threshold

        output_dataset_id: None | str | Unset
        if isinstance(self.output_dataset_id, Unset):
            output_dataset_id = UNSET
        else:
            output_dataset_id = self.output_dataset_id

        language = self.language

        private = self.private

        audio_cleaning: str | Unset = UNSET
        if not isinstance(self.audio_cleaning, Unset):
            audio_cleaning = self.audio_cleaning.value

        save_dropped = self.save_dropped

        normalizer = self.normalizer

        router_max_concurrency = self.router_max_concurrency

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if split is not UNSET:
            field_dict["split"] = split
        if cer_threshold is not UNSET:
            field_dict["cer_threshold"] = cer_threshold
        if output_dataset_id is not UNSET:
            field_dict["output_dataset_id"] = output_dataset_id
        if language is not UNSET:
            field_dict["language"] = language
        if private is not UNSET:
            field_dict["private"] = private
        if audio_cleaning is not UNSET:
            field_dict["audio_cleaning"] = audio_cleaning
        if save_dropped is not UNSET:
            field_dict["save_dropped"] = save_dropped
        if normalizer is not UNSET:
            field_dict["normalizer"] = normalizer
        if router_max_concurrency is not UNSET:
            field_dict["router_max_concurrency"] = router_max_concurrency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_id = d.pop("model_id", UNSET)

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

        def _parse_cer_threshold(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        cer_threshold = _parse_cer_threshold(d.pop("cer_threshold", UNSET))

        def _parse_output_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_dataset_id = _parse_output_dataset_id(d.pop("output_dataset_id", UNSET))

        language = d.pop("language", UNSET)

        private = d.pop("private", UNSET)

        _audio_cleaning = d.pop("audio_cleaning", UNSET)
        audio_cleaning: FilterRequestAudioCleaning | Unset
        if isinstance(_audio_cleaning, Unset):
            audio_cleaning = UNSET
        else:
            audio_cleaning = FilterRequestAudioCleaning(_audio_cleaning)

        save_dropped = d.pop("save_dropped", UNSET)

        normalizer = d.pop("normalizer", UNSET)

        router_max_concurrency = d.pop("router_max_concurrency", UNSET)

        filter_request = cls(
            model_id=model_id,
            dataset_id=dataset_id,
            file_store_id=file_store_id,
            split=split,
            cer_threshold=cer_threshold,
            output_dataset_id=output_dataset_id,
            language=language,
            private=private,
            audio_cleaning=audio_cleaning,
            save_dropped=save_dropped,
            normalizer=normalizer,
            router_max_concurrency=router_max_concurrency,
        )

        return filter_request
