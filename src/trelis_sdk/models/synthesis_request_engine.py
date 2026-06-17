from enum import Enum


class SynthesisRequestEngine(str, Enum):
    AUTO = "auto"
    CHATTERBOX = "chatterbox"
    ORPHEUS = "orpheus"
    PIPER = "piper"
    ROUTER = "router"

    def __str__(self) -> str:
        return str(self.value)
