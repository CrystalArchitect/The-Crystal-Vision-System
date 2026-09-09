#!/usr/bin/env python3
"""
Downloads the GGUF weights used by POST /api/v1/admin/generate.

Run this once before starting the server (see backend/README.md). Skips the
download if the file is already present, so it's safe to re-run.

Configure via environment variables:
    MODEL_REPO_ID   Hugging Face repo (default: Qwen/Qwen2.5-3B-Instruct-GGUF)
    MODEL_FILENAME  File within that repo (default: qwen2.5-3b-instruct-q4_k_m.gguf)
    MODEL_DIR       Local destination directory (default: models)

MODEL_DIR/MODEL_FILENAME must match LLM_MODEL_PATH in .env for the server to
find the file it downloads.
"""

import os
from pathlib import Path

from huggingface_hub import hf_hub_download

REPO_ID = os.environ.get("MODEL_REPO_ID", "Qwen/Qwen2.5-3B-Instruct-GGUF")
FILENAME = os.environ.get("MODEL_FILENAME", "qwen2.5-3b-instruct-q4_k_m.gguf")
MODEL_DIR = Path(os.environ.get("MODEL_DIR", "models"))


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    dest = MODEL_DIR / FILENAME

    if dest.exists():
        print(f"{dest} already present, skipping download")
        return

    print(f"Downloading {FILENAME} from {REPO_ID}...")
    downloaded_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME, local_dir=MODEL_DIR)
    print(f"Downloaded to {downloaded_path}")


if __name__ == "__main__":
    main()
