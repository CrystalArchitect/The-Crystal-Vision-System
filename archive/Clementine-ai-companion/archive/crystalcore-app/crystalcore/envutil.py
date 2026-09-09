"""Small local helpers: load git-ignored .env without extra dependencies."""

from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: str | Path = ".env") -> bool:
    """Load KEY=value lines into os.environ if the key is not already set.

    Returns True if a file was read. Never overwrites existing env vars.
    """
    p = Path(path)
    if not p.is_file():
        return False
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
    except OSError:
        return False
    return True


def xai_api_key_present() -> bool:
    """True if XAI_API_KEY is set and non-empty.

    Loads a project-root .env once if the key is missing from the process env,
    so late checks after cwd is the project folder still work.
    """
    if os.environ.get("XAI_API_KEY", "").strip():
        return True
    # Best-effort: project .env next to CWD (clementine launch dir).
    load_dotenv(".env")
    return bool(os.environ.get("XAI_API_KEY", "").strip())
