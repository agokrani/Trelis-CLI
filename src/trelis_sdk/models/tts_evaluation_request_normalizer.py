from enum import Enum


class TTSEvaluationRequestNormalizer(str, Enum):
    AUTO = "auto"
    GENERIC = "generic"
    GREEK = "greek"
    NONE = "none"
    WHISPER_ENGLISH = "whisper-english"

    def __str__(self) -> str:
        return str(self.value)
