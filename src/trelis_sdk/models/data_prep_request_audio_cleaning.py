from enum import Enum


class DataPrepRequestAudioCleaning(str, Enum):
    AGGRESSIVE = "aggressive"
    BASIC = "basic"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
