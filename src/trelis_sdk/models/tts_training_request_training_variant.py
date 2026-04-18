from enum import Enum


class TTSTrainingRequestTrainingVariant(str, Enum):
    FINETUNE = "finetune"
    ZSVC = "zsvc"

    def __str__(self) -> str:
        return str(self.value)
