from enum import Enum


class FileStoreTranscriptUpdateRequestTranscriptType(str, Enum):
    SRT = "srt"
    TXT = "txt"
    VTT = "vtt"

    def __str__(self) -> str:
        return str(self.value)
