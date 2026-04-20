from enum import Enum


class TrainingTTSV2RequestTrainingVariant(str, Enum):
    FINETUNE = "finetune"
    ZSVC = "zsvc"

    def __str__(self) -> str:
        return str(self.value)
