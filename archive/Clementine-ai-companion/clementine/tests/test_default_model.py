"""A model name is not guessed for a service this machine does not host."""
import pytest
from crystalcore.companion import Clementine


def test_a_remote_provider_without_a_model_is_refused(tmp_path):
    with pytest.raises(ValueError) as e:
        Clementine(memory_dir=str(tmp_path), llm_provider="openai",
                   llm_endpoint="https://api.example-vendor.test/v1/chat/completions")
    assert "needs an explicit model" in str(e.value)
    assert "--llm-model" in str(e.value), "the error must name the fix"


def test_it_no_longer_sends_a_local_tag_to_a_vendor(tmp_path):
    """The actual defect: llama3.1:8b on the wire to OpenAI, and in the log."""
    try:
        c = Clementine(memory_dir=str(tmp_path), llm_provider="openai",
                       llm_endpoint="https://api.example-vendor.test/v1/chat/completions")
    except ValueError:
        return
    assert c.wire_model != "llama3.1:8b", \
        "a local model tag was about to be sent to a remote vendor"


def test_an_explicit_model_is_accepted(tmp_path):
    c = Clementine(memory_dir=str(tmp_path), llm_provider="openai",
                   llm_endpoint="https://api.example-vendor.test/v1/chat/completions",
                   llm_model="gpt-5-5")
    assert c.wire_model == "gpt-5-5"


def test_local_is_untouched(tmp_path):
    c = Clementine(memory_dir=str(tmp_path))
    assert c.wire_model == "llama3.1:8b"


def test_the_grok_alias_still_works(tmp_path):
    c = Clementine(memory_dir=str(tmp_path), llm_provider="grok")
    assert c.wire_model, "existing profiles must not break"


def test_the_missing_address_is_reported_before_the_missing_model(tmp_path):
    """Both refuse now, so which speaks first is a decision, not an accident.

    "Where does this conversation go" is the question the consent gate exists
    to answer. The model name only matters once somewhere has been chosen.
    """
    with pytest.raises(ValueError) as e:
        Clementine(memory_dir=str(tmp_path), llm_provider="openai")
    assert "endpoint" in str(e.value)


# ------------------------------------------------- how the refusal is met

def _run(*args):
    """The terminal entry point, as a person actually meets it."""
    import subprocess, sys as _s, pathlib
    root = pathlib.Path(__file__).resolve().parents[1]
    return subprocess.run([_s.executable, str(root / "clementine.py"), *args],
                          capture_output=True, text=True, input="", timeout=60,
                          cwd=str(root))


def test_a_refusal_reads_as_a_refusal_not_a_crash(tmp_path):
    r = _run("--memory-dir", str(tmp_path), "--llm-provider", "openai")

    assert r.returncode == 2, "a refusal should exit deliberately"
    assert "Traceback" not in r.stderr, \
        "the line naming the fix must not be buried in a stack trace"
    assert "Cannot start:" in r.stderr
    assert "--llm-endpoint" in r.stderr


def test_it_does_not_announce_local_mode_while_configured_for_a_vendor(tmp_path):
    """The banner used to say 'local mode' before anything was resolved, so a
    remote setup announced local and then contradicted itself."""
    out = _run("--memory-dir", str(tmp_path),
               "--llm-provider", "openai",
               "--llm-endpoint", "https://api.example-vendor.test/v1/chat/completions",
               "--llm-model", "gpt-5-5").stdout

    assert "local" not in out.lower(), out
    assert "api.example-vendor.test" in out, "it must name where it will reach"


def test_it_says_so_plainly_when_everything_is_local(tmp_path):
    out = _run("--memory-dir", str(tmp_path)).stdout
    assert "stays on this machine" in out
