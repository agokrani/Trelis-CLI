from enum import Enum


class DataPrepRequestSplitOption(str, Enum):
    CREATE_VALIDATION = "create_validation"
    PRESERVE = "preserve"
    SINGLE = "single"

    def __str__(self) -> str:
        return str(self.value)
