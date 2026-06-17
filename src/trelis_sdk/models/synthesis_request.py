from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.synthesis_request_apply_text_normalization_type_0 import (
    SynthesisRequestApplyTextNormalizationType0,
)
from ..models.synthesis_request_engine import SynthesisRequestEngine
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="SynthesisRequest")


@_attrs_define
class SynthesisRequest:
    """v2 synthesis request — one input source, params grouped per §5.4.

    Attributes:
        model (str): TTS model id. Engine is auto-resolved from this unless `engine` is set.
        language (str): ISO 639-1 code. Required by Chatterbox; Orpheus/Piper accept 'en'/'auto'.
        input_ (None | str | Unset): Inline text (simple mode — single /v1/audio/speech call).
        file_store_id (None | str | Unset): FileStore containing raw_text / audio_text_pairs / chunked_dataset /
            transcribed_dataset.
        dataset_id (None | str | Unset): HuggingFace dataset id with a `text` column.
        split (str | Unset): Dataset split (HF or parquet). Default: 'test'.
        dataset_config (None | str | Unset): HF dataset config/subset name.
        num_samples (int | Unset): Row limit for batch input. Default: 500.
        reference_column (str | Unset): Reference column for CER scoring (defaults to prompt text). Default: 'text'.
        engine (SynthesisRequestEngine | Unset):  Default: SynthesisRequestEngine.AUTO.
        voice (str | Unset): Speaker name (engine-dependent). Default: 'default'.
        max_new_tokens (int | Unset):  Default: 2560.
        temperature (float | Unset):  Default: 0.7.
        top_p (float | Unset):  Default: 0.95.
        repetition_penalty (float | Unset):  Default: 1.1.
        apply_text_normalization (None | SynthesisRequestApplyTextNormalizationType0 | Unset):
        asr_model_id (None | str | Unset): Router ASR model for round-trip CER (e.g. fireworks/whisper-v3).
        router_max_concurrency (int | Unset):  Default: 16.
        filter_threshold (float | None | Unset): CER cutoff. Samples with CER > threshold go into the `dropped` sibling
            shard.
        chunk_size (int | Unset): Streaming chunk size — peak orchestrator memory is two chunks (§5.8). Default: 500.
        output_name (None | str | Unset): Output FileStore name; auto-generated if omitted.
    """

    model: str
    language: str
    input_: None | str | Unset = UNSET
    file_store_id: None | str | Unset = UNSET
    dataset_id: None | str | Unset = UNSET
    split: str | Unset = "test"
    dataset_config: None | str | Unset = UNSET
    num_samples: int | Unset = 500
    reference_column: str | Unset = "text"
    engine: SynthesisRequestEngine | Unset = SynthesisRequestEngine.AUTO
    voice: str | Unset = "default"
    max_new_tokens: int | Unset = 2560
    temperature: float | Unset = 0.7
    top_p: float | Unset = 0.95
    repetition_penalty: float | Unset = 1.1
    apply_text_normalization: None | SynthesisRequestApplyTextNormalizationType0 | Unset = UNSET
    asr_model_id: None | str | Unset = UNSET
    router_max_concurrency: int | Unset = 16
    filter_threshold: float | None | Unset = UNSET
    chunk_size: int | Unset = 500
    output_name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        model = self.model

        language = self.language

        input_: None | str | Unset
        if isinstance(self.input_, Unset):
            input_ = UNSET
        else:
            input_ = self.input_

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

        dataset_config: None | str | Unset
        if isinstance(self.dataset_config, Unset):
            dataset_config = UNSET
        else:
            dataset_config = self.dataset_config

        num_samples = self.num_samples

        reference_column = self.reference_column

        engine: str | Unset = UNSET
        if not isinstance(self.engine, Unset):
            engine = self.engine.value

        voice = self.voice

        max_new_tokens = self.max_new_tokens

        temperature = self.temperature

        top_p = self.top_p

        repetition_penalty = self.repetition_penalty

        apply_text_normalization: None | str | Unset
        if isinstance(self.apply_text_normalization, Unset):
            apply_text_normalization = UNSET
        elif isinstance(self.apply_text_normalization, SynthesisRequestApplyTextNormalizationType0):
            apply_text_normalization = self.apply_text_normalization.value
        else:
            apply_text_normalization = self.apply_text_normalization

        asr_model_id: None | str | Unset
        if isinstance(self.asr_model_id, Unset):
            asr_model_id = UNSET
        else:
            asr_model_id = self.asr_model_id

        router_max_concurrency = self.router_max_concurrency

        filter_threshold: float | None | Unset
        if isinstance(self.filter_threshold, Unset):
            filter_threshold = UNSET
        else:
            filter_threshold = self.filter_threshold

        chunk_size = self.chunk_size

        output_name: None | str | Unset
        if isinstance(self.output_name, Unset):
            output_name = UNSET
        else:
            output_name = self.output_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model": model,
                "language": language,
            }
        )
        if input_ is not UNSET:
            field_dict["input"] = input_
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if split is not UNSET:
            field_dict["split"] = split
        if dataset_config is not UNSET:
            field_dict["dataset_config"] = dataset_config
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if reference_column is not UNSET:
            field_dict["reference_column"] = reference_column
        if engine is not UNSET:
            field_dict["engine"] = engine
        if voice is not UNSET:
            field_dict["voice"] = voice
        if max_new_tokens is not UNSET:
            field_dict["max_new_tokens"] = max_new_tokens
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if repetition_penalty is not UNSET:
            field_dict["repetition_penalty"] = repetition_penalty
        if apply_text_normalization is not UNSET:
            field_dict["apply_text_normalization"] = apply_text_normalization
        if asr_model_id is not UNSET:
            field_dict["asr_model_id"] = asr_model_id
        if router_max_concurrency is not UNSET:
            field_dict["router_max_concurrency"] = router_max_concurrency
        if filter_threshold is not UNSET:
            field_dict["filter_threshold"] = filter_threshold
        if chunk_size is not UNSET:
            field_dict["chunk_size"] = chunk_size
        if output_name is not UNSET:
            field_dict["output_name"] = output_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model = d.pop("model")

        language = d.pop("language")

        def _parse_input_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        input_ = _parse_input_(d.pop("input", UNSET))

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

        def _parse_dataset_config(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_config = _parse_dataset_config(d.pop("dataset_config", UNSET))

        num_samples = d.pop("num_samples", UNSET)

        reference_column = d.pop("reference_column", UNSET)

        _engine = d.pop("engine", UNSET)
        engine: SynthesisRequestEngine | Unset
        if isinstance(_engine, Unset):
            engine = UNSET
        else:
            engine = SynthesisRequestEngine(_engine)

        voice = d.pop("voice", UNSET)

        max_new_tokens = d.pop("max_new_tokens", UNSET)

        temperature = d.pop("temperature", UNSET)

        top_p = d.pop("top_p", UNSET)

        repetition_penalty = d.pop("repetition_penalty", UNSET)

        def _parse_apply_text_normalization(
            data: object,
        ) -> None | SynthesisRequestApplyTextNormalizationType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                apply_text_normalization_type_0 = SynthesisRequestApplyTextNormalizationType0(data)

                return apply_text_normalization_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SynthesisRequestApplyTextNormalizationType0 | Unset, data)

        apply_text_normalization = _parse_apply_text_normalization(
            d.pop("apply_text_normalization", UNSET)
        )

        def _parse_asr_model_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        asr_model_id = _parse_asr_model_id(d.pop("asr_model_id", UNSET))

        router_max_concurrency = d.pop("router_max_concurrency", UNSET)

        def _parse_filter_threshold(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        filter_threshold = _parse_filter_threshold(d.pop("filter_threshold", UNSET))

        chunk_size = d.pop("chunk_size", UNSET)

        def _parse_output_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_name = _parse_output_name(d.pop("output_name", UNSET))

        synthesis_request = cls(
            model=model,
            language=language,
            input_=input_,
            file_store_id=file_store_id,
            dataset_id=dataset_id,
            split=split,
            dataset_config=dataset_config,
            num_samples=num_samples,
            reference_column=reference_column,
            engine=engine,
            voice=voice,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            apply_text_normalization=apply_text_normalization,
            asr_model_id=asr_model_id,
            router_max_concurrency=router_max_concurrency,
            filter_threshold=filter_threshold,
            chunk_size=chunk_size,
            output_name=output_name,
        )

        return synthesis_request
