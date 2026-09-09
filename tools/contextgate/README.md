# contextgate — deterministic RED/GREEN check for drafts

A small, stdlib-only checker: feed it a text or markdown file, it tells
you RED or GREEN and why, with no model call in the loop. What it
checks and doesn't, and the human-override mechanism, are specified in
[`SURFACE.md`](SURFACE.md) — read that first, this file is just how to
run it.

## Run it

```
python3 gate.py examples/bad-magellan.txt
python3 gate.py examples/good-sourced-brief.txt
python3 tests/test_gate.py
```

`gate.py` exits 0 on a final GREEN, 1 on a final RED (a human override
can force either). `tests/test_gate.py` is plain `unittest`, five
cases, no dependencies, no network:

```
$ python3 tests/test_gate.py -v
test_bad_magellan_example_is_red ... ok
test_good_sourced_example_is_green ... ok
test_human_override_forces_green_despite_violations ... ok
test_positioning_rule_flags_unsourced_hub_claim ... ok
test_positioning_rule_passes_when_sourced ... ok

Ran 5 tests in 0.001s

OK
```

## Scope, honestly

v0.1.0 checks exactly the three claim shapes that PR #146's fabricated
Small Council briefings actually contained (see `SURFACE.md` §"Why this
exists"), against the two fixture files in `examples/`. It has not been
run yet against real draft material outside those fixtures — doing that
against the pending Lynas/ELA drafts is a natural next step, not
something this pass claims to have done. It does not check dates,
spelling, tone, or whether a cited source is real; a fabricated citation
in the right shape passes today, same as a real one.

## Layout

- `gate.py` — the runtime; also importable (`from gate import evaluate,
  Verdict`) for scripting or a future paste-box UI.
- `tests/test_gate.py` — the self-tests above.
- `examples/` — the two fixtures the tests and the commands above run
  against; each carries a header comment on where its content came from.
