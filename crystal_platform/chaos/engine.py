# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Chaos Engine — multi-seat fan-out over the live stack.

One question → N intelligence seats independently → cross-compare **counts**.
Not a verdict. Not Canon. CrystalCore governs each seat turn; TAI Echo acts;
models think. Connection ≠ merge.

Manus is excluded from Portal fan-out (async Starline guest only).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Mapping, Sequence
from uuid import uuid4

from crystal_platform.orchestration import StackOrchestrator, build_live_stack
from crystal_platform.portal import EntryChannel, PortalIdentity, PortalRequest

# Default chaos seats (Portal sync path). Manus intentionally absent.
DEFAULT_CHAOS_SEATS: tuple[str, ...] = (
    "openai.chatgpt",
    "anthropic.claude",
    "xai.grok",
    "deepseek",
    "moonshot.kimi",
    "google.gemini",
    "local.open",
)


@dataclass(frozen=True)
class SeatReply:
    provider_id: str
    status: str
    text: str
    correlation_id: str | None
    silent: bool


@dataclass(frozen=True)
class ChaosRun:
    run_id: str
    question: str
    seats: tuple[str, ...]
    replies: tuple[SeatReply, ...]
    cross_compare: Mapping[str, object] = field(default_factory=dict)

    def markdown(self) -> str:
        lines = [
            "# Chaos Engine — matrix run",
            "",
            f"**Canon:** no  ",
            f"**Run id:** `{self.run_id}`  ",
            f"**Question:** {self.question}  ",
            f"**Seats:** {', '.join(self.seats)}  ",
            "",
            "## Cross-compare (count, not verdict)",
            "",
            f"- Asked: {self.cross_compare.get('seats_asked')}  ",
            f"- Ok: {self.cross_compare.get('seats_ok')}  ",
            f"- Silent / not configured: {self.cross_compare.get('seats_silent')}  ",
            f"- Status counts: `{self.cross_compare.get('status_counts')}`  ",
            "",
            "Agreement of silence is not permission. Human publishes.",
            "",
            "---",
            "",
        ]
        for r in self.replies:
            flag = " · silent" if r.silent else ""
            lines.append(f"### `{r.provider_id}` — `{r.status}`{flag}")
            lines.append("")
            lines.append(f"> {r.text}")
            lines.append("")
            if r.correlation_id:
                lines.append(f"*correlation:* `{r.correlation_id}`")
                lines.append("")
        lines.append("*Non Solus.*")
        lines.append("")
        return "\n".join(lines)


class ChaosEngine:
    """Fan-out harness. Uses StackOrchestrator; does not bypass Core."""

    def __init__(self, stack: StackOrchestrator | None = None) -> None:
        self.stack = stack or build_live_stack(provider_ids=("local.open",))

    def run(
        self,
        question: str,
        *,
        seats: Sequence[str] | None = None,
        channel: EntryChannel = EntryChannel.API,
        display_name: str | None = "ChaosEngine",
    ) -> ChaosRun:
        chosen = tuple(seats) if seats is not None else DEFAULT_CHAOS_SEATS
        known = frozenset(self.stack.providers.ids())
        run_id = str(uuid4())
        replies: list[SeatReply] = []

        for pid in chosen:
            if pid not in known:
                replies.append(
                    SeatReply(
                        provider_id=pid,
                        status="unknown_seat",
                        text=f"[{pid}] not in live registry; skipped.",
                        correlation_id=None,
                        silent=True,
                    )
                )
                continue
            req = PortalRequest(
                text=question,
                identity=PortalIdentity(
                    steward_id=None,
                    display_name=display_name,
                    channel=channel,
                    device_attested=False,
                ),
                metadata={"provider_id": pid, "chaos_run_id": run_id},
                client_request_id=f"{run_id}:{pid}",
            )
            resp = self.stack.accept(req)
            text = resp.speech_text or ""
            silent = (
                "not configured" in text.lower()
                or "staying silent" in text.lower()
            )
            if pid == "local.open" and resp.status == "ok" and not silent:
                silent = False
            replies.append(
                SeatReply(
                    provider_id=pid,
                    status=resp.status,
                    text=text,
                    correlation_id=resp.correlation_id,
                    silent=silent,
                )
            )

        status_counts = dict(Counter(r.status for r in replies))
        silent_n = sum(1 for r in replies if r.silent)
        ok_n = sum(1 for r in replies if r.status == "ok" and not r.silent)
        compare = {
            "seats_asked": len(chosen),
            "seats_ok": ok_n,
            "seats_silent": silent_n,
            "status_counts": status_counts,
            "unanimous_silence": silent_n == len(replies) and len(replies) > 0,
            "note": "count not verdict",
        }
        return ChaosRun(
            run_id=run_id,
            question=question,
            seats=chosen,
            replies=tuple(replies),
            cross_compare=compare,
        )
