from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="EvaluationRequest")


@_attrs_define
class EvaluationRequest:
    """Request to start an evaluation job.

    Attributes:
        model_id (str): HuggingFace model ID to evaluate. Supported model families: Whisper (openai/whisper-tiny,
            openai/whisper-base, openai/whisper-small, openai/whisper-medium, openai/whisper-large-v3-turbo, openai/whisper-
            large-v3, leduckhai/MultiMed-ST/asr/whisper-small-english), Moonshine (UsefulSensors/moonshine-tiny,
            UsefulSensors/moonshine-base, plus language-specific variants), Voxtral (mistralai/Voxtral-Mini-3B-2507), Qwen
            ASR (Qwen/Qwen3-ASR-0.6B, Qwen/Qwen3-ASR-1.7B), Parakeet (nvidia/parakeet-tdt-0.6b-v3), Canary
            (nvidia/canary-1b-v2), OmniASR (facebook/omniASR-LLM-7B, inference only), VibeVoice (microsoft/VibeVoice-ASR-HF,
            inference only), Cohere Transcribe (CohereLabs/cohere-transcribe-03-2026, inference only), MedASR
            (google/medasr, English medical domain, inference only), as well as fine-tuned models from any of the trainable
            families. Router models (e.g. fireworks/whisper-v3, deepgram/nova-3, google/gemini-2.5-pro) are also supported —
            see GET /api/v1/models?family=router for the full list.
        model_file_store_id (None | str | Unset): FileStore UUID containing model weights (S3). When provided, model is
            loaded from S3 instead of HuggingFace.
        dataset_id (None | str | Unset): HuggingFace dataset ID (e.g. 'Trelis/llm-lingo'). Mutually exclusive with
            parquet_url and file_store_id.
        parquet_url (list[str] | None | str | Unset): Presigned or public URL to a .parquet file containing evaluation
            data. Must have columns: 'audio' (bytes or path) and 'text' (reference transcript). Mutually exclusive with
            dataset_id and file_store_id. Also accepts a list of URLs for multi-shard parquet datasets.
        file_store_id (None | str | Unset): FileStore UUID for S3-backed evaluation dataset. Mutually exclusive with
            dataset_id and parquet_url.
        dataset_config (None | str | Unset):
        split (str | Unset):  Default: 'validation'.
        num_samples (int | Unset):  Default: 500.
        push_results (bool | None | Unset):
        private (bool | Unset):  Default: True.
        output_org (None | str | Unset):
        language (str | Unset): Language for ASR evaluation. Default 'auto' auto-detects for Whisper, Qwen, VibeVoice,
            Voxtral, and Router models. OmniASR and Cohere Transcribe require an explicit language (returns error if set to
            'auto'). Use a full language name (e.g., 'english', 'greek', 'french') to force a specific language. Use
            'multilingual' to read per-sample language from dataset 'language' column. Also controls WER/CER text
            normalization: Greek ('greek'/'el'/'ell') uses a Greek-specific normalizer (strips diacriticals, normalizes
            sigma variants). All other languages, including 'auto', use a generic Unicode-aware normalizer (lowercase, strip
            punctuation, preserve all scripts). Default: 'auto'.
        enable_timestamps (bool | Unset): Enable timestamp evaluation. Only applies to Whisper models with datasets
            containing a 'text_ts' column. Defaults to False. Default: False.
        normalizer (str | Unset): Text normalizer for WER/CER computation. Options: 'auto' (select based on language —
            e.g., Greek normalizer for Greek), 'generic' (Unicode-aware: lowercase, strip punctuation, preserve all
            scripts), 'whisper-english' (aggressive English normalizer — numbers, contractions, fillers, British spelling),
            'none' (no normalization — compare raw text), or a language name (e.g., 'greek'). Default: 'auto'.
        max_duration (float | Unset): Maximum audio duration in seconds. Samples longer than this are skipped during
            evaluation. Default 30s (Whisper/Moonshine architecture limit). Increase for models that support longer audio.
            Default: 30.0.
        router_max_concurrency (int | Unset): Max parallel requests to Trelis Router for proprietary ASR models. Lower
            this if your Router API key has a low requests-per-minute limit. Default: 16.
    """

    model_id: str
    model_file_store_id: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    parquet_url: list[str] | None | str | Unset = UNSET
    file_store_id: None | str | Unset = UNSET
    dataset_config: None | str | Unset = UNSET
    split: str | Unset = "validation"
    num_samples: int | Unset = 500
    push_results: bool | None | Unset = UNSET
    private: bool | Unset = True
    output_org: None | str | Unset = UNSET
    language: str | Unset = "auto"
    enable_timestamps: bool | Unset = False
    normalizer: str | Unset = "auto"
    max_duration: float | Unset = 30.0
    router_max_concurrency: int | Unset = 16

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id

        model_file_store_id: None | str | Unset
        if isinstance(self.model_file_store_id, Unset):
            model_file_store_id = UNSET
        else:
            model_file_store_id = self.model_file_store_id

        dataset_id: None | str | Unset
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        parquet_url: list[str] | None | str | Unset
        if isinstance(self.parquet_url, Unset):
            parquet_url = UNSET
        elif isinstance(self.parquet_url, list):
            parquet_url = self.parquet_url

        else:
            parquet_url = self.parquet_url

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

        language = self.language

        enable_timestamps = self.enable_timestamps

        normalizer = self.normalizer

        max_duration = self.max_duration

        router_max_concurrency = self.router_max_concurrency

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model_id": model_id,
            }
        )
        if model_file_store_id is not UNSET:
            field_dict["model_file_store_id"] = model_file_store_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if parquet_url is not UNSET:
            field_dict["parquet_url"] = parquet_url
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if dataset_config is not UNSET:
            field_dict["dataset_config"] = dataset_config
        if split is not UNSET:
            field_dict["split"] = split
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if push_results is not UNSET:
            field_dict["push_results"] = push_results
        if private is not UNSET:
            field_dict["private"] = private
        if output_org is not UNSET:
            field_dict["output_org"] = output_org
        if language is not UNSET:
            field_dict["language"] = language
        if enable_timestamps is not UNSET:
            field_dict["enable_timestamps"] = enable_timestamps
        if normalizer is not UNSET:
            field_dict["normalizer"] = normalizer
        if max_duration is not UNSET:
            field_dict["max_duration"] = max_duration
        if router_max_concurrency is not UNSET:
            field_dict["router_max_concurrency"] = router_max_concurrency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_id = d.pop("model_id")

        def _parse_model_file_store_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_file_store_id = _parse_model_file_store_id(d.pop("model_file_store_id", UNSET))

        def _parse_dataset_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_id = _parse_dataset_id(d.pop("dataset_id", UNSET))

        def _parse_parquet_url(data: object) -> list[str] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                parquet_url_type_1 = cast(list[str], data)

                return parquet_url_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | str | Unset, data)

        parquet_url = _parse_parquet_url(d.pop("parquet_url", UNSET))

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

        language = d.pop("language", UNSET)

        enable_timestamps = d.pop("enable_timestamps", UNSET)

        normalizer = d.pop("normalizer", UNSET)

        max_duration = d.pop("max_duration", UNSET)

        router_max_concurrency = d.pop("router_max_concurrency", UNSET)

        evaluation_request = cls(
            model_id=model_id,
            model_file_store_id=model_file_store_id,
            dataset_id=dataset_id,
            parquet_url=parquet_url,
            file_store_id=file_store_id,
            dataset_config=dataset_config,
            split=split,
            num_samples=num_samples,
            push_results=push_results,
            private=private,
            output_org=output_org,
            language=language,
            enable_timestamps=enable_timestamps,
            normalizer=normalizer,
            max_duration=max_duration,
            router_max_concurrency=router_max_concurrency,
        )

        return evaluation_request
