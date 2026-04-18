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

The upstream OpenAPI spec omits `securitySchemes` even though the API
enforces `Authorization: Bearer ...`. We patch it in via `overlay.yaml`
before codegen, and inject the bearer token in
`AuthenticatedClient` at runtime.

## Quick start

```bash
uv sync --extra dev
uv pip install -e .
make regen           # apply overlay + regenerate src/trelis_sdk
uv run pytest        # 6 tests, all mocked
uv run trelis --help
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
