from enum import Enum


class ProcessRequestSplitOption(str, Enum):
    CREATE_VALIDATION = "create_validation"
    TEST_ONLY = "test_only"
    TRAIN_ONLY = "train_only"
    VALIDATION_ONLY = "validation_only"

    def __str__(self) -> str:
        return str(self.value)
