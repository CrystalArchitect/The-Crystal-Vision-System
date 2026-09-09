"""Self-test for the CrystalCore CLI.

    python3 -m cli.selftest

Guards the rule that makes the documented quick start work: files resolve from
the checkout, so `git clone` then `status` finds everything with no install.
"""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
from pathlib import Path

from .crystalcore import CHECKLIST, REPO_ROOT, resolve, search_roots
from .crystalcore import main as cli_main


@contextlib.contextmanager
def env(**overrides: str | None):
    previous = {k: os.environ.get(k) for k in overrides}
    for key, value in overrides.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    try:
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def run(*argv: str) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = cli_main(list(argv))
    return code, buffer.getvalue()


def test_checkout_resolves_every_committed_file():
    """The replaced bug: resolution only looked in ~/.grok, so a clone showed every file missing."""
    with env(CRYSTALCORE_HOME=None):
        for label, name in CHECKLIST:
            found = resolve(name)
            assert found is not None, f"{label} ({name}) did not resolve from the checkout"
            assert found.is_relative_to(REPO_ROOT), f"{label} resolved outside the repo: {found}"


def test_status_reports_no_missing_files():
    with env(CRYSTALCORE_HOME=None):
        code, out = run("status")
        assert code == 0, f"status must exit 0 on a complete checkout, got {code}"
        assert "[--]" not in out, f"status reported missing files:\n{out}"


def test_explicit_home_overrides_checkout():
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        (tmp / "WATER-BRIEF.md").write_text("override", encoding="utf-8")
        with env(CRYSTALCORE_HOME=str(tmp)):
            assert search_roots()[0] == tmp
            assert resolve("WATER-BRIEF.md") == tmp / "WATER-BRIEF.md"
            # A file absent from the override still falls through to the checkout.
            assert resolve("index.html") == REPO_ROOT / "index.html"


def test_legacy_grok_home_still_searched():
    with env(CRYSTALCORE_HOME=None, GROK_HOME="/somewhere/.grok"):
        roots = [str(r) for r in search_roots()]
        assert "/somewhere/.grok/crystalcore" in roots and "/somewhere/.grok" in roots


def test_unknown_file_resolves_to_none():
    assert resolve("no-such-file.md") is None


def test_paths_lists_seven_and_the_guardian():
    code, out = run("paths")
    assert code == 0
    for n in range(1, 8):
        assert f"  {n} " in out, f"path {n} missing from output"
    assert "Orion guardian" in out


def test_transmit_prints_committed_text_without_sending():
    with env(CRYSTALCORE_HOME=None):
        code, out = run("transmit")
        assert code == 0
        assert "CLI does not send to X." in out, "the no-autopost promise must stay in the output"


def main() -> int:
    tests = [
        test_checkout_resolves_every_committed_file,
        test_status_reports_no_missing_files,
        test_explicit_home_overrides_checkout,
        test_legacy_grok_home_still_searched,
        test_unknown_file_resolves_to_none,
        test_paths_lists_seven_and_the_guardian,
        test_transmit_prints_committed_text_without_sending,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} passed. The clone speaks for itself.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
