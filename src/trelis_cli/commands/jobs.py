"""Job resource registry: 10 resources through the shared factory.

Skipped: old `/mos-evaluation` and `/speaker-similarity` — superseded
by v2 under `/analysis/*`, still reachable via the SDK if needed.
`tts-evaluation.submit` is absent upstream (`start_tts_evaluation_gone`).
"""

from __future__ import annotations

import typer

from trelis_sdk.api.api_v1 import (
    # data-prep
    list_data_prep_jobs_api_v1_data_prep_jobs_get as _list_data_prep,
    get_data_prep_job_api_v1_data_prep_jobs_job_id_get as _get_data_prep,
    stop_data_prep_job_api_v1_data_prep_jobs_job_id_cancel_post as _cancel_data_prep,
    delete_data_prep_job_not_supported_api_v1_data_prep_jobs_job_id_delete as _delete_data_prep,
    # evaluation
    list_evaluation_jobs_api_v1_evaluation_jobs_get as _list_evaluation,
    get_evaluation_job_api_v1_evaluation_jobs_job_id_get as _get_evaluation,
    stop_evaluation_job_api_v1_evaluation_jobs_job_id_cancel_post as _cancel_evaluation,
    delete_evaluation_job_not_supported_api_v1_evaluation_jobs_job_id_delete as _delete_evaluation,
    # training (submit via v2 unified endpoint; list/get/cancel/delete still on /training/jobs/*)
    list_training_jobs_api_v1_training_jobs_get as _list_training,
    get_training_job_api_v1_training_jobs_job_id_get as _get_training,
    stop_training_job_api_v1_training_jobs_job_id_cancel_post as _cancel_training,
    delete_training_job_not_supported_api_v1_training_jobs_job_id_delete as _delete_training,
    # synthesis
    list_synthesis_jobs_api_v1_synthesis_jobs_get as _list_synthesis,
    get_synthesis_job_api_v1_synthesis_jobs_job_id_get as _get_synthesis,
    stop_synthesis_job_api_v1_synthesis_jobs_job_id_cancel_post as _cancel_synthesis,
    delete_synthesis_job_not_supported_api_v1_synthesis_jobs_job_id_delete as _delete_synthesis,
    # transcription (cancel-only, no stop endpoint)
    list_transcription_jobs_api_v1_transcription_jobs_get as _list_transcription,
    get_transcription_job_api_v1_transcription_jobs_job_id_get as _get_transcription,
    cancel_transcription_job_api_v1_transcription_jobs_job_id_cancel_post as _cancel_transcription,
    delete_transcription_job_not_supported_api_v1_transcription_jobs_job_id_delete as _delete_transcription,
    # tts-training
    list_tts_training_jobs_api_v1_tts_training_jobs_get as _list_tts_training,
    get_tts_training_job_api_v1_tts_training_jobs_job_id_get as _get_tts_training,
    stop_tts_training_job_api_v1_tts_training_jobs_job_id_cancel_post as _cancel_tts_training,
    delete_tts_training_job_not_supported_api_v1_tts_training_jobs_job_id_delete as _delete_tts_training,
    # tts-training-ddp
    list_tts_training_ddp_jobs_api_v1_tts_training_ddp_jobs_get as _list_tts_training_ddp,
    get_tts_training_ddp_job_api_v1_tts_training_ddp_jobs_job_id_get as _get_tts_training_ddp,
    stop_tts_training_ddp_job_api_v1_tts_training_ddp_jobs_job_id_cancel_post as _cancel_tts_training_ddp,
    delete_tts_training_ddp_job_not_supported_api_v1_tts_training_ddp_jobs_job_id_delete as _delete_tts_training_ddp,
    # tts-evaluation (submit disabled upstream — start_tts_evaluation_gone)
    list_tts_evaluation_jobs_api_v1_tts_evaluation_jobs_get as _list_tts_evaluation,
    get_tts_evaluation_job_api_v1_tts_evaluation_jobs_job_id_get as _get_tts_evaluation,
    stop_tts_evaluation_job_api_v1_tts_evaluation_jobs_job_id_stop_post as _cancel_tts_evaluation,
    # mos (v2 via /analysis/mos)
    list_v2_mos_jobs_api_v1_analysis_mos_jobs_get as _list_mos,
    get_v2_mos_job_api_v1_analysis_mos_jobs_job_id_get as _get_mos,
    cancel_v2_mos_job_api_v1_analysis_mos_jobs_job_id_cancel_post as _cancel_mos,
    # speaker-similarity (v2 via /analysis/speaker-similarity)
    list_v2_speaker_similarity_jobs_api_v1_analysis_speaker_similarity_jobs_get as _list_speaker_similarity,
    get_v2_speaker_similarity_job_api_v1_analysis_speaker_similarity_jobs_job_id_get as _get_speaker_similarity,
    cancel_v2_speaker_similarity_job_api_v1_analysis_speaker_similarity_jobs_job_id_cancel_post as _cancel_speaker_similarity,
)

