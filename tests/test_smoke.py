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
    mock_api.get("/api/v1/file-stores/fs_123/files").mock(
        return_value=Response(
            200,
            json={
                "file_store_id": "fs_123",
                "files": [
                    {"filename": "dataset_info.json", "size_bytes": 12},
                ],
            },
        )
    )
    result = runner.invoke(app, ["--json", "file-stores", "upload-parquet", str(parquet)])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["file_store_id"] == "fs_123"
    assert payload["num_rows"] == 100
    assert payload["dataset_info_status"] == "present"


def test_upload_parquet_uploads_missing_dataset_info(runner, mock_api: respx.Router, tmp_path: Path) -> None:
    parquet = tmp_path / "train.parquet"
    parquet.write_bytes(b"PAR1\x00fake-parquet-content\x00PAR1")

    mock_api.post("/api/v1/file-stores/upload-parquet").mock(
        return_value=Response(
            200,
            json={
                "file_store_id": "fs_missing_info",
                "name": "train",
                "columns": ["audio", "text"],
                "num_rows": 100,
                "size_bytes": 4096,
            },
        )
    )
    mock_api.get("/api/v1/file-stores/fs_missing_info/files").mock(
        return_value=Response(
            200,
            json={
                "file_store_id": "fs_missing_info",
                "files": [
                    {"filename": "data/train-00000-of-00001.parquet", "size_bytes": 4096},
                ],
            },
        )
    )
    mock_api.post("/api/v1/file-stores/upload-urls").mock(
        return_value=Response(
            200,
            json={
                "file_store_id": "fs_missing_info",
                "files": [
                    {
                        "filename": "dataset_info.json",
                        "upload_url": "https://studio.trelis.com/presigned/dataset_info.json",
                        "content_type": "application/json",
                        "expires_in": 7200,
                    }
                ],
            },
        )
    )
    mock_api.put("/presigned/dataset_info.json").mock(return_value=Response(200))

    result = runner.invoke(app, ["--json", "file-stores", "upload-parquet", str(parquet)])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["file_store_id"] == "fs_missing_info"
    assert payload["dataset_info_status"] == "uploaded"


def test_upload_parquet_rejects_non_parquet(runner, mock_api: respx.Router, tmp_path: Path) -> None:
    bad = tmp_path / "not-parquet.txt"
    bad.write_text("hello")
    result = runner.invoke(app, ["--json", "file-stores", "upload-parquet", str(bad)])
    assert result.exit_code == 1
    err = json.loads(result.stderr)
    assert ".parquet" in err["error"]


def test_delete_file_stores_by_id(runner, mock_api: respx.Router) -> None:
    mock_api.delete("/api/v1/file-stores/fs-123").mock(
        return_value=Response(200, json={"id": "fs-123", "deleted": True})
    )
    mock_api.delete("/api/v1/file-stores/fs-456").mock(
        return_value=Response(200, json={"id": "fs-456", "deleted": True})
    )

    result = runner.invoke(app, ["--json", "file-stores", "delete", "fs-123", "fs-456"])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["deleted"] == [
        {"id": "fs-123", "deleted": True},
        {"id": "fs-456", "deleted": True},
    ]


def test_delete_file_stores_by_name(runner, mock_api: respx.Router) -> None:
    mock_api.get("/api/v1/file-stores").mock(
        return_value=Response(
            200,
            json={
                "stores": [
                    {
                        "id": "fs-1",
                        "name": "cli-demo-requirement-check",
                        "source": "parquet_upload",
                        "storage_backend": "s3",
                        "content_type": "audio_text_pairs",
                        "file_count": 1,
                        "size_bytes": 4400,
                        "total_duration_seconds": None,
                        "created_at": "2026-04-22T00:00:00Z",
                    },
                    {
                        "id": "fs-2",
                        "name": "cli-demo-requirement-check",
                        "source": "parquet_upload",
                        "storage_backend": "s3",
                        "content_type": "audio_text_pairs",
                        "file_count": 1,
                        "size_bytes": 4400,
                        "total_duration_seconds": None,
                        "created_at": "2026-04-22T00:00:01Z",
                    },
                    {
                        "id": "fs-3",
                        "name": "demo-cli-upload-no-manifest-json",
                        "source": "parquet_upload",
                        "storage_backend": "s3",
                        "content_type": "audio_text_pairs",
                        "file_count": 1,
                        "size_bytes": 4400,
                        "total_duration_seconds": None,
                        "created_at": "2026-04-22T00:00:02Z",
                    },
                    {
                        "id": "fs-4",
                        "name": "demo-cli-upload-no-manifest",
                        "source": "parquet_upload",
                        "storage_backend": "s3",
                        "content_type": "audio_text_pairs",
                        "file_count": 1,
                        "size_bytes": 4400,
                        "total_duration_seconds": None,
                        "created_at": "2026-04-22T00:00:03Z",
                    },
                ],
                "total": 4,
                "limit": 200,
                "offset": 0,
            },
        )
    )
    mock_api.delete("/api/v1/file-stores/fs-1").mock(
        return_value=Response(200, json={"id": "fs-1", "deleted": True})
    )
    mock_api.delete("/api/v1/file-stores/fs-2").mock(
        return_value=Response(200, json={"id": "fs-2", "deleted": True})
    )
    mock_api.delete("/api/v1/file-stores/fs-3").mock(
        return_value=Response(200, json={"id": "fs-3", "deleted": True})
    )
    mock_api.delete("/api/v1/file-stores/fs-4").mock(
        return_value=Response(200, json={"id": "fs-4", "deleted": True})
    )

    result = runner.invoke(
        app,
        [
            "--json",
            "file-stores",
            "delete-by-name",
            "cli-demo-requirement-check",
            "demo-cli-upload-no-manifest-json",
            "demo-cli-upload-no-manifest",
        ],
    )
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert sorted(item["id"] for item in payload["deleted"]) == ["fs-1", "fs-2", "fs-3", "fs-4"]
    assert sorted(payload["requested_names"]) == [
        "cli-demo-requirement-check",
        "demo-cli-upload-no-manifest",
        "demo-cli-upload-no-manifest-json",
    ]



