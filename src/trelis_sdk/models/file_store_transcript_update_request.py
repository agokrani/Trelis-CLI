from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.file_store_transcript_update_request_transcript_type import (
    FileStoreTranscriptUpdateRequestTranscriptType,
)
from ..types import UNSET, Unset


T = TypeVar("T", bound="FileStoreTranscriptUpdateRequest")


@_attrs_define
class FileStoreTranscriptUpdateRequest:
    """Editor-submitted transcript content for a given stem.

    ``transcript_type`` selects the target file extension + Content-Type:
    ``vtt`` → ``{stem}.vtt`` (text/vtt), ``srt`` → ``{stem}.srt`` (text/plain),
    ``txt`` → ``{stem}.txt`` (text/plain). Sibling extensions for the same
    stem are cleaned up on successful PUT so exactly one transcript per stem
    remains on disk.

        Attributes:
            vtt_content (str):
            transcript_type (FileStoreTranscriptUpdateRequestTranscriptType | Unset):  Default:
                FileStoreTranscriptUpdateRequestTranscriptType.VTT.
    """

    vtt_content: str
    transcript_type: FileStoreTranscriptUpdateRequestTranscriptType | Unset = (
        FileStoreTranscriptUpdateRequestTranscriptType.VTT
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        vtt_content = self.vtt_content

        transcript_type: str | Unset = UNSET
        if not isinstance(self.transcript_type, Unset):
            transcript_type = self.transcript_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vtt_content": vtt_content,
            }
        )
        if transcript_type is not UNSET:
            field_dict["transcript_type"] = transcript_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        vtt_content = d.pop("vtt_content")

        _transcript_type = d.pop("transcript_type", UNSET)
        transcript_type: FileStoreTranscriptUpdateRequestTranscriptType | Unset
        if isinstance(_transcript_type, Unset):
            transcript_type = UNSET
        else:
            transcript_type = FileStoreTranscriptUpdateRequestTranscriptType(_transcript_type)

        file_store_transcript_update_request = cls(
            vtt_content=vtt_content,
            transcript_type=transcript_type,
        )

        file_store_transcript_update_request.additional_properties = d
        return file_store_transcript_update_request

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
