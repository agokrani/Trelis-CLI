from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.data_prep_request_audio_cleaning import DataPrepRequestAudioCleaning
from ..models.data_prep_request_output_target_type_0 import DataPrepRequestOutputTargetType0
from ..models.data_prep_request_split_option import DataPrepRequestSplitOption
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="DataPrepRequest")


@_attrs_define
class DataPrepRequest:
    """v2 data prep request — one input source, params grouped per §6.2.

    Attributes:
        language (str): Language code or full name (e.g. 'english', 'en').
        file_store_id (None | str | Unset): FileStore containing audio+text pairs or a transcribed dataset.
        dataset_id (None | str | Unset): HuggingFace dataset id (must have audio + text columns).
        dataset_split (str | Unset): Dataset split to process. Default: 'train'.
        dataset_config (None | str | Unset): Dataset config / subset name (e.g. 'french' for
            facebook/multilingual_librispeech, 'clean' for LibriSpeech). Leave empty for single-config datasets.
        segment_padding_ms (int | Unset):  Default: 150.
        silence_threshold_ms (int | Unset):  Default: 2000.
        target_chunk_duration (float | Unset):  Default: 20.0.
        max_chunk_duration (float | Unset):  Default: 30.0.
        min_chunk_duration (float | Unset):  Default: 1.0.
        pack (bool | Unset): Pack short segments up to target duration. Default: False.
        enable_confidence_filter (bool | Unset):  Default: True.
        confidence_percentile_threshold (float | Unset):  Default: 15.0.
        bad_span_min_words (int | Unset):  Default: 5.
        confidence_absolute_floor (float | Unset):  Default: -10.0.
        confidence_segment_threshold (float | Unset):  Default: -5.0.
        min_char_density (float | None | Unset):
        max_char_density (float | None | Unset):
        audio_cleaning (DataPrepRequestAudioCleaning | Unset):  Default: DataPrepRequestAudioCleaning.NONE.
        save_cleaned_audio (bool | Unset):  Default: False.
        dedup_text (bool | Unset):  Default: True.
        dedup_audio (bool | Unset):  Default: True.
        detect_repetitions (bool | Unset):  Default: True.
        repetition_threshold (float | Unset):  Default: 0.3.
        repetition_min_words (int | Unset):  Default: 8.
        strip_annotations (bool | Unset):  Default: False.
        annotation_regex (None | str | Unset):
        output_target (DataPrepRequestOutputTargetType0 | None | Unset): Output destination; constrained by project
            config.
        output_dataset_name (None | str | Unset): Output dataset/FileStore name; auto-generated if omitted.
        split_option (DataPrepRequestSplitOption | Unset):  Default: DataPrepRequestSplitOption.CREATE_VALIDATION.
        max_val_rows (int | Unset):  Default: 500.
        max_test_rows (int | Unset):  Default: 500.
    """

    language: str
    file_store_id: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    dataset_split: str | Unset = "train"
    dataset_config: None | str | Unset = UNSET
    segment_padding_ms: int | Unset = 150
    silence_threshold_ms: int | Unset = 2000
    target_chunk_duration: float | Unset = 20.0
    max_chunk_duration: float | Unset = 30.0
    min_chunk_duration: float | Unset = 1.0
    pack: bool | Unset = False
    enable_confidence_filter: bool | Unset = True
    confidence_percentile_threshold: float | Unset = 15.0
    bad_span_min_words: int | Unset = 5
    confidence_absolute_floor: float | Unset = -10.0
    confidence_segment_threshold: float | Unset = -5.0
    min_char_density: float | None | Unset = UNSET
    max_char_density: float | None | Unset = UNSET
    audio_cleaning: DataPrepRequestAudioCleaning | Unset = DataPrepRequestAudioCleaning.NONE
    save_cleaned_audio: bool | Unset = False
    dedup_text: bool | Unset = True
    dedup_audio: bool | Unset = True
    detect_repetitions: bool | Unset = True
    repetition_threshold: float | Unset = 0.3
    repetition_min_words: int | Unset = 8
    strip_annotations: bool | Unset = False
    annotation_regex: None | str | Unset = UNSET
    output_target: DataPrepRequestOutputTargetType0 | None | Unset = UNSET
    output_dataset_name: None | str | Unset = UNSET
    split_option: DataPrepRequestSplitOption | Unset = DataPrepRequestSplitOption.CREATE_VALIDATION
    max_val_rows: int | Unset = 500
    max_test_rows: int | Unset = 500

    def to_dict(self) -> dict[str, Any]:
        language = self.language

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

        dataset_split = self.dataset_split

        dataset_config: None | str | Unset
        if isinstance(self.dataset_config, Unset):
            dataset_config = UNSET
        else:
            dataset_config = self.dataset_config

        segment_padding_ms = self.segment_padding_ms

        silence_threshold_ms = self.silence_threshold_ms

        target_chunk_duration = self.target_chunk_duration

        max_chunk_duration = self.max_chunk_duration

        min_chunk_duration = self.min_chunk_duration

        pack = self.pack

        enable_confidence_filter = self.enable_confidence_filter

        confidence_percentile_threshold = self.confidence_percentile_threshold

        bad_span_min_words = self.bad_span_min_words

        confidence_absolute_floor = self.confidence_absolute_floor

        confidence_segment_threshold = self.confidence_segment_threshold

        min_char_density: float | None | Unset
        if isinstance(self.min_char_density, Unset):
            min_char_density = UNSET
        else:
            min_char_density = self.min_char_density

        max_char_density: float | None | Unset
        if isinstance(self.max_char_density, Unset):
            max_char_density = UNSET
        else:
            max_char_density = self.max_char_density

        audio_cleaning: str | Unset = UNSET
        if not isinstance(self.audio_cleaning, Unset):
            audio_cleaning = self.audio_cleaning.value

        save_cleaned_audio = self.save_cleaned_audio

        dedup_text = self.dedup_text

        dedup_audio = self.dedup_audio

        detect_repetitions = self.detect_repetitions

        repetition_threshold = self.repetition_threshold

        repetition_min_words = self.repetition_min_words

        strip_annotations = self.strip_annotations

        annotation_regex: None | str | Unset
        if isinstance(self.annotation_regex, Unset):
            annotation_regex = UNSET
        else:
            annotation_regex = self.annotation_regex

        output_target: None | str | Unset
        if isinstance(self.output_target, Unset):
            output_target = UNSET
        elif isinstance(self.output_target, DataPrepRequestOutputTargetType0):
            output_target = self.output_target.value
        else:
            output_target = self.output_target

        output_dataset_name: None | str | Unset
        if isinstance(self.output_dataset_name, Unset):
            output_dataset_name = UNSET
        else:
            output_dataset_name = self.output_dataset_name

        split_option: str | Unset = UNSET
        if not isinstance(self.split_option, Unset):
            split_option = self.split_option.value

        max_val_rows = self.max_val_rows

        max_test_rows = self.max_test_rows

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "language": language,
            }
        )
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if dataset_split is not UNSET:
            field_dict["dataset_split"] = dataset_split
        if dataset_config is not UNSET:
            field_dict["dataset_config"] = dataset_config
        if segment_padding_ms is not UNSET:
            field_dict["segment_padding_ms"] = segment_padding_ms
        if silence_threshold_ms is not UNSET:
            field_dict["silence_threshold_ms"] = silence_threshold_ms
        if target_chunk_duration is not UNSET:
            field_dict["target_chunk_duration"] = target_chunk_duration
        if max_chunk_duration is not UNSET:
            field_dict["max_chunk_duration"] = max_chunk_duration
        if min_chunk_duration is not UNSET:
            field_dict["min_chunk_duration"] = min_chunk_duration
        if pack is not UNSET:
            field_dict["pack"] = pack
        if enable_confidence_filter is not UNSET:
            field_dict["enable_confidence_filter"] = enable_confidence_filter
        if confidence_percentile_threshold is not UNSET:
            field_dict["confidence_percentile_threshold"] = confidence_percentile_threshold
        if bad_span_min_words is not UNSET:
            field_dict["bad_span_min_words"] = bad_span_min_words
        if confidence_absolute_floor is not UNSET:
            field_dict["confidence_absolute_floor"] = confidence_absolute_floor
        if confidence_segment_threshold is not UNSET:
            field_dict["confidence_segment_threshold"] = confidence_segment_threshold
        if min_char_density is not UNSET:
            field_dict["min_char_density"] = min_char_density
        if max_char_density is not UNSET:
            field_dict["max_char_density"] = max_char_density
        if audio_cleaning is not UNSET:
            field_dict["audio_cleaning"] = audio_cleaning
        if save_cleaned_audio is not UNSET:
            field_dict["save_cleaned_audio"] = save_cleaned_audio
        if dedup_text is not UNSET:
            field_dict["dedup_text"] = dedup_text
        if dedup_audio is not UNSET:
            field_dict["dedup_audio"] = dedup_audio
        if detect_repetitions is not UNSET:
            field_dict["detect_repetitions"] = detect_repetitions
        if repetition_threshold is not UNSET:
            field_dict["repetition_threshold"] = repetition_threshold
        if repetition_min_words is not UNSET:
            field_dict["repetition_min_words"] = repetition_min_words
        if strip_annotations is not UNSET:
            field_dict["strip_annotations"] = strip_annotations
        if annotation_regex is not UNSET:
            field_dict["annotation_regex"] = annotation_regex
        if output_target is not UNSET:
            field_dict["output_target"] = output_target
        if output_dataset_name is not UNSET:
            field_dict["output_dataset_name"] = output_dataset_name
        if split_option is not UNSET:
            field_dict["split_option"] = split_option
        if max_val_rows is not UNSET:
            field_dict["max_val_rows"] = max_val_rows
        if max_test_rows is not UNSET:
            field_dict["max_test_rows"] = max_test_rows

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        language = d.pop("language")

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

        dataset_split = d.pop("dataset_split", UNSET)

        def _parse_dataset_config(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_config = _parse_dataset_config(d.pop("dataset_config", UNSET))

        segment_padding_ms = d.pop("segment_padding_ms", UNSET)

        silence_threshold_ms = d.pop("silence_threshold_ms", UNSET)

        target_chunk_duration = d.pop("target_chunk_duration", UNSET)

        max_chunk_duration = d.pop("max_chunk_duration", UNSET)

        min_chunk_duration = d.pop("min_chunk_duration", UNSET)

        pack = d.pop("pack", UNSET)

        enable_confidence_filter = d.pop("enable_confidence_filter", UNSET)

        confidence_percentile_threshold = d.pop("confidence_percentile_threshold", UNSET)

        bad_span_min_words = d.pop("bad_span_min_words", UNSET)

        confidence_absolute_floor = d.pop("confidence_absolute_floor", UNSET)

        confidence_segment_threshold = d.pop("confidence_segment_threshold", UNSET)

        def _parse_min_char_density(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        min_char_density = _parse_min_char_density(d.pop("min_char_density", UNSET))

        def _parse_max_char_density(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_char_density = _parse_max_char_density(d.pop("max_char_density", UNSET))

        _audio_cleaning = d.pop("audio_cleaning", UNSET)
        audio_cleaning: DataPrepRequestAudioCleaning | Unset
        if isinstance(_audio_cleaning, Unset):
            audio_cleaning = UNSET
        else:
            audio_cleaning = DataPrepRequestAudioCleaning(_audio_cleaning)

        save_cleaned_audio = d.pop("save_cleaned_audio", UNSET)

        dedup_text = d.pop("dedup_text", UNSET)

        dedup_audio = d.pop("dedup_audio", UNSET)

        detect_repetitions = d.pop("detect_repetitions", UNSET)

        repetition_threshold = d.pop("repetition_threshold", UNSET)

        repetition_min_words = d.pop("repetition_min_words", UNSET)

        strip_annotations = d.pop("strip_annotations", UNSET)

        def _parse_annotation_regex(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        annotation_regex = _parse_annotation_regex(d.pop("annotation_regex", UNSET))

        def _parse_output_target(data: object) -> DataPrepRequestOutputTargetType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                output_target_type_0 = DataPrepRequestOutputTargetType0(data)

                return output_target_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DataPrepRequestOutputTargetType0 | None | Unset, data)

        output_target = _parse_output_target(d.pop("output_target", UNSET))

        def _parse_output_dataset_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_dataset_name = _parse_output_dataset_name(d.pop("output_dataset_name", UNSET))

        _split_option = d.pop("split_option", UNSET)
        split_option: DataPrepRequestSplitOption | Unset
        if isinstance(_split_option, Unset):
            split_option = UNSET
        else:
            split_option = DataPrepRequestSplitOption(_split_option)

        max_val_rows = d.pop("max_val_rows", UNSET)

        max_test_rows = d.pop("max_test_rows", UNSET)

        data_prep_request = cls(
            language=language,
            file_store_id=file_store_id,
            dataset_id=dataset_id,
            dataset_split=dataset_split,
            dataset_config=dataset_config,
            segment_padding_ms=segment_padding_ms,
            silence_threshold_ms=silence_threshold_ms,
            target_chunk_duration=target_chunk_duration,
            max_chunk_duration=max_chunk_duration,
            min_chunk_duration=min_chunk_duration,
            pack=pack,
            enable_confidence_filter=enable_confidence_filter,
            confidence_percentile_threshold=confidence_percentile_threshold,
            bad_span_min_words=bad_span_min_words,
            confidence_absolute_floor=confidence_absolute_floor,
            confidence_segment_threshold=confidence_segment_threshold,
            min_char_density=min_char_density,
            max_char_density=max_char_density,
            audio_cleaning=audio_cleaning,
            save_cleaned_audio=save_cleaned_audio,
            dedup_text=dedup_text,
            dedup_audio=dedup_audio,
            detect_repetitions=detect_repetitions,
            repetition_threshold=repetition_threshold,
            repetition_min_words=repetition_min_words,
            strip_annotations=strip_annotations,
            annotation_regex=annotation_regex,
            output_target=output_target,
            output_dataset_name=output_dataset_name,
            split_option=split_option,
            max_val_rows=max_val_rows,
            max_test_rows=max_test_rows,
        )

        return data_prep_request
