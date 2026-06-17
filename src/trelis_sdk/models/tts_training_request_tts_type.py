from enum import Enum


class TTSTrainingRequestTtsType(str, Enum):
    ORPHEUS = "orpheus"
    PIPER = "piper"

    def __str__(self) -> str:
        return str(self.value)
