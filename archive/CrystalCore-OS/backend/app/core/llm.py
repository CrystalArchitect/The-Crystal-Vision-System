import logging
import threading
from pathlib import Path
from typing import Any, Literal

from app.core.config import get_settings

logger = logging.getLogger(__name__)

Tier = Literal["auto", "webllm", "local", "cloud"]

_llm: Any = None
_llm_lock = threading.Lock()


class ModelNotAvailableError(RuntimeError):
    """Raised when the local GGUF model file hasn't been downloaded yet."""


class CloudNotConfiguredError(RuntimeError):
    """Raised when the cloud tier has no ANTHROPIC_API_KEY configured."""


class AllTiersUnavailableError(RuntimeError):
    """Raised when every tier the request was allowed to use has failed."""


def _load_local_llm() -> Any:
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

    logger.info("loading local LLM from %s", model_path)
    _llm = Llama(
        model_path=str(model_path),
        n_ctx=settings.llm_n_ctx,
        n_threads=settings.llm_n_threads,
        verbose=False,
    )
    return _llm


def generate_local(prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
    """Tier 2: self-hosted llama.cpp model running on this machine."""
    llm = _load_local_llm()
    # A single llama.cpp context isn't safe for concurrent calls; FastAPI
    # runs sync routes in a thread pool, so serialize access here.
    with _llm_lock:
        result = llm.create_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
    return result["choices"][0]["message"]["content"]


def generate_cloud(prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
    """Tier 3: hosted API fallback, used when self-hosting can't serve the request."""
    settings = get_settings()
    if not settings.anthropic_api_key:
        raise CloudNotConfiguredError(
            "cloud tier not configured -- set ANTHROPIC_API_KEY to enable it"
        )

    # Imported lazily, same reasoning as llama_cpp above: local-only
    # deployments shouldn't need the `anthropic` package installed to boot.
    from anthropic import Anthropic

    logger.info("cloud LLM call via %s", settings.cloud_llm_model)
    client = Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(
        model=settings.cloud_llm_model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def generate(
    prompt: str,
    max_tokens: int = 256,
    temperature: float = 0.7,
    tier: Tier = "auto",
) -> tuple[str, str]:
    """Three-tier completion. Returns (completion, tier_used).

    Tiers, cheapest/most-private first:
      1. **webllm** -- runs entirely in the caller's browser (WebGPU), never
         reaches this server. Not implemented here by definition; a client
         that already tried it and failed sends tier="webllm", which this
         function treats identically to "auto" (it has nothing left to try
         client-side, so it cascades through the two tiers this process
         actually hosts).
      2. **local** -- `generate_local()`, this machine's llama.cpp model.
      3. **cloud** -- `generate_cloud()`, hosted API fallback.

    tier="local" or tier="cloud" pins the request to that tier only (no
    fallback) -- useful for testing a specific tier, or when a caller
    explicitly wants to avoid the cloud tier's cost/privacy trade-off.
    tier="auto" (default) and tier="webllm" cascade local -> cloud.
    """
    if tier == "local":
        return generate_local(prompt, max_tokens, temperature), "local"

    if tier == "cloud":
        return generate_cloud(prompt, max_tokens, temperature), "cloud"

    # "auto" / "webllm": local first (free, private, on this machine),
    # cloud as fallback only if local can't serve the request right now.
    try:
        return generate_local(prompt, max_tokens, temperature), "local"
    except ModelNotAvailableError as local_exc:
        try:
            return generate_cloud(prompt, max_tokens, temperature), "cloud"
        except CloudNotConfiguredError as cloud_exc:
            raise AllTiersUnavailableError(
                f"local tier unavailable ({local_exc}); cloud tier unavailable ({cloud_exc})"
            ) from cloud_exc
