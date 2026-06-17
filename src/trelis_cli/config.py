"""Configuration: base URL, config file paths, defaults."""

from __future__ import annotations

import os
from pathlib import Path

from platformdirs import user_config_dir

DEFAULT_BASE_URL = "https://studio.trelis.com"
KEYRING_SERVICE = "trelis-cli"
KEYRING_USER = "default"


def config_dir() -> Path:
    return Path(user_config_dir("trelis", appauthor=False))


def config_file() -> Path:
    return config_dir() / "config.toml"


def base_url() -> str:
    """Resolve base URL: env > config file > default.

    Note: the upstream OpenAPI spec has no `servers:` block, so this is the
    only source of truth for where the SDK points.
    """
    env = os.environ.get("TRELIS_BASE_URL")
    if env:
        return env.rstrip("/")
    # Config file lookup deferred until we add a real config writer; default
    # is fine for now.
    return DEFAULT_BASE_URL
