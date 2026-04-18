from enum import Enum


class SpeakerSimilarityV2RequestOutputTarget(str, Enum):
    HF = "hf"
    S3 = "s3"
    S3HF = "s3+hf"

    def __str__(self) -> str:
        return str(self.value)
