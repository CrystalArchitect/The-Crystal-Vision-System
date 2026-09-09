"""Local speech-to-text via faster-whisper (OpenAI Whisper weights).

Optional. If faster-whisper is not installed, the transcribe route answers
503 with a clear install line. Audio never leaves this machine: the model
runs in-process, same as Ollama for chat.

Not Meta. Whisper is OpenAI's model; we run the open weights locally.
"""

from __future__ import annotations

from pathlib import Path

_model = None
_model_size: str | None = None


def available() -> bool:
    try:
        import faster_whisper  # noqa: F401
        return True
    except ImportError:
        return False


def transcribe(path: str | Path, model_size: str = "base") -> str:
    """Return plain text for an audio file on disk. Raises ImportError if
    faster-whisper is missing; raises RuntimeError on empty/failed decode.
    """
    global _model, _model_size
    from faster_whisper import WhisperModel

    size = (model_size or "base").strip() or "base"
    if _model is None or _model_size != size:
        # int8 on CPU keeps modest machines honest.
        _model = WhisperModel(size, device="cpu", compute_type="int8")
        _model_size = size
    segments, _info = _model.transcribe(str(path))
    text = " ".join(s.text.strip() for s in segments if s.text).strip()
    if not text:
        raise RuntimeError("no speech detected")
    return text
