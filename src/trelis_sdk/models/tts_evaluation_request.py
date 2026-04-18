from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.tts_evaluation_request_apply_text_normalization_type_0 import (
    TTSEvaluationRequestApplyTextNormalizationType0,
)
from ..models.tts_evaluation_request_normalizer import TTSEvaluationRequestNormalizer
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TTSEvaluationRequest")


@_attrs_define
class TTSEvaluationRequest:
    """Request to start a TTS evaluation job.

    Attributes:
        model_id (str): TTS model to evaluate. Use GET /api/v1/models?modality=tts for available base models. Formats by
            engine type: Orpheus — HuggingFace model ID (e.g. 'unsloth/orpheus-3b-0.1-ft'). Chatterbox — HuggingFace model
            ID (e.g. 'ResembleAI/chatterbox' or a fine-tuned repo). Piper — HuggingFace model ID (e.g. 'Trelis/piper-en-us-
            lessac-high') or checkpoint path (e.g. 'rhasspy/piper-checkpoints:en/en_GB/alan/medium'). Kokoro — literal
            string 'kokoro' (uses kokoro_voice param for voice selection). Router TTS — provider model ID (e.g.
            'elevenlabs/eleven-multilingual-v2'); requires Router API key.
        prompts (list[str] | None | Unset): Text prompts to generate audio for. If not provided, uses dataset_id or
            default prompts.
        dataset_id (None | str | Unset): HF dataset with 'text' column to source prompts from. Mutually exclusive with
            file_store_id.
        file_store_id (None | str | Unset): FileStore UUID to source prompts from (must contain parquet files with
            'text' column). Mutually exclusive with dataset_id.
        dataset_config (None | str | Unset):
        split (str | Unset):  Default: 'validation'.
        num_samples (int | Unset):  Default: 500.
        max_new_tokens (int | Unset):  Default: 2560.
        temperature (float | Unset):  Default: 0.7.
        top_p (float | Unset):  Default: 0.95.
        repetition_penalty (float | Unset):  Default: 1.1.
        speaker_name (str | Unset):  Default: 'speaker'.
        push_results (bool | None | Unset):
        private (bool | Unset):  Default: True.
        output_org (None | str | Unset):
        output_name (None | str | Unset):
        asr_model_id (None | str | Unset): Optional Router ASR model for round-trip evaluation (e.g.
            'fireworks/whisper-v3', 'assemblyai/universal-3-pro'). Only Router models are supported. Transcribes generated
            audio back to text and computes WER/CER.
        language (str | Unset): Language code. Use 'auto' for Orpheus/Kokoro/Router models (ASR auto-detection).
            Chatterbox and Piper require an explicit ISO 639-1 code (e.g. 'en', 'el', 'fr'). Default: 'auto'.
        tts_model_type (str | Unset): TTS model type hint. Accepted values: 'orpheus', 'chatterbox', 'piper', 'kokoro',
            'auto'. For Router TTS models (e.g. 'openai/gpt-4o-mini-tts', 'cartesia/sonic-3', 'google/gemini-2.5-flash-tts',
            'google/gemini-2.5-pro-tts', 'elevenlabs/eleven-multilingual-v2') set to 'auto' — the model type is detected
            automatically from model_id. Default: 'auto'.
        kokoro_voice (str | Unset): Voice name for Kokoro TTS (e.g. 'af_heart', 'am_echo'). Only used when
            model_id='kokoro'. Default: 'af_heart'.
        reference_column (None | str | Unset): Dataset column containing the ASR transcription of the ground-truth voice
            recording, used as the CER/WER reference instead of the 'text' column. Useful when the speaker didn't read the
            prompt verbatim — CER is then computed against what was actually said rather than the original text. Defaults to
            'reference_asr' if that column exists in the dataset; set explicitly to use a different column name.
        normalizer (TTSEvaluationRequestNormalizer | Unset): Text normalizer for ASR round-trip WER/CER computation.
            Options: 'auto' (select based on language — e.g., Greek normalizer for Greek), 'generic' (Unicode-aware:
            lowercase, strip punctuation, preserve all scripts), 'whisper-english' (aggressive English normalizer — numbers,
            contractions, fillers, British spelling), 'none' (no normalization — compare raw text), or a language name
            (e.g., 'greek'). Only used when asr_model_id is set. Default: TTSEvaluationRequestNormalizer.AUTO.
        apply_text_normalization (None | TTSEvaluationRequestApplyTextNormalizationType0 | Unset): Text normalization
            for ElevenLabs TTS: 'auto' (default), 'on' (always normalize numbers/units), 'off' (read as-is). Only applies to
            ElevenLabs models via Router.
        router_max_concurrency (int | Unset): Max parallel requests to Trelis Router for ASR round-trip and TTS
            synthesis. Lower this if your Router API key has a low requests-per-minute limit. Default: 16.
    """

    model_id: str
    prompts: list[str] | None | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    file_store_id: None | str | Unset = UNSET
    dataset_config: None | str | Unset = UNSET
    split: str | Unset = "validation"
    num_samples: int | Unset = 500
    max_new_tokens: int | Unset = 2560
    temperature: float | Unset = 0.7
    top_p: float | Unset = 0.95
    repetition_penalty: float | Unset = 1.1
    speaker_name: str | Unset = "speaker"
    push_results: bool | None | Unset = UNSET
    private: bool | Unset = True
    output_org: None | str | Unset = UNSET
    output_name: None | str | Unset = UNSET
    asr_model_id: None | str | Unset = UNSET
    language: str | Unset = "auto"
    tts_model_type: str | Unset = "auto"
    kokoro_voice: str | Unset = "af_heart"
    reference_column: None | str | Unset = UNSET
    normalizer: TTSEvaluationRequestNormalizer | Unset = TTSEvaluationRequestNormalizer.AUTO
    apply_text_normalization: None | TTSEvaluationRequestApplyTextNormalizationType0 | Unset = UNSET
    router_max_concurrency: int | Unset = 16

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id

        prompts: list[str] | None | Unset
        if isinstance(self.prompts, Unset):
            prompts = UNSET
        elif isinstance(self.prompts, list):
            prompts = self.prompts

        else:
            prompts = self.prompts

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

        dataset_config: None | str | Unset
        if isinstance(self.dataset_config, Unset):
            dataset_config = UNSET
        else:
            dataset_config = self.dataset_config

        split = self.split

        num_samples = self.num_samples

        max_new_tokens = self.max_new_tokens

        temperature = self.temperature

        top_p = self.top_p

        repetition_penalty = self.repetition_penalty

        speaker_name = self.speaker_name

        push_results: bool | None | Unset
        if isinstance(self.push_results, Unset):
            push_results = UNSET
        else:
            push_results = self.push_results

        private = self.private

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

        asr_model_id: None | str | Unset
        if isinstance(self.asr_model_id, Unset):
            asr_model_id = UNSET
        else:
            asr_model_id = self.asr_model_id

        language = self.language

        tts_model_type = self.tts_model_type

        kokoro_voice = self.kokoro_voice

        reference_column: None | str | Unset
        if isinstance(self.reference_column, Unset):
            reference_column = UNSET
        else:
            reference_column = self.reference_column

        normalizer: str | Unset = UNSET
        if not isinstance(self.normalizer, Unset):
            normalizer = self.normalizer.value

        apply_text_normalization: None | str | Unset
        if isinstance(self.apply_text_normalization, Unset):
            apply_text_normalization = UNSET
        elif isinstance(
            self.apply_text_normalization, TTSEvaluationRequestApplyTextNormalizationType0
        ):
            apply_text_normalization = self.apply_text_normalization.value
        else:
            apply_text_normalization = self.apply_text_normalization

        router_max_concurrency = self.router_max_concurrency

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model_id": model_id,
            }
        )
        if prompts is not UNSET:
            field_dict["prompts"] = prompts
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if dataset_config is not UNSET:
            field_dict["dataset_config"] = dataset_config
        if split is not UNSET:
            field_dict["split"] = split
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if max_new_tokens is not UNSET:
            field_dict["max_new_tokens"] = max_new_tokens
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if repetition_penalty is not UNSET:
            field_dict["repetition_penalty"] = repetition_penalty
        if speaker_name is not UNSET:
            field_dict["speaker_name"] = speaker_name
        if push_results is not UNSET:
            field_dict["push_results"] = push_results
        if private is not UNSET:
            field_dict["private"] = private
        if output_org is not UNSET:
            field_dict["output_org"] = output_org
        if output_name is not UNSET:
            field_dict["output_name"] = output_name
        if asr_model_id is not UNSET:
            field_dict["asr_model_id"] = asr_model_id
        if language is not UNSET:
            field_dict["language"] = language
        if tts_model_type is not UNSET:
            field_dict["tts_model_type"] = tts_model_type
        if kokoro_voice is not UNSET:
            field_dict["kokoro_voice"] = kokoro_voice
        if reference_column is not UNSET:
            field_dict["reference_column"] = reference_column
        if normalizer is not UNSET:
            field_dict["normalizer"] = normalizer
        if apply_text_normalization is not UNSET:
            field_dict["apply_text_normalization"] = apply_text_normalization
        if router_max_concurrency is not UNSET:
            field_dict["router_max_concurrency"] = router_max_concurrency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_id = d.pop("model_id")

        def _parse_prompts(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                prompts_type_0 = cast(list[str], data)

                return prompts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        prompts = _parse_prompts(d.pop("prompts", UNSET))

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

        def _parse_dataset_config(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_config = _parse_dataset_config(d.pop("dataset_config", UNSET))

        split = d.pop("split", UNSET)

        num_samples = d.pop("num_samples", UNSET)

        max_new_tokens = d.pop("max_new_tokens", UNSET)

        temperature = d.pop("temperature", UNSET)

        top_p = d.pop("top_p", UNSET)

        repetition_penalty = d.pop("repetition_penalty", UNSET)

        speaker_name = d.pop("speaker_name", UNSET)

        def _parse_push_results(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        push_results = _parse_push_results(d.pop("push_results", UNSET))

        private = d.pop("private", UNSET)

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

        def _parse_asr_model_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        asr_model_id = _parse_asr_model_id(d.pop("asr_model_id", UNSET))

        language = d.pop("language", UNSET)

        tts_model_type = d.pop("tts_model_type", UNSET)

        kokoro_voice = d.pop("kokoro_voice", UNSET)

        def _parse_reference_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reference_column = _parse_reference_column(d.pop("reference_column", UNSET))

        _normalizer = d.pop("normalizer", UNSET)
        normalizer: TTSEvaluationRequestNormalizer | Unset
        if isinstance(_normalizer, Unset):
            normalizer = UNSET
        else:
            normalizer = TTSEvaluationRequestNormalizer(_normalizer)

        def _parse_apply_text_normalization(
            data: object,
        ) -> None | TTSEvaluationRequestApplyTextNormalizationType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                apply_text_normalization_type_0 = TTSEvaluationRequestApplyTextNormalizationType0(
                    data
                )

                return apply_text_normalization_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TTSEvaluationRequestApplyTextNormalizationType0 | Unset, data)

        apply_text_normalization = _parse_apply_text_normalization(
            d.pop("apply_text_normalization", UNSET)
        )

        router_max_concurrency = d.pop("router_max_concurrency", UNSET)

        tts_evaluation_request = cls(
            model_id=model_id,
            prompts=prompts,
            dataset_id=dataset_id,
            file_store_id=file_store_id,
            dataset_config=dataset_config,
            split=split,
            num_samples=num_samples,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            speaker_name=speaker_name,
            push_results=push_results,
            private=private,
            output_org=output_org,
            output_name=output_name,
            asr_model_id=asr_model_id,
            language=language,
            tts_model_type=tts_model_type,
            kokoro_voice=kokoro_voice,
            reference_column=reference_column,
            normalizer=normalizer,
            apply_text_normalization=apply_text_normalization,
            router_max_concurrency=router_max_concurrency,
        )

        return tts_evaluation_request
