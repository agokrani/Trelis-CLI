from enum import Enum


class TTSEvaluationRequestApplyTextNormalizationType0(str, Enum):
    AUTO = "auto"
    OFF = "off"
    ON = "on"

    def __str__(self) -> str:
        return str(self.value)
