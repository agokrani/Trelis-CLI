"""End-to-end CLI smoke tests against respx-mocked HTTP."""

from __future__ import annotations

import json
from pathlib import Path

import respx
from httpx import Response

from trelis_cli.__main__ import app


def test_version(runner) -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip()


def test_whoami_json(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/me/").mock(
        return_value=Response(200, json={"email": "a@b.com", "credits": 42})
    )
    result = runner.invoke(app, ["--json", "auth", "whoami"])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload == {"email": "a@b.com", "credits": 42}


def test_whoami_unauthorized(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/me/").mock(
        return_value=Response(401, json={"detail": "Invalid API key"})
    )
    result = runner.invoke(app, ["--json", "auth", "whoami"])
    assert result.exit_code == 3
    err = json.loads(result.stderr)
    assert err["error"] == "Invalid API key"
    assert err["exit_code"] == 3


def test_models_list_json(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/models").mock(
        return_value=Response(
            200,
            json=[
                {"id": "whisper-large-v3", "modality": "asr"},
                {"id": "xtts-v2", "modality": "tts"},
            ],
        )
    )
    result = runner.invoke(app, ["--json", "models", "list"])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert len(payload) == 2
    assert payload[0]["id"] == "whisper-large-v3"


def test_upload_parquet_no_wait(runner, mock_api: respx.Router, tmp_path: Path) -> None:
    parquet = tmp_path / "train.parquet"
    parquet.write_bytes(b"PAR1\x00fake-parquet-content\x00PAR1")
    mock_api.post("/api/v1/file-stores/upload-parquet").mock(
        return_value=Response(
            200,
            json={
                "file_store_id": "fs_123",
                "name": "train",
                "columns": ["audio", "text"],
                "num_rows": 100,
                "size_bytes": 4096,
            },
        )
    )
    result = runner.invoke(app, ["--json", "file-stores", "upload-parquet", str(parquet)])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["file_store_id"] == "fs_123"
    assert payload["num_rows"] == 100


def test_upload_parquet_rejects_non_parquet(runner, mock_api: respx.Router, tmp_path: Path) -> None:
    bad = tmp_path / "not-parquet.txt"
    bad.write_text("hello")
    result = runner.invoke(app, ["--json", "file-stores", "upload-parquet", str(bad)])
    assert result.exit_code == 1
    err = json.loads(result.stderr)
    assert ".parquet" in err["error"]


def test_warns_on_non_tsk_prefix(runner, mock_api: respx.Router, monkeypatch) -> None:
    """Token without tsk_ prefix should warn on stderr in human mode."""
    monkeypatch.setenv("TRELIS_API_KEY", "hf_wrong_token_kind")
    mock_api.get("/api/v1/me/").mock(return_value=Response(200, json={"email": "a@b.com"}))
    result = runner.invoke(app, ["auth", "whoami"])  # no --json
    assert result.exit_code == 0, result.stderr
    assert "does not start with 'tsk_'" in result.stderr


def test_no_prefix_warning_in_json_mode(runner, mock_api: respx.Router, monkeypatch) -> None:
    """JSON mode keeps stderr clean for agents."""
    monkeypatch.setenv("TRELIS_API_KEY", "hf_wrong_token_kind")
    mock_api.get("/api/v1/me/").mock(return_value=Response(200, json={"email": "a@b.com"}))
    result = runner.invoke(app, ["--json", "auth", "whoami"])
    assert result.exit_code == 0, result.stderr
    assert result.stderr == ""
