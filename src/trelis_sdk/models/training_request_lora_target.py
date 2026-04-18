from enum import Enum


class TrainingRequestLoraTarget(str, Enum):
    BOTH = "both"
    DECODER_ONLY = "decoder_only"

    def __str__(self) -> str:
        return str(self.value)
