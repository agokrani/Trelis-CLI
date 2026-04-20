from enum import Enum


class TrainingASRV2RequestLoraTarget(str, Enum):
    BOTH = "both"
    DECODER_ONLY = "decoder_only"

    def __str__(self) -> str:
        return str(self.value)
