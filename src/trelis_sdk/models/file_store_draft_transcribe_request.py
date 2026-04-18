from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.file_store_draft_transcribe_request_audio_cleaning import (
    FileStoreDraftTranscribeRequestAudioCleaning,
)
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="FileStoreDraftTranscribeRequest")


@_attrs_define
class FileStoreDraftTranscribeRequest:
    """
    Attributes:
        model_id (str | Unset): ASR model to use for transcription. Pass a HuggingFace model ID (e.g. 'openai/whisper-
            large-v3-turbo') for GPU transcription, or a Router model directly (e.g. 'google/gemini-2.5-flash',
            'fireworks/whisper-v3'). For the legacy router convention, pass 'router' here and set router_model. Default:
            'openai/whisper-large-v3'.
        router_model (None | str | Unset): Deprecated — pass the router model directly in model_id instead. Only used
            when model_id='router' (legacy convention).
        language (None | str | Unset):
        vad_threshold (float | Unset):  Default: 0.5.
        audio_cleaning (FileStoreDraftTranscribeRequestAudioCleaning | Unset):  Default:
            FileStoreDraftTranscribeRequestAudioCleaning.NONE.
        filenames (list[str] | None | Unset):
        router_max_concurrency (int | Unset):  Default: 16.
    """

    model_id: str | Unset = "openai/whisper-large-v3"
    router_model: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    vad_threshold: float | Unset = 0.5
    audio_cleaning: FileStoreDraftTranscribeRequestAudioCleaning | Unset = (
        FileStoreDraftTranscribeRequestAudioCleaning.NONE
    )
    filenames: list[str] | None | Unset = UNSET
    router_max_concurrency: int | Unset = 16
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id

        router_model: None | str | Unset
        if isinstance(self.router_model, Unset):
            router_model = UNSET
        else:
            router_model = self.router_model

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        vad_threshold = self.vad_threshold

        audio_cleaning: str | Unset = UNSET
        if not isinstance(self.audio_cleaning, Unset):
            audio_cleaning = self.audio_cleaning.value

        filenames: list[str] | None | Unset
        if isinstance(self.filenames, Unset):
            filenames = UNSET
        elif isinstance(self.filenames, list):
            filenames = self.filenames

        else:
            filenames = self.filenames

        router_max_concurrency = self.router_max_concurrency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if router_model is not UNSET:
            field_dict["router_model"] = router_model
        if language is not UNSET:
            field_dict["language"] = language
        if vad_threshold is not UNSET:
            field_dict["vad_threshold"] = vad_threshold
        if audio_cleaning is not UNSET:
            field_dict["audio_cleaning"] = audio_cleaning
        if filenames is not UNSET:
            field_dict["filenames"] = filenames
        if router_max_concurrency is not UNSET:
            field_dict["router_max_concurrency"] = router_max_concurrency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_id = d.pop("model_id", UNSET)

        def _parse_router_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        router_model = _parse_router_model(d.pop("router_model", UNSET))

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        vad_threshold = d.pop("vad_threshold", UNSET)

        _audio_cleaning = d.pop("audio_cleaning", UNSET)
        audio_cleaning: FileStoreDraftTranscribeRequestAudioCleaning | Unset
        if isinstance(_audio_cleaning, Unset):
            audio_cleaning = UNSET
        else:
            audio_cleaning = FileStoreDraftTranscribeRequestAudioCleaning(_audio_cleaning)

        def _parse_filenames(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filenames_type_0 = cast(list[str], data)

                return filenames_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        filenames = _parse_filenames(d.pop("filenames", UNSET))

        router_max_concurrency = d.pop("router_max_concurrency", UNSET)

        file_store_draft_transcribe_request = cls(
            model_id=model_id,
            router_model=router_model,
            language=language,
            vad_threshold=vad_threshold,
            audio_cleaning=audio_cleaning,
            filenames=filenames,
            router_max_concurrency=router_max_concurrency,
        )

        file_store_draft_transcribe_request.additional_properties = d
        return file_store_draft_transcribe_request

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
