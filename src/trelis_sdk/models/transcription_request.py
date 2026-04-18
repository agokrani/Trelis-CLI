from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transcription_request_output_target import TranscriptionRequestOutputTarget
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TranscriptionRequest")


@_attrs_define
class TranscriptionRequest:
    """POST /api/v1/transcription request body (§4.6).

    Required: ``model_id``, ``language``.
    Exactly one input source: ``dataset_id``, ``parquet_urls``, or
    ``file_store_id``.

    Project-scoped parameters — NEVER in the request body per §4.6:
    ``hf_token``, ``router_api_key``, ``s3_config``, ``output_target``.
    Those arrive via the project's stored credentials + settings; a
    request body that tries to override them is rejected by the
    strict (``extra="forbid"``) config below.

        Attributes:
            model_id (str):
            language (str):
            dataset_id (None | str | Unset):
            dataset_split (str | Unset):  Default: 'test'.
            dataset_config (None | str | Unset):
            parquet_urls (list[str] | None | Unset):
            file_store_id (None | str | Unset):
            num_samples (int | None | Unset):
            max_duration (float | Unset):  Default: 30.0.
            enable_timestamps (bool | Unset):  Default: False.
            reference_column (None | str | Unset):
            entities_column (None | str | Unset):
            normalizer (str | Unset):  Default: 'auto'.
            filter_threshold (float | None | Unset):
            save_dropped (bool | Unset):  Default: True.
            output_target (TranscriptionRequestOutputTarget | Unset):  Default: TranscriptionRequestOutputTarget.S3.
            output_dataset_name (None | str | Unset):
            chunk_size (int | Unset):  Default: 500.
            router_max_concurrency (int | Unset):  Default: 16.
    """

    model_id: str
    language: str
    dataset_id: None | str | Unset = UNSET
    dataset_split: str | Unset = "test"
    dataset_config: None | str | Unset = UNSET
    parquet_urls: list[str] | None | Unset = UNSET
    file_store_id: None | str | Unset = UNSET
    num_samples: int | None | Unset = UNSET
    max_duration: float | Unset = 30.0
    enable_timestamps: bool | Unset = False
    reference_column: None | str | Unset = UNSET
    entities_column: None | str | Unset = UNSET
    normalizer: str | Unset = "auto"
    filter_threshold: float | None | Unset = UNSET
    save_dropped: bool | Unset = True
    output_target: TranscriptionRequestOutputTarget | Unset = TranscriptionRequestOutputTarget.S3
    output_dataset_name: None | str | Unset = UNSET
    chunk_size: int | Unset = 500
    router_max_concurrency: int | Unset = 16

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id

        language = self.language

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

        parquet_urls: list[str] | None | Unset
        if isinstance(self.parquet_urls, Unset):
            parquet_urls = UNSET
        elif isinstance(self.parquet_urls, list):
            parquet_urls = self.parquet_urls

        else:
            parquet_urls = self.parquet_urls

        file_store_id: None | str | Unset
        if isinstance(self.file_store_id, Unset):
            file_store_id = UNSET
        else:
            file_store_id = self.file_store_id

        num_samples: int | None | Unset
        if isinstance(self.num_samples, Unset):
            num_samples = UNSET
        else:
            num_samples = self.num_samples

        max_duration = self.max_duration

        enable_timestamps = self.enable_timestamps

        reference_column: None | str | Unset
        if isinstance(self.reference_column, Unset):
            reference_column = UNSET
        else:
            reference_column = self.reference_column

        entities_column: None | str | Unset
        if isinstance(self.entities_column, Unset):
            entities_column = UNSET
        else:
            entities_column = self.entities_column

        normalizer = self.normalizer

        filter_threshold: float | None | Unset
        if isinstance(self.filter_threshold, Unset):
            filter_threshold = UNSET
        else:
            filter_threshold = self.filter_threshold

        save_dropped = self.save_dropped

        output_target: str | Unset = UNSET
        if not isinstance(self.output_target, Unset):
            output_target = self.output_target.value

        output_dataset_name: None | str | Unset
        if isinstance(self.output_dataset_name, Unset):
            output_dataset_name = UNSET
        else:
            output_dataset_name = self.output_dataset_name

        chunk_size = self.chunk_size

        router_max_concurrency = self.router_max_concurrency

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model_id": model_id,
                "language": language,
            }
        )
        if dataset_id is not UNSET:
            field_dict["dataset_id"] = dataset_id
        if dataset_split is not UNSET:
            field_dict["dataset_split"] = dataset_split
        if dataset_config is not UNSET:
            field_dict["dataset_config"] = dataset_config
        if parquet_urls is not UNSET:
            field_dict["parquet_urls"] = parquet_urls
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if max_duration is not UNSET:
            field_dict["max_duration"] = max_duration
        if enable_timestamps is not UNSET:
            field_dict["enable_timestamps"] = enable_timestamps
        if reference_column is not UNSET:
            field_dict["reference_column"] = reference_column
        if entities_column is not UNSET:
            field_dict["entities_column"] = entities_column
        if normalizer is not UNSET:
            field_dict["normalizer"] = normalizer
        if filter_threshold is not UNSET:
            field_dict["filter_threshold"] = filter_threshold
        if save_dropped is not UNSET:
            field_dict["save_dropped"] = save_dropped
        if output_target is not UNSET:
            field_dict["output_target"] = output_target
        if output_dataset_name is not UNSET:
            field_dict["output_dataset_name"] = output_dataset_name
        if chunk_size is not UNSET:
            field_dict["chunk_size"] = chunk_size
        if router_max_concurrency is not UNSET:
            field_dict["router_max_concurrency"] = router_max_concurrency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_id = d.pop("model_id")

        language = d.pop("language")

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

        def _parse_parquet_urls(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                parquet_urls_type_0 = cast(list[str], data)

                return parquet_urls_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        parquet_urls = _parse_parquet_urls(d.pop("parquet_urls", UNSET))

        def _parse_file_store_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_store_id = _parse_file_store_id(d.pop("file_store_id", UNSET))

        def _parse_num_samples(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_samples = _parse_num_samples(d.pop("num_samples", UNSET))

        max_duration = d.pop("max_duration", UNSET)

        enable_timestamps = d.pop("enable_timestamps", UNSET)

        def _parse_reference_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reference_column = _parse_reference_column(d.pop("reference_column", UNSET))

        def _parse_entities_column(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        entities_column = _parse_entities_column(d.pop("entities_column", UNSET))

        normalizer = d.pop("normalizer", UNSET)

        def _parse_filter_threshold(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        filter_threshold = _parse_filter_threshold(d.pop("filter_threshold", UNSET))

        save_dropped = d.pop("save_dropped", UNSET)

        _output_target = d.pop("output_target", UNSET)
        output_target: TranscriptionRequestOutputTarget | Unset
        if isinstance(_output_target, Unset):
            output_target = UNSET
        else:
            output_target = TranscriptionRequestOutputTarget(_output_target)

        def _parse_output_dataset_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_dataset_name = _parse_output_dataset_name(d.pop("output_dataset_name", UNSET))

        chunk_size = d.pop("chunk_size", UNSET)

        router_max_concurrency = d.pop("router_max_concurrency", UNSET)

        transcription_request = cls(
            model_id=model_id,
            language=language,
            dataset_id=dataset_id,
            dataset_split=dataset_split,
            dataset_config=dataset_config,
            parquet_urls=parquet_urls,
            file_store_id=file_store_id,
            num_samples=num_samples,
            max_duration=max_duration,
            enable_timestamps=enable_timestamps,
            reference_column=reference_column,
            entities_column=entities_column,
            normalizer=normalizer,
            filter_threshold=filter_threshold,
            save_dropped=save_dropped,
            output_target=output_target,
            output_dataset_name=output_dataset_name,
            chunk_size=chunk_size,
            router_max_concurrency=router_max_concurrency,
        )

        return transcription_request
