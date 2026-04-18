from enum import Enum


class FileStoreTTSRequestEngineType0(str, Enum):
    KOKORO = "kokoro"
    ORPHEUS = "orpheus"
    PIPER = "piper"

    def __str__(self) -> str:
        return str(self.value)
