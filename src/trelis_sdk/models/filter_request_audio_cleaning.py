from enum import Enum


class FilterRequestAudioCleaning(str, Enum):
    BASIC = "basic"
    DENOISE = "denoise"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
