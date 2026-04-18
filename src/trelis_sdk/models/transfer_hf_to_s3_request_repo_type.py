from enum import Enum


class TransferHfToS3RequestRepoType(str, Enum):
    DATASET = "dataset"
    MODEL = "model"

    def __str__(self) -> str:
        return str(self.value)
