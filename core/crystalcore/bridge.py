# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""CrystalBridge — the MCP stdio server that lets a guest AI meet the companion.

Reconstructed spec: the original `docs/CRYSTALBRIDGE.md` design doc was lost
along with the machine this project was first built on. This file's shape is
inferred from `core/crystalcore/gate.py` (the consent gate it must call before
doing anything), `docs/guides/MCP-Guest.md` / `docs/guides/Access.md` (the CLI and env var
contract guests already assume: `python -m crystalcore.bridge --profile
<name>`, guest identity via the CRYSTALBRIDGE_GUEST env var), and
`core/profiles/default/bridge_config.json` (the config shape). `recall` and
`teach` are deliberately thin, obvious wrappers around the mind's existing
memory methods rather than new memory logic of their own — this file grants
*access* to the mind, it doesn't reimplement it.

Every tool call passes through ConsentGate.check() first. Nothing runs for a
guest who isn't approved for that specific tool.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from crystalcore.config import BridgeConfig
from crystalcore.gate import ConsentGate

# The mind is an ordinary subpackage of this one, so reaching it needs no
# importlib alias any more — but it is still imported *lazily*, inside the
# functions that need it, and deliberately so. `crystalcore.mind` pulls in
# `requests` at module level; importing it here would make `status` — which
# touches no memory and needs no model — fail on a bridge-only install that
# has just `mcp`. Laziness is what lets requirements-bridge.txt stay honest
# about declaring one dependency.

SRC_ROOT = Path(__file__).resolve().parent.parent          # core/
REPO_ROOT = SRC_ROOT.parent                                 # repo root (parent of core/ and vision/)
# The front-of-house interface. Only the *memory* the mind reads lives
# beside the interface; that is what this path is for.
#: Where the human's companion keeps its profiles. There is no default and
#: deliberately no guess: the companion is installed wherever its owner chose
#: to clone it, so this process cannot know the path and must be told.
MEMORY_DIR_ENV = "CRYSTALBRIDGE_MEMORY_DIR"


class MemoryNotConfigured(SystemExit):
    """Raised instead of running against a memory folder nobody nominated."""

    def __init__(self, detail: str):
        super().__init__(
            f"CrystalBridge: {detail}\n\n"
            "This server hands a guest access to a human's actual companion "
            "memory, so it will not guess where that is.\n"
            "Point it at the profiles folder of a running companion:\n\n"
            f"    python -m crystalcore.bridge --memory-dir <path> --profile <name>\n"
            f"    {MEMORY_DIR_ENV}=<path> python -m crystalcore.bridge --profile <name>\n\n"
            "<path> is the folder holding the named profiles — for a companion "
            "installed from Clementine-ai-companion, that is normally "
            "clementine/clementine_profiles/."
        )


def _profiles_root() -> Path:
    """The profiles folder, as nominated. Fails closed if it is not.

    This used to be derived from a path inside this repository, back when the
    companion lived here. It no longer does, and a derived path would now
    resolve to somewhere that does not exist — at which point the mind would
    helpfully *create* it and the bridge would serve a guest an empty
    companion, while `teach` wrote memories into a folder the human never
    reads. Silence is the danger here, not absence: an empty companion looks
    like a companion with nothing to say.

    So: no default, no fallback, no creation. Told, or stopped.
    """
    raw = os.environ.get(MEMORY_DIR_ENV, "").strip()
    if not raw:
        raise MemoryNotConfigured(f"{MEMORY_DIR_ENV} is not set")
    root = Path(raw).expanduser()
    if not root.is_dir():
        raise MemoryNotConfigured(f"{raw} is not a directory")
    return root


class Bridge:
    """Holds the one companion instance this bridge process gives guests
    limited, gated access to."""

    def __init__(self, config: BridgeConfig, guest: str, token: str = ""):
        self.config = config
        self.guest = guest
        self.token = token
        self.gate = ConsentGate(config)
        self._companion = None
        # The request_id of the most recent check(), so refuse_scope can
        # join a door-5 decision to the pending.jsonl line doors 1–4 just
        # wrote. Empty until the first check.
        self.last_request_id = ""

    def refuse(self, tool: str, arguments: dict[str, Any]) -> dict[str, Any]:
        result = self.gate.check(self.guest, tool, arguments, token=self.token)
        self.last_request_id = result.request_id
        return None if result.allowed else result.as_refusal_payload()

    def refuse_scope(self, tool: str, kind: str,
                     arguments: dict[str, Any],
                     types: tuple[str, ...] = ()) -> dict[str, Any]:
        result = self.gate.require_scope(
            self.guest, tool, kind, arguments,
            types=types, request_id=self.last_request_id)
        return None if result.allowed else result.as_refusal_payload()

    @property
    def companion(self):
        """The companion, loaded lazily so `status` doesn't need Ollama.

        The mind's own `profiles.profile_dir()` resolves relative to the
        *calling process's* working directory. This bridge runs from
        `core/`, a different cwd than the terminal interface uses
        (wherever the human cloned the companion), so the path
        is built explicitly and anchored to the interface — otherwise the
        bridge would open a second, empty profile dir wherever it happened
        to be launched from, instead of the memory the human actually sees.
        """
        if self._companion is None:
            from crystalcore.mind import CrystalCore

            safe_name = "".join(
                c for c in self.config.profile if c.isalnum() or c in "-_ "
            ).strip()
            memory_dir = _profiles_root() / safe_name
            self._companion = CrystalCore(memory_dir=str(memory_dir))
        return self._companion


