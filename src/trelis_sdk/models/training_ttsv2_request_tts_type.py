from enum import Enum


class TrainingTTSV2RequestTtsType(str, Enum):
    ORPHEUS = "orpheus"
    PIPER = "piper"

    def __str__(self) -> str:
        return str(self.value)
