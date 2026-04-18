from enum import Enum


class TransferS3ToHfRequestRepoType(str, Enum):
    DATASET = "dataset"
    MODEL = "model"

    def __str__(self) -> str:
        return str(self.value)