def build_server(bridge: Bridge) -> FastMCP:
    mcp = FastMCP("crystalbridge")

    @mcp.tool()
    def status() -> dict[str, Any]:
        """Who you are to this bridge, and what you're allowed to do."""
        refusal = bridge.refuse("status", {})
        if refusal:
            return refusal
        grant = bridge.config.guest(bridge.guest)
        return {
            "ok": True,
            "guest": bridge.guest,
            "profile": bridge.config.profile,
            "tools": grant.tools if grant else [],
            "read_types": grant.read_types if grant else [],
            "write_types": grant.write_types if grant else [],
        }

    @mcp.tool()
    def recall(query: str = "") -> dict[str, Any]:
        """Recall what the companion remembers, optionally filtered by a query."""
        refusal = bridge.refuse("recall", {"query": query})
        if refusal:
            return refusal
        # recall serves the semantic layer (notes and facts) — the only
        # layer with per-entry visibility consent today. Episodic and
        # reflective grants gain content only when per-entry sharing
        # reaches those layers; until then this declaration keeps the
        # refusal honest about what is actually behind the door.
        refusal = bridge.refuse_scope("recall", "read", {"query": query},
                                      types=("semantic",))
        if refusal:
            return refusal
        grant = bridge.config.guest(bridge.guest)
        memory_text = bridge.companion._memory_block(
            query, visible=set(grant.read_scope))
        return {"ok": True, "memory": memory_text or "(nothing shared with you yet)"}

    @mcp.tool()
    def teach(text: str) -> dict[str, Any]:
        """Teach the companion something to remember permanently."""
        refusal = bridge.refuse("teach", {"text": text})
        if refusal:
            return refusal
        refusal = bridge.refuse_scope("teach", "write", {"text": text},
                                      types=("semantic",))
        if refusal:
            return refusal
        grant = bridge.config.guest(bridge.guest)
        bridge.companion.remember(text, visibility=grant.write_scope[0])
        return {"ok": True, "remembered": text,
                "visibility": grant.write_scope[0]}

    @mcp.tool()
    def message(text: str) -> dict[str, Any]:
        """Leave a message for the human. Recorded, but not automatically
        folded into the companion's memory — that's what `teach` is for."""
        refusal = bridge.refuse("message", {"text": text})
        if refusal:
            return refusal
        from crystalcore.audit import append_audit

        append_audit(
            bridge.config.profile_dir / "messages.jsonl",
            guest=bridge.guest,
            tool="message",
            arguments={"text": text},
            decision="delivered",
        )
        return {"ok": True, "delivered": True}

    return mcp


def mint_token(profile: str, guest: str) -> None:
    """Mint a per-guest secret, store only its hash in bridge_config.json,
    and print the secret once. The secret goes in the guest launcher's
    CRYSTALBRIDGE_TOKEN; it is never stored here."""
    import json
    import secrets

    from crystalcore.config import PROFILES_DIR, write_json_atomic
    from crystalcore.gate import token_hash

    guest = guest.strip().lower()
    config_path = PROFILES_DIR / profile / "bridge_config.json"
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    if guest not in raw.get("guests", {}):
        raise SystemExit(f"no guest '{guest}' in {config_path} — add the "
                         "grant first, then mint its token")
    secret = secrets.token_urlsafe(32)
    raw["guests"][guest]["token_hash"] = token_hash(secret)
    write_json_atomic(config_path, raw)
    print(f"Minted for '{guest}' (hash stored in {config_path.name}).")
    print("Give this secret to that guest's launcher config only — it is")
    print("shown once and not stored:\n")
    print(f"  CRYSTALBRIDGE_TOKEN={secret}")


