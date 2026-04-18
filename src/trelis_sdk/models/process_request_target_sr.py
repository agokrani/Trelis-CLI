from enum import IntEnum


class ProcessRequestTargetSr(IntEnum):
    VALUE_16000 = 16000
    VALUE_22050 = 22050
    VALUE_24000 = 24000

    def __str__(self) -> str:
        return str(self.value)
