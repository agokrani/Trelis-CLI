from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.process_request_audio_cleaning import ProcessRequestAudioCleaning
from ..models.process_request_output_target_type_0 import ProcessRequestOutputTargetType0
from ..models.process_request_split_option import ProcessRequestSplitOption
from ..models.process_request_target_sr import ProcessRequestTargetSr
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="ProcessRequest")


@_attrs_define
class ProcessRequest:
    r"""Request to process and push to HuggingFace.

    Used by both web routes and API v1 endpoints.

        Attributes:
            output_dataset_name (str):
            output_target (None | ProcessRequestOutputTargetType0 | Unset): Override output target. If omitted, resolved
                from project settings (S3 if configured, HF if enabled, both if both).
            output_org (None | str | Unset): Deprecated — ignored. The HF org from project settings is used automatically.
            hf_token (None | str | Unset): Deprecated — ignored. The HF token from project settings is used automatically.
            private (bool | Unset): Deprecated — always True. Repos are always created as private. Default: True.
            split_option (ProcessRequestSplitOption | Unset): 'create_validation' creates 80/15/5 train/validation/test
                splits; 'train_only' puts all data in train; 'validation_only' pushes all data as a validation split;
                'test_only' pushes all data as a test split. Default: ProcessRequestSplitOption.CREATE_VALIDATION.
            max_val_rows (int | Unset): Max validation split rows Default: 500.
            max_test_rows (int | Unset): Max test split rows Default: 500.
            min_char_density (float | None | Unset): Minimum chars/sec — chunks below this are dropped as misaligned. None =
                no lower bound. Typical speech is ~20-25 chars/sec; 6 is a reasonable floor.
            max_char_density (float | None | Unset): Maximum chars/sec — chunks above this are dropped as clipped/sped-up.
                None = no upper bound. 32 is a reasonable ceiling.
            dedup_text (bool | Unset): Drop rows with identical transcript text (case-insensitive). Logs dropped count.
                Default: True.
            dedup_audio (bool | Unset): Drop rows with identical audio key (source_file + start_time + end_time). Catches
                duplicate segments from the same source file. Default: True.
            detect_repetitions (bool | Unset): Drop rows where the transcript contains repeated phrases. Uses two checks:
                contiguous exact repeat of ≥3 words, and trigram ratio above threshold. Default: True.
            repetition_threshold (float | Unset): Max fraction of trigrams that may be the same trigram. Only used when
                detect_repetitions=True. Default 0.3 (30%). Default: 0.3.
            repetition_min_words (int | Unset): Minimum word count before repetition check runs. Samples shorter than this
                skip the check. Default 8. Default: 8.
            strip_annotations (bool | Unset): Strip bracketed annotations (e.g. [music], [laughter], [unintelligible]) from
                transcripts. Rows that become empty after stripping are dropped. Default: False.
            annotation_regex (None | str | Unset): Custom regex for annotation stripping. Defaults to r'\[\w[^\]]*\]' when
                strip_annotations=True and this is None. Max 200 chars.
            language (None | str | Unset): Language of the audio. Accepted formats: full name ('english', 'irish'), ISO
                639-1 ('en', 'ga'), or ISO 639-3 ('eng', 'gle'). Used for text romanization during forced alignment (uroman) and
                injected as an ISO 639-1 code into the dataset 'language' column. Setting the correct language improves
                alignment accuracy for non-Latin scripts. Default: 'english'.
            segment_padding_ms (int | Unset): Padding (ms) added around each SRT/VTT segment boundary when extracting audio
                for alignment. Default 150ms. Only used for .srt/.vtt transcripts; ignored for .txt. Default: 150.
            silence_threshold_ms (int | Unset): Silence gap (ms) between words that triggers a segment split. Default
                2000ms. Only used for .txt transcripts; ignored for .srt/.vtt. Default: 2000.
            target_chunk_duration (float | Unset): Soft target for chunk duration in seconds. For SRT/VTT with pack=False,
                each segment becomes its own sample. Default: 20.0.
            max_chunk_duration (float | Unset): Hard cap for chunk duration in seconds (max 30s for Whisper) Default: 30.0.
            min_chunk_duration (float | Unset): Filter out chunks shorter than this duration in seconds (always applied).
                Default 1s. Default: 1.0.
            pack (bool | Unset): If True, concatenate speech segments (removes silence) — improves training efficiency for
                longer runs. If False (default), each segment becomes its own sample with realistic segment lengths
                representative of real-world inference — recommended for training where the model needs to handle natural audio
                boundaries. For .srt/.vtt, segments come from transcript timestamps. For .txt, segments come from word-gap
                clustering (silence_threshold_ms). Default: False.
            vad_threshold (float | Unset): Silero VAD sensitivity for audio-only file transcription (lower = more
                sensitive). Only used when the file store contains audio-only files (no paired transcripts). Default 0.5 is
                Silero's calibrated general-purpose threshold. Use 0.25 for quiet/radio audio (e.g. ATC) to avoid missed speech.
                Default: 0.5.
            audio_cleaning (ProcessRequestAudioCleaning | Unset): Audio cleaning applied before alignment and to extracted
                speech chunks. Default 'none' preserves the original audio — important for ASR training where cleaning can
                filter out the 'hard' examples the model needs to learn from. Users can opt in (e.g. for TTS data) when cleaning
                is desired. 'none': no processing. 'basic': highpass filter at 80Hz + LUFS normalization to -12dBFS. 'denoise':
                basic + spectral gating noise reduction (prop_decrease=0.6). Default: ProcessRequestAudioCleaning.NONE.
            target_sr (ProcessRequestTargetSr | Unset): Output sample rate for audio chunks in the HuggingFace dataset.
                16000 Hz for ASR models (Whisper, Moonshine, Voxtral, Parakeet). 22050 Hz for Piper TTS. 24000 Hz for Orpheus
                TTS. Default: ProcessRequestTargetSr.VALUE_16000.
            save_cleaned_audio (bool | Unset): When True and audio_cleaning is not 'none', include a 'clean_audio' column in
                the HuggingFace dataset with the denoised version of each chunk. The 'audio' column remains the raw (silence-
                stripped) audio. Default: False.
            enable_confidence_filter (bool | Unset): Split files at runs of low-confidence alignment spans rather than
                rejecting whole files. Language-agnostic: uses per-file percentile of wav2vec2 log-prob scores. Default: True.
            confidence_percentile_threshold (int | Unset): Words below this within-file percentile (of alignment confidence)
                are flagged as low-quality. Default 15 means bottom 15% of each file's score distribution. Default: 15.
            bad_span_min_words (int | Unset): Minimum consecutive low-confidence words to trigger a split. Higher values
                tolerate technical terms that score low in isolation. Default: 5.
            confidence_absolute_floor (float | Unset): Reject the entire file if its median word score is below this log-
                prob floor. Guards against completely wrong transcripts. Default: -10.0.
            confidence_segment_threshold (float | Unset): VTT/SRT only: drop segments whose median CTC word score falls
                below this absolute threshold. Only applies when enable_confidence_filter=True and input has SRT/VTT
                transcripts. Default: -5.0.
            file_store_ids (list[str] | Unset): IDs of previously saved file stores to use as input. When provided, files
                are loaded from the Modal volume — no upload needed. Multiple stores are merged into a single dataset. Obtain
                IDs from GET /api/v1/data-prep/file-stores.
            file_store_name (None | str | Unset): Name for the file store that will be created after processing. Defaults to
                the output_dataset_name if not provided. Has no effect when file_store_ids is provided (re-run, not a new
                upload).
    """

    output_dataset_name: str
    output_target: None | ProcessRequestOutputTargetType0 | Unset = UNSET
    output_org: None | str | Unset = UNSET
    hf_token: None | str | Unset = UNSET
    private: bool | Unset = True
    split_option: ProcessRequestSplitOption | Unset = ProcessRequestSplitOption.CREATE_VALIDATION
    max_val_rows: int | Unset = 500
    max_test_rows: int | Unset = 500
    min_char_density: float | None | Unset = UNSET
    max_char_density: float | None | Unset = UNSET
    dedup_text: bool | Unset = True
    dedup_audio: bool | Unset = True
    detect_repetitions: bool | Unset = True
    repetition_threshold: float | Unset = 0.3
    repetition_min_words: int | Unset = 8
    strip_annotations: bool | Unset = False
    annotation_regex: None | str | Unset = UNSET
    language: None | str | Unset = "english"
    segment_padding_ms: int | Unset = 150
    silence_threshold_ms: int | Unset = 2000
    target_chunk_duration: float | Unset = 20.0
    max_chunk_duration: float | Unset = 30.0
    min_chunk_duration: float | Unset = 1.0
    pack: bool | Unset = False
    vad_threshold: float | Unset = 0.5
    audio_cleaning: ProcessRequestAudioCleaning | Unset = ProcessRequestAudioCleaning.NONE
    target_sr: ProcessRequestTargetSr | Unset = ProcessRequestTargetSr.VALUE_16000
    save_cleaned_audio: bool | Unset = False
    enable_confidence_filter: bool | Unset = True
    confidence_percentile_threshold: int | Unset = 15
    bad_span_min_words: int | Unset = 5
    confidence_absolute_floor: float | Unset = -10.0
    confidence_segment_threshold: float | Unset = -5.0
    file_store_ids: list[str] | Unset = UNSET
    file_store_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        output_dataset_name = self.output_dataset_name

        output_target: None | str | Unset
        if isinstance(self.output_target, Unset):
            output_target = UNSET
        elif isinstance(self.output_target, ProcessRequestOutputTargetType0):
            output_target = self.output_target.value
        else:
            output_target = self.output_target

        output_org: None | str | Unset
        if isinstance(self.output_org, Unset):
            output_org = UNSET
        else:
            output_org = self.output_org

        hf_token: None | str | Unset
        if isinstance(self.hf_token, Unset):
            hf_token = UNSET
        else:
            hf_token = self.hf_token

        private = self.private

        split_option: str | Unset = UNSET
        if not isinstance(self.split_option, Unset):
            split_option = self.split_option.value

        max_val_rows = self.max_val_rows

        max_test_rows = self.max_test_rows

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

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        segment_padding_ms = self.segment_padding_ms

        silence_threshold_ms = self.silence_threshold_ms

        target_chunk_duration = self.target_chunk_duration

        max_chunk_duration = self.max_chunk_duration

        min_chunk_duration = self.min_chunk_duration

        pack = self.pack

        vad_threshold = self.vad_threshold

        audio_cleaning: str | Unset = UNSET
        if not isinstance(self.audio_cleaning, Unset):
            audio_cleaning = self.audio_cleaning.value

        target_sr: int | Unset = UNSET
        if not isinstance(self.target_sr, Unset):
            target_sr = self.target_sr.value

        save_cleaned_audio = self.save_cleaned_audio

        enable_confidence_filter = self.enable_confidence_filter

        confidence_percentile_threshold = self.confidence_percentile_threshold

        bad_span_min_words = self.bad_span_min_words

        confidence_absolute_floor = self.confidence_absolute_floor

        confidence_segment_threshold = self.confidence_segment_threshold

        file_store_ids: list[str] | Unset = UNSET
        if not isinstance(self.file_store_ids, Unset):
            file_store_ids = self.file_store_ids

        file_store_name: None | str | Unset
        if isinstance(self.file_store_name, Unset):
            file_store_name = UNSET
        else:
            file_store_name = self.file_store_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "output_dataset_name": output_dataset_name,
            }
        )
        if output_target is not UNSET:
            field_dict["output_target"] = output_target
        if output_org is not UNSET:
            field_dict["output_org"] = output_org
        if hf_token is not UNSET:
            field_dict["hf_token"] = hf_token
        if private is not UNSET:
            field_dict["private"] = private
        if split_option is not UNSET:
            field_dict["split_option"] = split_option
        if max_val_rows is not UNSET:
            field_dict["max_val_rows"] = max_val_rows
        if max_test_rows is not UNSET:
            field_dict["max_test_rows"] = max_test_rows
        if min_char_density is not UNSET:
            field_dict["min_char_density"] = min_char_density
        if max_char_density is not UNSET:
            field_dict["max_char_density"] = max_char_density
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
        if language is not UNSET:
            field_dict["language"] = language
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
        if vad_threshold is not UNSET:
            field_dict["vad_threshold"] = vad_threshold
        if audio_cleaning is not UNSET:
            field_dict["audio_cleaning"] = audio_cleaning
        if target_sr is not UNSET:
            field_dict["target_sr"] = target_sr
        if save_cleaned_audio is not UNSET:
            field_dict["save_cleaned_audio"] = save_cleaned_audio
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
        if file_store_ids is not UNSET:
            field_dict["file_store_ids"] = file_store_ids
        if file_store_name is not UNSET:
            field_dict["file_store_name"] = file_store_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        output_dataset_name = d.pop("output_dataset_name")

        def _parse_output_target(data: object) -> None | ProcessRequestOutputTargetType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                output_target_type_0 = ProcessRequestOutputTargetType0(data)

                return output_target_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProcessRequestOutputTargetType0 | Unset, data)

        output_target = _parse_output_target(d.pop("output_target", UNSET))

        def _parse_output_org(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_org = _parse_output_org(d.pop("output_org", UNSET))

        def _parse_hf_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        hf_token = _parse_hf_token(d.pop("hf_token", UNSET))

        private = d.pop("private", UNSET)

        _split_option = d.pop("split_option", UNSET)
        split_option: ProcessRequestSplitOption | Unset
        if isinstance(_split_option, Unset):
            split_option = UNSET
        else:
            split_option = ProcessRequestSplitOption(_split_option)

        max_val_rows = d.pop("max_val_rows", UNSET)

        max_test_rows = d.pop("max_test_rows", UNSET)

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

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        segment_padding_ms = d.pop("segment_padding_ms", UNSET)

        silence_threshold_ms = d.pop("silence_threshold_ms", UNSET)

        target_chunk_duration = d.pop("target_chunk_duration", UNSET)

        max_chunk_duration = d.pop("max_chunk_duration", UNSET)

        min_chunk_duration = d.pop("min_chunk_duration", UNSET)

        pack = d.pop("pack", UNSET)

        vad_threshold = d.pop("vad_threshold", UNSET)

        _audio_cleaning = d.pop("audio_cleaning", UNSET)
        audio_cleaning: ProcessRequestAudioCleaning | Unset
        if isinstance(_audio_cleaning, Unset):
            audio_cleaning = UNSET
        else:
            audio_cleaning = ProcessRequestAudioCleaning(_audio_cleaning)

        _target_sr = d.pop("target_sr", UNSET)
        target_sr: ProcessRequestTargetSr | Unset
        if isinstance(_target_sr, Unset):
            target_sr = UNSET
        else:
            target_sr = ProcessRequestTargetSr(_target_sr)

        save_cleaned_audio = d.pop("save_cleaned_audio", UNSET)

        enable_confidence_filter = d.pop("enable_confidence_filter", UNSET)

        confidence_percentile_threshold = d.pop("confidence_percentile_threshold", UNSET)

        bad_span_min_words = d.pop("bad_span_min_words", UNSET)

        confidence_absolute_floor = d.pop("confidence_absolute_floor", UNSET)

        confidence_segment_threshold = d.pop("confidence_segment_threshold", UNSET)

        file_store_ids = cast(list[str], d.pop("file_store_ids", UNSET))

        def _parse_file_store_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_store_name = _parse_file_store_name(d.pop("file_store_name", UNSET))

        process_request = cls(
            output_dataset_name=output_dataset_name,
            output_target=output_target,
            output_org=output_org,
            hf_token=hf_token,
            private=private,
            split_option=split_option,
            max_val_rows=max_val_rows,
            max_test_rows=max_test_rows,
            min_char_density=min_char_density,
            max_char_density=max_char_density,
            dedup_text=dedup_text,
            dedup_audio=dedup_audio,
            detect_repetitions=detect_repetitions,
            repetition_threshold=repetition_threshold,
            repetition_min_words=repetition_min_words,
            strip_annotations=strip_annotations,
            annotation_regex=annotation_regex,
            language=language,
            segment_padding_ms=segment_padding_ms,
            silence_threshold_ms=silence_threshold_ms,
            target_chunk_duration=target_chunk_duration,
            max_chunk_duration=max_chunk_duration,
            min_chunk_duration=min_chunk_duration,
            pack=pack,
            vad_threshold=vad_threshold,
            audio_cleaning=audio_cleaning,
            target_sr=target_sr,
            save_cleaned_audio=save_cleaned_audio,
            enable_confidence_filter=enable_confidence_filter,
            confidence_percentile_threshold=confidence_percentile_threshold,
            bad_span_min_words=bad_span_min_words,
            confidence_absolute_floor=confidence_absolute_floor,
            confidence_segment_threshold=confidence_segment_threshold,
            file_store_ids=file_store_ids,
            file_store_name=file_store_name,
        )

        process_request.additional_properties = d
        return process_request

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