def test_upload_folder_json(runner, mock_api: respx.Router, tmp_path: Path) -> None:
    folder = tmp_path / "dataset"
    folder.mkdir()
    (folder / "a.wav").write_bytes(b"RIFF....WAVE")
    (folder / "a.txt").write_text("hello")
    (folder / "b.vtt").write_text("WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nhi\n")

    mock_api.post("/api/v1/file-stores/upload-urls").mock(
        return_value=Response(
            200,
            json={
                "file_store_id": "fs_folder",
                "files": [
                    {
                        "filename": "a.wav",
                        "upload_url": "https://studio.trelis.com/presigned/a.wav",
                        "content_type": "audio/wav",
                        "expires_in": 7200,
                    },
                    {
                        "filename": "a.txt",
                        "upload_url": "https://studio.trelis.com/presigned/a.txt",
                        "content_type": "text/plain",
                        "expires_in": 7200,
                    },
                    {
                        "filename": "b.vtt",
                        "upload_url": "https://studio.trelis.com/presigned/b.vtt",
                        "content_type": "text/vtt",
                        "expires_in": 7200,
                    },
                ],
            },
        )
    )
    mock_api.put("/presigned/a.wav").mock(return_value=Response(200))
    mock_api.put("/presigned/a.txt").mock(return_value=Response(200))
    mock_api.put("/presigned/b.vtt").mock(return_value=Response(200))

    result = runner.invoke(app, ["--json", "file-stores", "upload-folder", str(folder)])
    assert result.exit_code == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["file_store_id"] == "fs_folder"
    assert payload["uploaded_files"] == 3
    assert payload["skipped_unsupported"] == 0


def test_upload_folder_rejects_duplicate_basenames(runner, mock_api: respx.Router, tmp_path: Path) -> None:
    folder = tmp_path / "dataset"
    (folder / "part1").mkdir(parents=True)
    (folder / "part2").mkdir(parents=True)
    (folder / "part1" / "same.wav").write_bytes(b"a")
    (folder / "part2" / "same.wav").write_bytes(b"b")

    result = runner.invoke(app, ["--json", "file-stores", "upload-folder", str(folder)])
    assert result.exit_code == 1
    err = json.loads(result.stderr)
    assert "Duplicate basenames" in err["error"]


def test_upload_folder_rejects_unsupported_files(runner, mock_api: respx.Router, tmp_path: Path) -> None:
    folder = tmp_path / "dataset"
    folder.mkdir()
    (folder / "a.wav").write_bytes(b"RIFF")
    (folder / "notes.md").write_text("nope")

    result = runner.invoke(app, ["--json", "file-stores", "upload-folder", str(folder)])
    assert result.exit_code == 1
    err = json.loads(result.stderr)
    assert "Unsupported files found" in err["error"]


def test_transcription_submit_reports_nested_error_detail(runner, mock_api: respx.Router, tmp_path: Path) -> None:
    body = tmp_path / "request.json"
    body.write_text('{"file_store_id": "fs_123"}')

    mock_api.post("/api/v1/transcription").mock(
        return_value=Response(
            400,
            json={
                "detail": {
                    "code": "FILESTORE_CONTRACT",
                    "message": "transcription requires a column_manifest; this FileStore has none.",
                }
            },
        )
    )

    result = runner.invoke(app, ["--json", "transcription", "submit", "--body", str(body)])
    assert result.exit_code == 2, result.stderr
    err = json.loads(result.stderr)
    assert "FILESTORE_CONTRACT" in err["error"]
    assert "transcription requires a column_manifest" in err["error"]


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
