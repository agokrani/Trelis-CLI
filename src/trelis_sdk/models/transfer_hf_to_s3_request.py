from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transfer_hf_to_s3_request_repo_type import TransferHfToS3RequestRepoType
from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TransferHfToS3Request")


@_attrs_define
class TransferHfToS3Request:
    """Import a HuggingFace repo (model or dataset) into a new S3 FileStore.

    Attributes:
        repo_id (str): HuggingFace repo ID (e.g. org/model-name)
        repo_type (TransferHfToS3RequestRepoType | Unset): Type of HF repo Default:
            TransferHfToS3RequestRepoType.DATASET.
        revision (None | str | Unset): Branch, tag, or commit hash
        name (None | str | Unset): Name for the new FileStore
    """

    repo_id: str
    repo_type: TransferHfToS3RequestRepoType | Unset = TransferHfToS3RequestRepoType.DATASET
    revision: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        repo_id = self.repo_id

        repo_type: str | Unset = UNSET
        if not isinstance(self.repo_type, Unset):
            repo_type = self.repo_type.value

        revision: None | str | Unset
        if isinstance(self.revision, Unset):
            revision = UNSET
        else:
            revision = self.revision

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "repo_id": repo_id,
            }
        )
        if repo_type is not UNSET:
            field_dict["repo_type"] = repo_type
        if revision is not UNSET:
            field_dict["revision"] = revision
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repo_id = d.pop("repo_id")

        _repo_type = d.pop("repo_type", UNSET)
        repo_type: TransferHfToS3RequestRepoType | Unset
        if isinstance(_repo_type, Unset):
            repo_type = UNSET
        else:
            repo_type = TransferHfToS3RequestRepoType(_repo_type)

        def _parse_revision(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        revision = _parse_revision(d.pop("revision", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        transfer_hf_to_s3_request = cls(
            repo_id=repo_id,
            repo_type=repo_type,
            revision=revision,
            name=name,
        )

        transfer_hf_to_s3_request.additional_properties = d
        return transfer_hf_to_s3_request

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
