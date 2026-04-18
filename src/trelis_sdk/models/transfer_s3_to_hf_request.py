from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.transfer_s3_to_hf_request_repo_type import TransferS3ToHfRequestRepoType
from ..types import UNSET, Unset


T = TypeVar("T", bound="TransferS3ToHfRequest")


@_attrs_define
class TransferS3ToHfRequest:
    """Push an S3 FileStore to a HuggingFace repo.

    Attributes:
        repo_id (str): Destination HF repo ID (e.g. org/model-name)
        repo_type (TransferS3ToHfRequestRepoType | Unset): Type of HF repo Default:
            TransferS3ToHfRequestRepoType.DATASET.
    """

    repo_id: str
    repo_type: TransferS3ToHfRequestRepoType | Unset = TransferS3ToHfRequestRepoType.DATASET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        repo_id = self.repo_id

        repo_type: str | Unset = UNSET
        if not isinstance(self.repo_type, Unset):
            repo_type = self.repo_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "repo_id": repo_id,
            }
        )
        if repo_type is not UNSET:
            field_dict["repo_type"] = repo_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repo_id = d.pop("repo_id")

        _repo_type = d.pop("repo_type", UNSET)
        repo_type: TransferS3ToHfRequestRepoType | Unset
        if isinstance(_repo_type, Unset):
            repo_type = UNSET
        else:
            repo_type = TransferS3ToHfRequestRepoType(_repo_type)

        transfer_s3_to_hf_request = cls(
            repo_id=repo_id,
            repo_type=repo_type,
        )

        transfer_s3_to_hf_request.additional_properties = d
        return transfer_s3_to_hf_request

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