def set_revocation(profile: str, guest: str, action: str, reason: str) -> None:
    """Append a revocation or reinstatement to the profile's ledger.

    Runtime and durable: the gate reads the ledger on every check, so this
    takes effect immediately for a bridge already running, and survives any
    restart. It needs no memory dir — consent state is the profile's, not
    the companion's.
    """
    from crystalcore.audit import append_audit
    from crystalcore.config import PROFILES_DIR
    from crystalcore.revocation import append_revocation, revocations_path

    guest = guest.strip().lower()
    profile_dir = PROFILES_DIR / profile
    config = BridgeConfig.load(profile)
    if config.guest(guest) is None:
        # Revoking an unknown name is allowed — a guest removed from the
        # config can still be on the ledger — but say so, since a typo here
        # would otherwise revoke nobody in silence.
        print(f"note: '{guest}' is not in {profile}/bridge_config.json — "
              "recording the ledger entry anyway.")
    append_revocation(revocations_path(profile_dir),
                      guest=guest, action=action, reason=reason)
    append_audit(config.audit_path, guest=guest, tool=action,
                 arguments={"reason": reason}, decision=f"{action}d",
                 reason=reason, detail={"by": "human"})
    if action == "revoke":
        print(f"Revoked '{guest}'. Takes effect on their next request — no "
              "restart needed. Reinstate with:\n"
              f"  python -m crystalcore.bridge --reinstate {guest}")
    else:
        print(f"Reinstated '{guest}'. Their standing grant applies again; "
              "nothing was minted or widened.")


def review_memories(profile: str) -> None:
    """One-time migration helper: walk private memories and let the human
    mark chosen ones shared. Everything stays private unless marked."""
    config = BridgeConfig.load(profile)
    from crystalcore.mind import CrystalCore

    safe_name = "".join(
        c for c in config.profile if c.isalnum() or c in "-_ "
    ).strip()
    companion = CrystalCore(memory_dir=str(_profiles_root() / safe_name))
    entries = [("note", n["text"], n) for n in companion.memory.notes] + [
        ("fact", f"{k}: {v['value']}", v) for k, v in companion.memory.facts.items()
    ]
    private = [(kind, text, store) for kind, text, store in entries
               if store.get("visibility", "private") != "shared"]
    if not private:
        print("Nothing private to review — all memories are already shared "
              "or there are none.")
        return
    print(f"{len(private)} private memories. 's' shares one with guests, "
          "Enter keeps it private, 'q' stops:\n")
    changed = 0
    for kind, text, store in private:
        answer = input(f"[{kind}] {text}\n  share? [s/Enter/q] ").strip().lower()
        if answer == "q":
            break
        if answer == "s":
            store["visibility"] = "shared"
            changed += 1
        else:
            store["visibility"] = "private"
    companion.save()
    print(f"\n{changed} shared; everything else stays private.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="crystalcore.bridge")
    parser.add_argument("--profile", default="default")
    parser.add_argument("--memory-dir", default="",
                        help="the companion's profiles folder. Required, "
                             f"unless {MEMORY_DIR_ENV} is set. There is no "
                             "default: this server will not guess where a "
                             "human's memory lives.")
    parser.add_argument("--mint-token", metavar="GUEST",
                        help="mint a provenance secret for GUEST and exit")
    parser.add_argument("--revoke", metavar="GUEST",
                        help="withdraw GUEST's consent — immediate, durable, "
                             "no restart needed — and exit")
    parser.add_argument("--reinstate", metavar="GUEST",
                        help="lift a revocation for GUEST and exit")
    parser.add_argument("--reason", default="",
                        help="recorded alongside --revoke/--reinstate")
    parser.add_argument("--review-memories", action="store_true",
                        help="interactively mark private memories as shared")
    args = parser.parse_args()
    if args.memory_dir:
        os.environ[MEMORY_DIR_ENV] = args.memory_dir

    if args.mint_token:
        mint_token(args.profile, args.mint_token)
        return
    if args.revoke:
        set_revocation(args.profile, args.revoke, "revoke", args.reason)
        return
    if args.reinstate:
        set_revocation(args.profile, args.reinstate, "reinstate", args.reason)
        return
    if args.review_memories:
        review_memories(args.profile)
        return

    guest = os.environ.get("CRYSTALBRIDGE_GUEST", "")
    token = os.environ.get("CRYSTALBRIDGE_TOKEN", "")
    config = BridgeConfig.load(args.profile)
    # Resolved here, before the server starts, though the companion itself is
    # loaded lazily. Left to the lazy path, an unconfigured bridge would come
    # up clean, report nothing, and fail only when a guest called a tool —
    # putting the error in front of the guest instead of the operator who can
    # fix it. Fail closed *and* early.
    _profiles_root()
    bridge = Bridge(config, guest, token)
    server = build_server(bridge)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
