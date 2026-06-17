from enum import Enum


class SpeakerSimilarityV2RequestSvModel(str, Enum):
    ECAPA = "ecapa"
    WAVLM_LARGE_SV = "wavlm_large_sv"

    def __str__(self) -> str:
        return str(self.value)
