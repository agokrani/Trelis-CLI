from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.training_request_lora_target import TrainingRequestLoraTarget
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
    from ..models.dataset_spec import DatasetSpec


T = TypeVar("T", bound="TrainingRequest")


@_attrs_define
class TrainingRequest:
    """Request to start a training job.

    Attributes:
        base_model (str): HuggingFace model ID for the base model to fine-tune. Supported model families: Whisper
            (openai/whisper-tiny, openai/whisper-base, openai/whisper-small, openai/whisper-medium, openai/whisper-
            large-v3-turbo, openai/whisper-large-v3), Moonshine (UsefulSensors/moonshine-tiny, UsefulSensors/moonshine-base,
            plus language-specific variants like moonshine-tiny-ar, moonshine-base-zh, etc.), Qwen ASR (Qwen/Qwen3-ASR-0.6B,
            Qwen/Qwen3-ASR-1.7B), Voxtral (mistralai/Voxtral-Mini-3B-2507), Parakeet (nvidia/parakeet-tdt-0.6b-v3). You can
            also pass a fine-tuned model ID from any of these families.
        base_model_file_store_id (None | str | Unset): FileStore UUID containing model weights (S3). Mutually exclusive
            with base_model as HF ID.
        train_datasets (list[DatasetSpec] | None | Unset): List of training datasets (recommended). Use this OR
            train_dataset, not both.
        train_dataset (None | str | Unset): Single training dataset ID (legacy). Prefer train_datasets for new
            integrations.
        train_split (str | Unset): Dataset split to use for training. Default: 'train'.
        train_dataset_config (None | str | Unset): Dataset config name, for datasets with multiple subsets (e.g. 'en_us'
            in google/fleurs).
        validation_dataset (None | str | Unset): Validation dataset ID. If omitted, a portion of the training data is
            used.
        validation_split (str | Unset): Dataset split to use for validation. Default: 'validation'.
        validation_dataset_config (None | str | Unset): Config name for the validation dataset, if it has multiple
            subsets.
        output_org (None | str | Unset): HuggingFace org/user to push the trained model to, e.g. 'my-org'. Required if
            push_to_hub is true.
        output_model_name (None | str | Unset): Name for the output model repo, e.g. 'whisper-large-v3-turbo-my-data'.
            Auto-generated if omitted.
        push_to_hub (bool | Unset): Push the trained model to HuggingFace Hub when training completes. Default: True.
        batch_size (int | None | Unset): Global batch size (total samples per optimizer step across all GPUs). Must be a
            power of 2. Leave blank to auto-recommend based on dataset size (recommended).
        gradient_accumulation_steps (int | None | Unset): Gradient accumulation steps. Auto-derived from global batch
            size and GPU count. Only provide to override.
        learning_rate (float | None | Unset): Learning rate. Leave blank to auto-recommend based on dataset size
            (recommended).
        lr_scheduler (str | Unset): Learning rate scheduler: 'constant_with_warmup' or 'cosine'. Default:
            'constant_with_warmup'.
        epochs (int | None | Unset): Number of training epochs. Leave blank to auto-recommend based on dataset size
            (recommended).
        lora_rank (int | Unset): LoRA rank. Higher values increase model capacity but use more memory. Default: 32.
        lora_alpha (int | Unset): LoRA alpha scaling factor. Default: 16.
        use_rslora (bool | Unset): Use Rank-Stabilized LoRA (RSLoRA) for more stable training. Default: True.
        lora_target (TrainingRequestLoraTarget | Unset): Which modules to apply LoRA to: 'both' (encoder + decoder) or
            'decoder_only'. Default: TrainingRequestLoraTarget.BOTH.
        train_embeddings (bool | Unset): Whether to train input/output embedding layers (increases memory usage).
            Default: False.
        private (bool | Unset): Deprecated — always True. Repos are always created as private. Default: True.
        enable_timestamps (bool | Unset): Enable timestamp token training. When enabled, 50% of training data uses
            timestamp tokens. Default: False.
        wandb_entity (None | str | Unset): W&B team name (not organization). Uses default team if omitted.
        wandb_project (None | str | Unset): W&B project name.
        wandb_run_name (None | str | Unset): W&B run name. Auto-generated if omitted.
        max_validation_rows (int | Unset): Max validation samples for evaluation during training (baseline, periodic,
            final) Default: 500.
        language (str | Unset): Full language name (e.g., 'english', 'greek'). Set to 'multilingual' to read per-sample
            language from the dataset's 'language' column (ISO 639-1 codes like 'en', 'el'). When 'multilingual' is set,
            samples without a language column are skipped. When set to a specific language (default), the dataset's language
            column is ignored. 'auto' is not supported for training. Default: 'english'.
        normalizer (str | Unset): Text normalizer for WER/CER computation during training evaluation. Options: 'auto'
            (select based on language — e.g., Greek normalizer for Greek), 'generic' (Unicode-aware: lowercase, strip
            punctuation, preserve all scripts), 'whisper-english' (aggressive English normalizer — numbers, contractions,
            fillers, British spelling), 'none' (no normalization — compare raw text), or a language name (e.g., 'greek').
            Default: 'auto'.
        max_train_samples (int | None | Unset): Limit training to a random subset of N samples. Useful for quick
            experimentation.
    """

    base_model: str
    base_model_file_store_id: None | str | Unset = UNSET
    train_datasets: list[DatasetSpec] | None | Unset = UNSET
    train_dataset: None | str | Unset = UNSET
    train_split: str | Unset = "train"
    train_dataset_config: None | str | Unset = UNSET
    validation_dataset: None | str | Unset = UNSET
    validation_split: str | Unset = "validation"
    validation_dataset_config: None | str | Unset = UNSET
    output_org: None | str | Unset = UNSET
    output_model_name: None | str | Unset = UNSET
    push_to_hub: bool | Unset = True
    batch_size: int | None | Unset = UNSET
    gradient_accumulation_steps: int | None | Unset = UNSET
    learning_rate: float | None | Unset = UNSET
    lr_scheduler: str | Unset = "constant_with_warmup"
    epochs: int | None | Unset = UNSET
    lora_rank: int | Unset = 32
    lora_alpha: int | Unset = 16
    use_rslora: bool | Unset = True
    lora_target: TrainingRequestLoraTarget | Unset = TrainingRequestLoraTarget.BOTH
    train_embeddings: bool | Unset = False
    private: bool | Unset = True
    enable_timestamps: bool | Unset = False
    wandb_entity: None | str | Unset = UNSET
    wandb_project: None | str | Unset = UNSET
    wandb_run_name: None | str | Unset = UNSET
    max_validation_rows: int | Unset = 500
    language: str | Unset = "english"
    normalizer: str | Unset = "auto"
    max_train_samples: int | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_spec import DatasetSpec

        base_model = self.base_model

        base_model_file_store_id: None | str | Unset
        if isinstance(self.base_model_file_store_id, Unset):
            base_model_file_store_id = UNSET
        else:
            base_model_file_store_id = self.base_model_file_store_id

        train_datasets: list[dict[str, Any]] | None | Unset
        if isinstance(self.train_datasets, Unset):
            train_datasets = UNSET
        elif isinstance(self.train_datasets, list):
            train_datasets = []
            for train_datasets_type_0_item_data in self.train_datasets:
                train_datasets_type_0_item = train_datasets_type_0_item_data.to_dict()
                train_datasets.append(train_datasets_type_0_item)

        else:
            train_datasets = self.train_datasets

        train_dataset: None | str | Unset
        if isinstance(self.train_dataset, Unset):
            train_dataset = UNSET
        else:
            train_dataset = self.train_dataset

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

        lora_rank = self.lora_rank

        lora_alpha = self.lora_alpha

        use_rslora = self.use_rslora

        lora_target: str | Unset = UNSET
        if not isinstance(self.lora_target, Unset):
            lora_target = self.lora_target.value

        train_embeddings = self.train_embeddings

        private = self.private

        enable_timestamps = self.enable_timestamps

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

        max_validation_rows = self.max_validation_rows

        language = self.language

        normalizer = self.normalizer

        max_train_samples: int | None | Unset
        if isinstance(self.max_train_samples, Unset):
            max_train_samples = UNSET
        else:
            max_train_samples = self.max_train_samples

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "base_model": base_model,
            }
        )
        if base_model_file_store_id is not UNSET:
            field_dict["base_model_file_store_id"] = base_model_file_store_id
        if train_datasets is not UNSET:
            field_dict["train_datasets"] = train_datasets
        if train_dataset is not UNSET:
            field_dict["train_dataset"] = train_dataset
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
        if lora_rank is not UNSET:
            field_dict["lora_rank"] = lora_rank
        if lora_alpha is not UNSET:
            field_dict["lora_alpha"] = lora_alpha
        if use_rslora is not UNSET:
            field_dict["use_rslora"] = use_rslora
        if lora_target is not UNSET:
            field_dict["lora_target"] = lora_target
        if train_embeddings is not UNSET:
            field_dict["train_embeddings"] = train_embeddings
        if private is not UNSET:
            field_dict["private"] = private
        if enable_timestamps is not UNSET:
            field_dict["enable_timestamps"] = enable_timestamps
        if wandb_entity is not UNSET:
            field_dict["wandb_entity"] = wandb_entity
        if wandb_project is not UNSET:
            field_dict["wandb_project"] = wandb_project
        if wandb_run_name is not UNSET:
            field_dict["wandb_run_name"] = wandb_run_name
        if max_validation_rows is not UNSET:
            field_dict["max_validation_rows"] = max_validation_rows
        if language is not UNSET:
            field_dict["language"] = language
        if normalizer is not UNSET:
            field_dict["normalizer"] = normalizer
        if max_train_samples is not UNSET:
            field_dict["max_train_samples"] = max_train_samples

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_spec import DatasetSpec

        d = dict(src_dict)
        base_model = d.pop("base_model")

        def _parse_base_model_file_store_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        base_model_file_store_id = _parse_base_model_file_store_id(
            d.pop("base_model_file_store_id", UNSET)
        )

        def _parse_train_datasets(data: object) -> list[DatasetSpec] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                train_datasets_type_0 = []
                _train_datasets_type_0 = data
                for train_datasets_type_0_item_data in _train_datasets_type_0:
                    train_datasets_type_0_item = DatasetSpec.from_dict(
                        train_datasets_type_0_item_data
                    )

                    train_datasets_type_0.append(train_datasets_type_0_item)

                return train_datasets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DatasetSpec] | None | Unset, data)

        train_datasets = _parse_train_datasets(d.pop("train_datasets", UNSET))

        def _parse_train_dataset(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        train_dataset = _parse_train_dataset(d.pop("train_dataset", UNSET))

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

        lora_rank = d.pop("lora_rank", UNSET)

        lora_alpha = d.pop("lora_alpha", UNSET)

        use_rslora = d.pop("use_rslora", UNSET)

        _lora_target = d.pop("lora_target", UNSET)
        lora_target: TrainingRequestLoraTarget | Unset
        if isinstance(_lora_target, Unset):
            lora_target = UNSET
        else:
            lora_target = TrainingRequestLoraTarget(_lora_target)

        train_embeddings = d.pop("train_embeddings", UNSET)

        private = d.pop("private", UNSET)

        enable_timestamps = d.pop("enable_timestamps", UNSET)

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

        max_validation_rows = d.pop("max_validation_rows", UNSET)

        language = d.pop("language", UNSET)

        normalizer = d.pop("normalizer", UNSET)

        def _parse_max_train_samples(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_train_samples = _parse_max_train_samples(d.pop("max_train_samples", UNSET))

        training_request = cls(
            base_model=base_model,
            base_model_file_store_id=base_model_file_store_id,
            train_datasets=train_datasets,
            train_dataset=train_dataset,
            train_split=train_split,
            train_dataset_config=train_dataset_config,
            validation_dataset=validation_dataset,
            validation_split=validation_split,
            validation_dataset_config=validation_dataset_config,
            output_org=output_org,
            output_model_name=output_model_name,
            push_to_hub=push_to_hub,
            batch_size=batch_size,
            gradient_accumulation_steps=gradient_accumulation_steps,
            learning_rate=learning_rate,
            lr_scheduler=lr_scheduler,
            epochs=epochs,
            lora_rank=lora_rank,
            lora_alpha=lora_alpha,
            use_rslora=use_rslora,
            lora_target=lora_target,
            train_embeddings=train_embeddings,
            private=private,
            enable_timestamps=enable_timestamps,
            wandb_entity=wandb_entity,
            wandb_project=wandb_project,
            wandb_run_name=wandb_run_name,
            max_validation_rows=max_validation_rows,
            language=language,
            normalizer=normalizer,
            max_train_samples=max_train_samples,
        )

        return training_request
