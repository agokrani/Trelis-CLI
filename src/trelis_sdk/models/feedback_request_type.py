from enum import Enum


class FeedbackRequestType(str, Enum):
    BUG = "bug"
    SUGGESTION = "suggestion"

    def __str__(self) -> str:
        return str(self.value)
