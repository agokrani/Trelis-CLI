# Trelis CLI

Command-line interface for [Trelis Studio](https://studio.trelis.com) —
ASR/TTS training, evaluation, and data prep.

Designed for both humans (rich tables, prompts) and agents (`--json`
contract on every command, documented exit codes).

## Status: Phase A scaffolding

This repository implements **Phase A** from the project plan: SDK
generation, auth wrapper, command-map skeleton, hand-written
`file-stores upload-parquet`, and an end-to-end test scaffold mocked
with `respx`. Phase B (live response capture, snapshot lock,
`/stop` vs `/cancel` probe, smoke test) is gated on a real API key.

## Architecture

```
openapi.json + overlay.yaml  →  scripts/apply_overlay.py
                              →  build/openapi.merged.json
                              →  openapi-python-client (codegen)
                              →  src/trelis_sdk/   (generated, not hand-edited)

src/trelis_cli/                  hand-written CLI (Typer)
  ├─ __main__.py                 Typer root + JSON-mode flag
  ├─ auth.py / config.py         credential resolution, base URL
  ├─ output.py / errors.py       --json contract, exit codes, decorator
  ├─ jobs.py                     shared --wait/--watch/--poll helper
  ├─ api_helpers.py              call_json() bridge (handles 92% empty schemas)
  └─ commands/                   resource sub-apps grouped by path prefix
```

## Quick start

```bash
uv sync --extra dev
uv pip install -e .
make regen           # apply overlay + regenerate src/trelis_sdk
uv run pytest        # mocked CLI tests
uv run trelis --help
```

Example uploads:

```bash
uv run trelis file-stores upload-parquet ./dataset.parquet
uv run trelis file-stores upload-folder ./my-audio-folder
```

## ASR workflows

The workflow-oriented ASR surface sits on top of the low-level
`file-stores`, `data-prep`, and `transcription` commands:

```bash
# Discover ASR models and whether they route through Trelis Router
uv run trelis asr models list
uv run trelis asr models list --engine router
uv run trelis asr models show fireworks/whisper-v3

# Upload raw audio/text pairs
uv run trelis asr upload folder ./my-audio-folder --name my-raw-store

# Prepare a raw file store into a dataset-shaped store
uv run trelis asr prepare file-store <raw_store_id> --wait

# Submit an ASR job directly (HF dataset / FileStore / parquet URLs)
uv run trelis asr transcribe submit \
  --model openai/whisper-small \
  --language en \
  --dataset-id Trelis/my-dataset \
  --split train \
  --wait

# Inspect output and optionally push it to HF
uv run trelis asr output show <job_id>
uv run trelis asr output push-hf --job-id <job_id> --repo-id Trelis/my-output --wait
```

## Auth

Resolution order: `--api-key` flag → `TRELIS_API_KEY` env → keyring.

```bash
trelis auth login              # prompt + store in keyring
trelis auth whoami             # check
trelis auth logout
```

## Agent contract

Every command supports `--json`. JSON payloads on stdout; errors as
JSON on stderr. Exit codes:

| Code | Meaning            |
|------|--------------------|
| 0    | Success            |
| 1    | Usage error        |
| 2    | API error          |
| 3    | Auth error         |
| 4    | Timeout / poll exceeded |

## Development

```bash
make regen     # rebuild src/trelis_sdk/ from spec + overlay
make test      # pytest
make lint      # ruff check + format
make build     # wheel + sdist
```

## Implementation notes

### Why `overlay.yaml` exists

The upstream OpenAPI spec at `https://studio.trelis.com/openapi.json`
does not declare how the API is authenticated — it has no
`components.securitySchemes` block and no top-level `security:`
block — even though the live server requires
`Authorization: Bearer tsk_...` on every call.

If you point `openapi-python-client` at the raw spec, the generated
SDK has no concept of auth: no `token=` parameter, no
`AuthenticatedClient` class.

`overlay.yaml` patches the missing `BearerAuth` scheme into the
spec before codegen. `scripts/apply_overlay.py` applies the overlay
and writes `build/openapi.merged.json`, which is the input to the
generator. Result: the generated SDK produces
`AuthenticatedClient(token=...)` and injects the bearer header
automatically.

If Trelis ever fixes the spec upstream, the overlay can be deleted
and the generator re-run; nothing else in the CLI layer depends on
its existence.
