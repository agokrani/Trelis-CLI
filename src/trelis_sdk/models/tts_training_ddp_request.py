from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast


T = TypeVar("T", bound="TTSTrainingDDPRequest")


@_attrs_define
class TTSTrainingDDPRequest:
    """Request to start a TTS DDP training job.

    Attributes:
        tts_type (str | Unset):  Default: 'orpheus'.
        base_model (None | str | Unset):  Default: ''.
        train_dataset (None | str | Unset):
        file_store_id (None | str | Unset): FileStore UUID to use as training dataset (must contain parquet files).
            Mutually exclusive with train_dataset.
        train_split (str | Unset):  Default: 'train'.
        train_dataset_config (None | str | Unset):
        validation_dataset (None | str | Unset):
        validation_split (str | Unset):  Default: 'validation'.
        validation_dataset_config (None | str | Unset):
        output_org (None | str | Unset):
        output_model_name (None | str | Unset):
        push_to_hub (bool | Unset):  Default: True.
        private (bool | Unset):  Default: True.
        lora_rank (int | Unset):  Default: 64.
        lora_alpha (int | Unset):  Default: 64.
        train_embeddings (bool | Unset):  Default: False.
        batch_size (int | None | Unset):
        gradient_accumulation_steps (int | None | Unset):
        learning_rate (float | None | Unset):
        lr_scheduler (str | Unset):  Default: 'linear'.
        epochs (int | None | Unset):
        max_seq_length (int | Unset):  Default: 4096.
        warmup_steps (int | Unset):  Default: 5.
        num_gpus (int | Unset):  Default: 4.
        use_unsloth (bool | Unset):  Default: True.
        speaker_name (str | Unset):  Default: 'speaker'.
        quality (None | str | Unset):
        language (None | str | Unset):
        validation_pct (float | None | Unset):
        preprocessed_dataset (None | str | Unset):
        push_preprocessed (bool | Unset):  Default: False.
        max_train_samples (int | None | Unset): Limit training to a random subset of N samples. Useful for quick smoke
            tests.
        max_validation_rows (int | Unset): Max validation samples evaluated during training (baseline, periodic, final).
            Default: 500.
        wandb_entity (None | str | Unset): W&B team name (not organization).
        wandb_project (None | str | Unset):
        wandb_run_name (None | str | Unset):
    """

    tts_type: str | Unset = "orpheus"
    base_model: None | str | Unset = ""
    train_dataset: None | str | Unset = UNSET
    file_store_id: None | str | Unset = UNSET
    train_split: str | Unset = "train"
    train_dataset_config: None | str | Unset = UNSET
    validation_dataset: None | str | Unset = UNSET
    validation_split: str | Unset = "validation"
    validation_dataset_config: None | str | Unset = UNSET
    output_org: None | str | Unset = UNSET
    output_model_name: None | str | Unset = UNSET
    push_to_hub: bool | Unset = True
    private: bool | Unset = True
    lora_rank: int | Unset = 64
    lora_alpha: int | Unset = 64
    train_embeddings: bool | Unset = False
    batch_size: int | None | Unset = UNSET
    gradient_accumulation_steps: int | None | Unset = UNSET
    learning_rate: float | None | Unset = UNSET
    lr_scheduler: str | Unset = "linear"
    epochs: int | None | Unset = UNSET
    max_seq_length: int | Unset = 4096
    warmup_steps: int | Unset = 5
    num_gpus: int | Unset = 4
    use_unsloth: bool | Unset = True
    speaker_name: str | Unset = "speaker"
    quality: None | str | Unset = UNSET
    language: None | str | Unset = UNSET
    validation_pct: float | None | Unset = UNSET
    preprocessed_dataset: None | str | Unset = UNSET
    push_preprocessed: bool | Unset = False
    max_train_samples: int | None | Unset = UNSET
    max_validation_rows: int | Unset = 500
    wandb_entity: None | str | Unset = UNSET
    wandb_project: None | str | Unset = UNSET
    wandb_run_name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        tts_type = self.tts_type

        base_model: None | str | Unset
        if isinstance(self.base_model, Unset):
            base_model = UNSET
        else:
            base_model = self.base_model

        train_dataset: None | str | Unset
        if isinstance(self.train_dataset, Unset):
            train_dataset = UNSET
        else:
            train_dataset = self.train_dataset

        file_store_id: None | str | Unset
        if isinstance(self.file_store_id, Unset):
            file_store_id = UNSET
        else:
            file_store_id = self.file_store_id

        train_split = self.train_split

        train_dataset_config: None | str | Unset
        if isinstance(self.train_dataset_config, Unset):
            train_dataset_config = UNSET
        else:
            train_dataset_config = self.train_dataset_config

        validation_dataset: None | str | Unset
        if isinstance(self.validation_dataset, Unset):
            validation_dataset = UNSET
        else:
            validation_dataset = self.validation_dataset

        validation_split = self.validation_split

        validation_dataset_config: None | str | Unset
        if isinstance(self.validation_dataset_config, Unset):
            validation_dataset_config = UNSET
        else:
            validation_dataset_config = self.validation_dataset_config

        output_org: None | str | Unset
        if isinstance(self.output_org, Unset):
            output_org = UNSET
        else:
            output_org = self.output_org

        output_model_name: None | str | Unset
        if isinstance(self.output_model_name, Unset):
            output_model_name = UNSET
        else:
            output_model_name = self.output_model_name

        push_to_hub = self.push_to_hub

        private = self.private

        lora_rank = self.lora_rank

        lora_alpha = self.lora_alpha

        train_embeddings = self.train_embeddings

        batch_size: int | None | Unset
        if isinstance(self.batch_size, Unset):
            batch_size = UNSET
        else:
            batch_size = self.batch_size

        gradient_accumulation_steps: int | None | Unset
        if isinstance(self.gradient_accumulation_steps, Unset):
            gradient_accumulation_steps = UNSET
        else:
            gradient_accumulation_steps = self.gradient_accumulation_steps

        learning_rate: float | None | Unset
        if isinstance(self.learning_rate, Unset):
            learning_rate = UNSET
        else:
            learning_rate = self.learning_rate

        lr_scheduler = self.lr_scheduler

        epochs: int | None | Unset
        if isinstance(self.epochs, Unset):
            epochs = UNSET
        else:
            epochs = self.epochs

        max_seq_length = self.max_seq_length

        warmup_steps = self.warmup_steps

        num_gpus = self.num_gpus

        use_unsloth = self.use_unsloth

        speaker_name = self.speaker_name

        quality: None | str | Unset
        if isinstance(self.quality, Unset):
            quality = UNSET
        else:
            quality = self.quality

        language: None | str | Unset
        if isinstance(self.language, Unset):
            language = UNSET
        else:
            language = self.language

        validation_pct: float | None | Unset
        if isinstance(self.validation_pct, Unset):
            validation_pct = UNSET
        else:
            validation_pct = self.validation_pct

        preprocessed_dataset: None | str | Unset
        if isinstance(self.preprocessed_dataset, Unset):
            preprocessed_dataset = UNSET
        else:
            preprocessed_dataset = self.preprocessed_dataset

        push_preprocessed = self.push_preprocessed

        max_train_samples: int | None | Unset
        if isinstance(self.max_train_samples, Unset):
            max_train_samples = UNSET
        else:
            max_train_samples = self.max_train_samples

        max_validation_rows = self.max_validation_rows

        wandb_entity: None | str | Unset
        if isinstance(self.wandb_entity, Unset):
            wandb_entity = UNSET
        else:
            wandb_entity = self.wandb_entity

        wandb_project: None | str | Unset
        if isinstance(self.wandb_project, Unset):
            wandb_project = UNSET
        else:
            wandb_project = self.wandb_project

        wandb_run_name: None | str | Unset
        if isinstance(self.wandb_run_name, Unset):
            wandb_run_name = UNSET
        else:
            wandb_run_name = self.wandb_run_name

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if tts_type is not UNSET:
            field_dict["tts_type"] = tts_type
        if base_model is not UNSET:
            field_dict["base_model"] = base_model
        if train_dataset is not UNSET:
            field_dict["train_dataset"] = train_dataset
        if file_store_id is not UNSET:
            field_dict["file_store_id"] = file_store_id
        if train_split is not UNSET:
            field_dict["train_split"] = train_split
        if train_dataset_config is not UNSET:
            field_dict["train_dataset_config"] = train_dataset_config
        if validation_dataset is not UNSET:
            field_dict["validation_dataset"] = validation_dataset
        if validation_split is not UNSET:
            field_dict["validation_split"] = validation_split
        if validation_dataset_config is not UNSET:
            field_dict["validation_dataset_config"] = validation_dataset_config
        if output_org is not UNSET:
            field_dict["output_org"] = output_org
        if output_model_name is not UNSET:
            field_dict["output_model_name"] = output_model_name
        if push_to_hub is not UNSET:
            field_dict["push_to_hub"] = push_to_hub
        if private is not UNSET:
            field_dict["private"] = private
        if lora_rank is not UNSET:
            field_dict["lora_rank"] = lora_rank
        if lora_alpha is not UNSET:
            field_dict["lora_alpha"] = lora_alpha
        if train_embeddings is not UNSET:
            field_dict["train_embeddings"] = train_embeddings
        if batch_size is not UNSET:
            field_dict["batch_size"] = batch_size
        if gradient_accumulation_steps is not UNSET:
            field_dict["gradient_accumulation_steps"] = gradient_accumulation_steps
        if learning_rate is not UNSET:
            field_dict["learning_rate"] = learning_rate
        if lr_scheduler is not UNSET:
            field_dict["lr_scheduler"] = lr_scheduler
        if epochs is not UNSET:
            field_dict["epochs"] = epochs
        if max_seq_length is not UNSET:
            field_dict["max_seq_length"] = max_seq_length
        if warmup_steps is not UNSET:
            field_dict["warmup_steps"] = warmup_steps
        if num_gpus is not UNSET:
            field_dict["num_gpus"] = num_gpus
        if use_unsloth is not UNSET:
            field_dict["use_unsloth"] = use_unsloth
        if speaker_name is not UNSET:
            field_dict["speaker_name"] = speaker_name
        if quality is not UNSET:
            field_dict["quality"] = quality
        if language is not UNSET:
            field_dict["language"] = language
        if validation_pct is not UNSET:
            field_dict["validation_pct"] = validation_pct
        if preprocessed_dataset is not UNSET:
            field_dict["preprocessed_dataset"] = preprocessed_dataset
        if push_preprocessed is not UNSET:
            field_dict["push_preprocessed"] = push_preprocessed
        if max_train_samples is not UNSET:
            field_dict["max_train_samples"] = max_train_samples
        if max_validation_rows is not UNSET:
            field_dict["max_validation_rows"] = max_validation_rows
        if wandb_entity is not UNSET:
            field_dict["wandb_entity"] = wandb_entity
        if wandb_project is not UNSET:
            field_dict["wandb_project"] = wandb_project
        if wandb_run_name is not UNSET:
            field_dict["wandb_run_name"] = wandb_run_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tts_type = d.pop("tts_type", UNSET)

        def _parse_base_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        base_model = _parse_base_model(d.pop("base_model", UNSET))

        def _parse_train_dataset(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        train_dataset = _parse_train_dataset(d.pop("train_dataset", UNSET))

        def _parse_file_store_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        file_store_id = _parse_file_store_id(d.pop("file_store_id", UNSET))

        train_split = d.pop("train_split", UNSET)

        def _parse_train_dataset_config(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        train_dataset_config = _parse_train_dataset_config(d.pop("train_dataset_config", UNSET))

        def _parse_validation_dataset(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        validation_dataset = _parse_validation_dataset(d.pop("validation_dataset", UNSET))

        validation_split = d.pop("validation_split", UNSET)

        def _parse_validation_dataset_config(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        validation_dataset_config = _parse_validation_dataset_config(
            d.pop("validation_dataset_config", UNSET)
        )

        def _parse_output_org(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_org = _parse_output_org(d.pop("output_org", UNSET))

        def _parse_output_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        output_model_name = _parse_output_model_name(d.pop("output_model_name", UNSET))

        push_to_hub = d.pop("push_to_hub", UNSET)

        private = d.pop("private", UNSET)

        lora_rank = d.pop("lora_rank", UNSET)

        lora_alpha = d.pop("lora_alpha", UNSET)

        train_embeddings = d.pop("train_embeddings", UNSET)

        def _parse_batch_size(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        batch_size = _parse_batch_size(d.pop("batch_size", UNSET))

        def _parse_gradient_accumulation_steps(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        gradient_accumulation_steps = _parse_gradient_accumulation_steps(
            d.pop("gradient_accumulation_steps", UNSET)
        )

        def _parse_learning_rate(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        learning_rate = _parse_learning_rate(d.pop("learning_rate", UNSET))

        lr_scheduler = d.pop("lr_scheduler", UNSET)

        def _parse_epochs(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        epochs = _parse_epochs(d.pop("epochs", UNSET))

        max_seq_length = d.pop("max_seq_length", UNSET)

        warmup_steps = d.pop("warmup_steps", UNSET)

        num_gpus = d.pop("num_gpus", UNSET)

        use_unsloth = d.pop("use_unsloth", UNSET)

        speaker_name = d.pop("speaker_name", UNSET)

        def _parse_quality(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        quality = _parse_quality(d.pop("quality", UNSET))

        def _parse_language(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        language = _parse_language(d.pop("language", UNSET))

        def _parse_validation_pct(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        validation_pct = _parse_validation_pct(d.pop("validation_pct", UNSET))

        def _parse_preprocessed_dataset(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        preprocessed_dataset = _parse_preprocessed_dataset(d.pop("preprocessed_dataset", UNSET))

        push_preprocessed = d.pop("push_preprocessed", UNSET)

        def _parse_max_train_samples(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_train_samples = _parse_max_train_samples(d.pop("max_train_samples", UNSET))

        max_validation_rows = d.pop("max_validation_rows", UNSET)

        def _parse_wandb_entity(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        wandb_entity = _parse_wandb_entity(d.pop("wandb_entity", UNSET))

        def _parse_wandb_project(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        wandb_project = _parse_wandb_project(d.pop("wandb_project", UNSET))

        def _parse_wandb_run_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        wandb_run_name = _parse_wandb_run_name(d.pop("wandb_run_name", UNSET))

        tts_training_ddp_request = cls(
            tts_type=tts_type,
            base_model=base_model,
            train_dataset=train_dataset,
            file_store_id=file_store_id,
            train_split=train_split,
            train_dataset_config=train_dataset_config,
            validation_dataset=validation_dataset,
            validation_split=validation_split,
            validation_dataset_config=validation_dataset_config,
            output_org=output_org,
            output_model_name=output_model_name,
            push_to_hub=push_to_hub,
            private=private,
            lora_rank=lora_rank,
            lora_alpha=lora_alpha,
            train_embeddings=train_embeddings,
            batch_size=batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            lr_scheduler=lr_scheduler,
            epochs=epochs,
            max_seq_length=max_seq_length,
            warmup_steps=warmup_steps,
            num_gpus=num_gpus,
            use_unsloth=use_unsloth,
            speaker_name=speaker_name,
            quality=quality,
            language=language,
            validation_pct=validation_pct,
            preprocessed_dataset=preprocessed_dataset,
            push_preprocessed=push_preprocessed,
            max_train_samples=max_train_samples,
            max_validation_rows=max_validation_rows,
            wandb_entity=wandb_entity,
            wandb_project=wandb_project,
            wandb_run_name=wandb_run_name,
        )

        return tts_training_ddp_request
