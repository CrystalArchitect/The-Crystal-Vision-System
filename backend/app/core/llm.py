import logging
import threading
from pathlib import Path
from typing import Any

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_llm: Any = None
_llm_lock = threading.Lock()


class ModelNotAvailableError(RuntimeError):
    """Raised when the GGUF model file hasn't been downloaded yet."""


def _load_llm() -> Any:
    global _llm
    if _llm is not None:
        return _llm

    settings = get_settings()
    model_path = Path(settings.llm_model_path)
    if not model_path.exists():
        raise ModelNotAvailableError(
            f"model file not found at {model_path} -- run download_model.py first"
        )

    # Imported lazily so the rest of the app can start (and be tested) even
    # in environments where llama-cpp-python or the model file isn't present.
    from llama_cpp import Llama

    logger.info("loading LLM from %s", model_path)
    _llm = Llama(
        model_path=str(model_path),
        n_ctx=settings.llm_n_ctx,
        n_threads=settings.llm_n_threads,
        verbose=False,
    )
    return _llm


def generate(prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
    llm = _load_llm()
    # A single llama.cpp context isn't safe for concurrent calls; FastAPI
    # runs sync routes in a thread pool, so serialize access here.
    with _llm_lock:
        result = llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
    return result["choices"][0]["message"]["content"]
