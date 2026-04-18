from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.file_store_tts_request_engine_type_0 import FileStoreTTSRequestEngineType0
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="FileStoreTTSRequest")


@_attrs_define
class FileStoreTTSRequest:
    """
    Attributes:
        model_id (str | Unset):  Default: 'unsloth/orpheus-3b-0.1-ft'.
        engine (FileStoreTTSRequestEngineType0 | None | Unset):
        speaker_name (str | Unset):  Default: 'tara'.
        max_new_tokens (int | Unset):  Default: 2560.
        language (None | str | Unset):
        kokoro_voice (str | Unset):  Default: 'af_heart'.
    """

    model_id: str | Unset = "unsloth/orpheus-3b-0.1-ft"
    engine: FileStoreTTSRequestEngineType0 | None | Unset = UNSET
    speaker_name: str | Unset = "tara"
    max_new_tokens: int | Unset = 2560
    language: None | str | Unset = UNSET
    kokoro_voice: str | Unset = "af_heart"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id

        engine: None | str | Unset
        if isinstance(self.engine, Unset):
            engine = UNSET
        elif isinstance(self.engine, FileStoreTTSRequestEngineType0):
            engine = self.engine.value
        else:
            engine = self.engine

        speaker_name = self.speaker_name

        max_new_tokens = self.max_new_tokens

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        kokoro_voice = self.kokoro_voice

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if engine is not UNSET:
            field_dict["engine"] = engine
        if speaker_name is not UNSET:
            field_dict["speaker_name"] = speaker_name
        if max_new_tokens is not UNSET:
            field_dict["max_new_tokens"] = max_new_tokens
        if language is not UNSET:
            field_dict["language"] = language
        if kokoro_voice is not UNSET:
            field_dict["kokoro_voice"] = kokoro_voice

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        model_id = d.pop("model_id", UNSET)

        def _parse_engine(data: object) -> FileStoreTTSRequestEngineType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                engine_type_0 = FileStoreTTSRequestEngineType0(data)

                return engine_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FileStoreTTSRequestEngineType0 | None | Unset, data)

        engine = _parse_engine(d.pop("engine", UNSET))

        speaker_name = d.pop("speaker_name", UNSET)

        max_new_tokens = d.pop("max_new_tokens", UNSET)

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        kokoro_voice = d.pop("kokoro_voice", UNSET)

        file_store_tts_request = cls(
            model_id=model_id,
            engine=engine,
            speaker_name=speaker_name,
            max_new_tokens=max_new_tokens,
            language=language,
            kokoro_voice=kokoro_voice,
        )

        file_store_tts_request.additional_properties = d
        return file_store_tts_request

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
