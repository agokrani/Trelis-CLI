from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.file_store_transcript_response_transcript_type import (
    FileStoreTranscriptResponseTranscriptType,
)
from typing import cast


T = TypeVar("T", bound="FileStoreTranscriptResponse")


@_attrs_define
class FileStoreTranscriptResponse:
    """Transcript content + paired audio presigned URL for a FileStore file.

    ``transcript_type`` is the canonical wire-format tag; the UI uses it to
    label the editor and the download button. Values correspond 1:1 to the
    file extensions ``.vtt``/``.srt``/``.txt`` — ``vtt_content`` is named
    historically; for SRT/TXT it carries the raw body of the respective
    format (no on-the-fly conversion).

        Attributes:
            stem (str):
            vtt_content (str):
            audio_url (None | str):
            transcript_type (FileStoreTranscriptResponseTranscriptType):
    """

    stem: str
    vtt_content: str
    audio_url: None | str
    transcript_type: FileStoreTranscriptResponseTranscriptType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        stem = self.stem

        vtt_content = self.vtt_content

        audio_url: None | str
        audio_url = self.audio_url

        transcript_type = self.transcript_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "stem": stem,
                "vtt_content": vtt_content,
                "audio_url": audio_url,
                "transcript_type": transcript_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stem = d.pop("stem")

        vtt_content = d.pop("vtt_content")

        def _parse_audio_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        audio_url = _parse_audio_url(d.pop("audio_url"))

        transcript_type = FileStoreTranscriptResponseTranscriptType(d.pop("transcript_type"))

        file_store_transcript_response = cls(
            stem=stem,
            vtt_content=vtt_content,
            audio_url=audio_url,
            transcript_type=transcript_type,
        )

        file_store_transcript_response.additional_properties = d
        return file_store_transcript_response

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
