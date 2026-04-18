from enum import Enum


class SpeakerSimilarityRequestMode(str, Enum):
    PAIRED = "paired"
    SINGLE_REF = "single_ref"

    def __str__(self) -> str:
        return str(self.value)