from ._job_factory import JobResource, build_resource_app


RESOURCES: list[JobResource] = [
    JobResource(
        name="data-prep",
        help="Data preparation jobs (format conversion, splits).",
        submit_path="/api/v1/data-prep",
        list_mod=_list_data_prep,
        get_mod=_get_data_prep,
        cancel_mod=_cancel_data_prep,
        delete_mod=_delete_data_prep,
    ),
    JobResource(
        name="evaluation",
        help="ASR/model evaluation jobs.",
        submit_path="/api/v1/evaluation/jobs",
        list_mod=_list_evaluation,
        get_mod=_get_evaluation,
        cancel_mod=_cancel_evaluation,
        delete_mod=_delete_evaluation,
    ),
    JobResource(
        name="training",
        help="Training jobs (ASR/TTS unified v2 submit).",
        submit_path="/api/v1/training",  # v2 unified endpoint
        list_mod=_list_training,
        get_mod=_get_training,
        cancel_mod=_cancel_training,
        delete_mod=_delete_training,
    ),
    JobResource(
        name="synthesis",
        help="Speech synthesis jobs.",
        submit_path="/api/v1/synthesis",
        list_mod=_list_synthesis,
        get_mod=_get_synthesis,
        cancel_mod=_cancel_synthesis,
        delete_mod=_delete_synthesis,
    ),
    JobResource(
        name="transcription",
        help="Transcription jobs.",
        submit_path="/api/v1/transcription",
        list_mod=_list_transcription,
        get_mod=_get_transcription,
        cancel_mod=_cancel_transcription,
        delete_mod=_delete_transcription,
    ),
    JobResource(
        name="tts-training",
        help="TTS training jobs (single-GPU).",
        submit_path="/api/v1/tts-training/jobs",
        list_mod=_list_tts_training,
        get_mod=_get_tts_training,
        cancel_mod=_cancel_tts_training,
        delete_mod=_delete_tts_training,
    ),
    JobResource(
        name="tts-training-ddp",
        help="TTS training jobs (multi-GPU distributed).",
        submit_path="/api/v1/tts-training-ddp/jobs",
        list_mod=_list_tts_training_ddp,
        get_mod=_get_tts_training_ddp,
        cancel_mod=_cancel_tts_training_ddp,
        delete_mod=_delete_tts_training_ddp,
    ),
    JobResource(
        name="tts-evaluation",
        help="TTS evaluation jobs (submit disabled upstream; list/get/cancel only).",
        submit_path=None,  # upstream removed submit: start_tts_evaluation_gone
        list_mod=_list_tts_evaluation,
        get_mod=_get_tts_evaluation,
        cancel_mod=_cancel_tts_evaluation,
    ),
    JobResource(
        name="mos",
        help="MOS analysis jobs (v2, /analysis/mos).",
        submit_path="/api/v1/analysis/mos",
        list_mod=_list_mos,
        get_mod=_get_mos,
        cancel_mod=_cancel_mos,
    ),
    JobResource(
        name="speaker-similarity",
        help="Speaker-similarity analysis jobs (v2, /analysis/speaker-similarity).",
        submit_path="/api/v1/analysis/speaker-similarity",
        list_mod=_list_speaker_similarity,
        get_mod=_get_speaker_similarity,
        cancel_mod=_cancel_speaker_similarity,
    ),
]


def register_all(parent: typer.Typer) -> None:
    """Mount every job resource sub-app onto the given parent Typer app."""
    for resource in RESOURCES:
        parent.add_typer(build_resource_app(resource))
