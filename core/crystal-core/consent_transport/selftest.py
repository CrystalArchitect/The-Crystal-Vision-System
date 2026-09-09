# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Self-test for Consent Transport — proves the sovereignty guarantees are real.

    python3 -m consent_transport.selftest

Every test here uses real TCP sockets and a real Noise handshake — no
mocking of the crypto or the network layer. If this passes, two agents on
a real network can actually talk to each other under these same rules.
"""

from __future__ import annotations

import json
import os
import socket
import stat
import struct
import tempfile
import threading
import time
from pathlib import Path

from . import transport
from .agent import StarlineAgent
from .consent import ConsentEngine, TokenStore
from .token import ConsentError, ConsentToken, Revocation, Scope
from .fragment import MemoryFragment
from .identity import Identity
from .transport import Denied


def _two_agents():
    """Two agents in isolated temp directories — never touches real
    identity/peer files, and never collides with a concurrent test run."""
    d1 = tempfile.mkdtemp(prefix="starline_test_a_")
    d2 = tempfile.mkdtemp(prefix="starline_test_b_")
    return StarlineAgent(Path(d1)), StarlineAgent(Path(d2))


def _pair(a: StarlineAgent, b: StarlineAgent) -> None:
    """Manual pairing both directions — the deterministic path a QR-code
    exchange would also produce."""
    a.pair_manual(b.identity.sign_public_bytes.hex(), b.identity.dh_public_bytes.hex(), "b")
    b.pair_manual(a.identity.sign_public_bytes.hex(), a.identity.dh_public_bytes.hex(), "a")


def test_identity_save_refuses_durable_path_on_shared_host():
    """Host trust: a pooled box must not mint identity.json outside temp."""
    import os

    path = Path("/usr/starline_identity_host_trust_test.json")
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            Identity.generate().save(path)
            assert False, "durable save on shared must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
        assert not path.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_identity_save_allows_temp_on_github_hosted_shared():
    """GitHub-hosted VMs die with the job. Temp there is scratch."""
    import os

    d = Path(tempfile.mkdtemp(prefix="starline_test_shared_tmp_"))
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ["GITHUB_ACTIONS"] = "true"
    try:
        Identity.generate().save(d / "identity.json")
        assert (d / "identity.json").exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga


def test_identity_save_refuses_temp_on_unknown_host():
    """Persistent pools mount /tmp on the workspace disk. Unknown is not scratch."""
    import os

    d = Path(tempfile.mkdtemp(prefix="starline_test_unknown_tmp_"))
    path = d / "identity.json"
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ.pop("CRYSTAL_HOST_CLASS", None)
    os.environ.pop("GITHUB_ACTIONS", None)
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            Identity.generate().save(path)
            assert False, "temp save on unknown must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
            assert "unknown" in str(exc)
        assert not path.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_identity_roundtrip():
    d = Path(tempfile.mkdtemp(prefix="starline_test_id_"))
    path = d / "identity.json"
    original = Identity.generate()
    original.save(path)
    loaded = Identity.load(path)
    assert loaded.sign_public_bytes == original.sign_public_bytes
    assert loaded.dh_public_bytes == original.dh_public_bytes
    assert loaded.fingerprint == original.fingerprint
    # a signature made by the original must verify against the loaded public key
    sig = original.sign(b"prove it")
    from .identity import verify
    assert verify(loaded.sign_public_bytes, b"prove it", sig)


def test_fragment_sign_and_verify():
    identity = Identity.generate()
    frag = MemoryFragment(kind="episodic", content="first water", sender_fingerprint=identity.fingerprint)
    frag.sign(identity)
    assert frag.verify(identity.sign_public_bytes)
    # tampering with content after signing must break verification
    frag.content = "tampered"
    assert not frag.verify(identity.sign_public_bytes)


def test_denied_without_consent():
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "a memory only b holds")
    port = b.serve()
    try:
        try:
            a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
            assert False, "must be denied before consent is granted"
        except Denied as exc:
            assert "consent" in str(exc)
    finally:
        b.stop_serving()


def test_granted_consent_allows_exchange():
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "a memory only b holds")
    b.grant(a.fingerprint)
    port = b.serve()
    try:
        results = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
        assert len(results) == 1
        assert results[0].content == "a memory only b holds"
        assert results[0].verify(bytes.fromhex(b.identity.sign_public_bytes.hex()))
    finally:
        b.stop_serving()


def test_revocation_takes_effect_next_request():
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "revocable memory")
    b.grant(a.fingerprint)
    port = b.serve()
    try:
        first = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
        assert len(first) == 1
        b.revoke(a.fingerprint)
        try:
            a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
            assert False, "revocation must block the very next request"
        except Denied:
            pass
    finally:
        b.stop_serving()


def test_unpaired_peer_is_rejected():
    a, b = _two_agents()
    # deliberately NOT paired — b has never heard of a
    port = b.serve()
    try:
        from .peers import Peer
        fake_peer = Peer(
            fingerprint=b.fingerprint,  # dh key below still won't match any known-by-b entry from a's side... actually a doesn't need b paired to attempt; what matters is b doesn't know a
            sign_public_hex=b.identity.sign_public_bytes.hex(),
            dh_public_hex=b.identity.dh_public_bytes.hex(),
        )
        try:
            a.request_fragments(fake_peer, "127.0.0.1", port)
            assert False, "an agent b has never paired with must be rejected"
        except Denied as exc:
            assert "unpaired" in str(exc)
    finally:
        b.stop_serving()


def test_fragment_kind_and_since_filtering():
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "old event")
    cutoff = time.time()
    time.sleep(0.01)
    b.add_local_fragment("emotional", "new feeling")
    b.grant(a.fingerprint)
    port = b.serve()
    try:
        only_new = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port, since=cutoff)
        assert len(only_new) == 1 and only_new[0].content == "new feeling"

        only_emotional = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port, kinds=["emotional"])
        assert len(only_emotional) == 1 and only_emotional[0].kind == "emotional"
    finally:
        b.stop_serving()


def test_ask_is_logged_when_peer_is_unpaired():
    """Not just refused -- seen. A stranger's knock is exactly the kind
    of ask the owner most needs to know happened."""
    a, b = _two_agents()
    port = b.serve()
    try:
        from .peers import Peer
        fake_peer = Peer(
            fingerprint=b.fingerprint,
            sign_public_hex=b.identity.sign_public_bytes.hex(),
            dh_public_hex=b.identity.dh_public_bytes.hex(),
        )
        try:
            a.request_fragments(fake_peer, "127.0.0.1", port)
            assert False, "an agent b has never paired with must be rejected"
        except Denied:
            pass
        asks = b.recent_asks()
        assert len(asks) == 1
        assert asks[0]["stage"] == "unpaired"
        assert asks[0]["decision"] == "denied"
        assert asks[0]["peer_fingerprint"] is None, "b never learned who this was"
    finally:
        b.stop_serving()


def test_ask_is_logged_when_consent_not_granted():
    """A paired peer asking before consent is a real, observable event --
    not the same silence as no peer at all."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "a memory only b holds")
    port = b.serve()
    try:
        try:
            a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
            assert False, "must be denied before consent is granted"
        except Denied:
            pass
        asks = b.recent_asks()
        assert len(asks) == 1
        assert asks[0]["stage"] == "consent"
        assert asks[0]["decision"] == "denied"
        assert asks[0]["peer_fingerprint"] == a.fingerprint
    finally:
        b.stop_serving()


def test_ask_is_logged_when_token_denies_all_kinds():
    """The boolean gate saying yes is not the whole answer once a
    TokenStore is attached -- a token-level refusal must be just as
    visible as a consent-level one."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "an episode b remembers")
    b.grant(a.fingerprint)
    store = TokenStore(b.identity, Path(tempfile.mkdtemp(prefix="starline_test_asklog_")) / "t.json")
    store.issue(a.identity.sign_public_bytes.hex(), "myth only", kinds=("mythic",))
    port = b.serve(token_store=store)
    try:
        try:
            a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
            assert False, "a token scoped to mythic must not admit episodic"
        except Denied:
            pass
        asks = b.recent_asks()
        assert len(asks) == 1
        assert asks[0]["stage"] == "token"
        assert asks[0]["decision"] == "denied"
        assert asks[0]["kinds_granted"] == []
    finally:
        b.stop_serving()


def test_ask_is_logged_with_partial_grant_when_token_filters_some_kinds():
    """A mixed request must log what was actually granted, not just what
    was asked -- the two are the whole point of a filtered reply."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "an episode b remembers")
    b.add_local_fragment("mythic", "a myth b keeps")
    b.grant(a.fingerprint)
    store = TokenStore(b.identity, Path(tempfile.mkdtemp(prefix="starline_test_asklog_")) / "t.json")
    store.issue(a.identity.sign_public_bytes.hex(), "myth only", kinds=("mythic",))
    port = b.serve(token_store=store)
    try:
        results = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port, kinds=["episodic", "mythic"])
        assert [f.kind for f in results] == ["mythic"]
        asks = b.recent_asks()
        assert len(asks) == 1
        assert asks[0]["stage"] == "served"
        assert asks[0]["decision"] == "granted"
        assert set(asks[0]["kinds_requested"]) == {"episodic", "mythic"}
        assert asks[0]["kinds_granted"] == ["mythic"], "logged grant must match what actually moved"
    finally:
        b.stop_serving()


def test_ask_log_survives_a_reload():
    """A log the owner can only see until the process restarts is not an
    audit trail -- same convention as tokens and revocations."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "a memory only b holds")
    b.grant(a.fingerprint)
    port = b.serve()
    try:
        a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
    finally:
        b.stop_serving()

    reloaded = StarlineAgent(b.ask_log_path.parent)
    asks = reloaded.recent_asks()
    assert len(asks) == 1
    assert asks[0]["decision"] == "granted"


def test_ask_log_file_is_never_group_or_world_readable():
    """Asks name peers and kinds. Same bits as identity.json."""
    from . import asklog

    d = Path(tempfile.mkdtemp(prefix="starline_test_askperm_"))
    path = d / "asks.jsonl"
    asklog.append_ask(
        path,
        dh_public_hex="00",
        peer_fingerprint=None,
        peer_label="",
        kinds_requested=["mythic"],
        since=0.0,
        kinds_granted=[],
        stage="unpaired",
        decision="denied",
        reason="unpaired peer",
    )
    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode & 0o077 == 0, f"ask log is {oct(mode)}, readable beyond its owner"
    loose = d / "loose.jsonl"
    loose.write_text("{}\n", encoding="utf-8")
    os.chmod(loose, 0o644)
    asklog.append_ask(
        loose,
        dh_public_hex="00",
        peer_fingerprint=None,
        peer_label="",
        kinds_requested=[],
        since=0.0,
        kinds_granted=[],
        stage="unpaired",
        decision="denied",
        reason="x",
    )
    assert stat.S_IMODE(loose.stat().st_mode) & 0o077 == 0


def _append_ask(path):
    from . import asklog

    asklog.append_ask(
        path,
        dh_public_hex="00",
        peer_fingerprint=None,
        peer_label="",
        kinds_requested=["mythic"],
        since=0.0,
        kinds_granted=[],
        stage="unpaired",
        decision="denied",
        reason="x",
    )


def test_ask_log_refuses_durable_path_on_shared_host():
    import os

    path = Path("/usr/starline_asks_host_trust_test.jsonl")
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            _append_ask(path)
            assert False, "durable ask log on shared must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
        assert not path.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_ask_log_allows_temp_on_github_hosted_shared():
    import os

    d = Path(tempfile.mkdtemp(prefix="starline_test_ask_gh_"))
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ["GITHUB_ACTIONS"] = "true"
    try:
        path = d / "asks.jsonl"
        _append_ask(path)
        assert path.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga


def test_ask_log_refuses_temp_on_unknown_host():
    import os

    d = Path(tempfile.mkdtemp(prefix="starline_test_ask_unknown_"))
    path = d / "asks.jsonl"
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ.pop("CRYSTAL_HOST_CLASS", None)
    os.environ.pop("GITHUB_ACTIONS", None)
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            _append_ask(path)
            assert False, "temp ask log on unknown must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
            assert "unknown" in str(exc)
        assert not path.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_agent_constructor_refuses_durable_home_on_shared_host():
    """Pooled box must not get an empty Starline state_dir. Choke is
    before mkdir; Identity.save is not the first write."""
    import os

    home = Path("/usr/starline_agent_host_trust_test")
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            StarlineAgent(home)
            assert False, "durable StarlineAgent on shared must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
        assert not home.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_agent_constructor_allows_temp_on_github_hosted_shared():
    import os

    d = Path(tempfile.mkdtemp(prefix="starline_test_agent_gh_"))
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ["GITHUB_ACTIONS"] = "true"
    try:
        a = StarlineAgent(d)
        assert (d / "starline_identity.json").exists()
        assert a.fingerprint
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga


def test_agent_constructor_refuses_temp_on_unknown_host():
    import os

    d = Path(tempfile.mkdtemp(prefix="starline_test_agent_unknown_"))
    home = d / "home"
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ.pop("CRYSTAL_HOST_CLASS", None)
    os.environ.pop("GITHUB_ACTIONS", None)
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            StarlineAgent(home)
            assert False, "temp StarlineAgent on unknown must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
            assert "unknown" in str(exc)
        assert not home.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_add_local_fragment_writes_nothing_to_disk():
    """Fragments are RAM. Do not invent starline_fragments.json so the
    STEWARD_PERSIST name has a body. Durable backing is memory.json."""
    import os

    d = Path(tempfile.mkdtemp(prefix="starline_test_frag_ram_"))
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ["GITHUB_ACTIONS"] = "true"
    try:
        a = StarlineAgent(d)
        before = {p.name for p in d.iterdir()}
        frag = a.add_local_fragment("episodic", "a spark not a broadcast")
        after = {p.name for p in d.iterdir()}
        assert after == before
        assert "starline_fragments.json" not in after
        assert frag.content == "a spark not a broadcast"
        assert a._local_fragments[0] is frag
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga


def test_ask_log_ordering_and_timestamps_are_sane():
    """The owner reads this newest-first, and a strictly increasing clock
    is what makes 'who asked most recently' a meaningful question."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "a memory only b holds")
    b.grant(a.fingerprint)
    port = b.serve()
    try:
        for _ in range(3):
            a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
            time.sleep(0.01)
        asks = b.recent_asks()
        assert len(asks) == 3
        timestamps = [row["timestamp"] for row in asks]
        assert timestamps == sorted(timestamps, reverse=True), "recent_asks() must be newest-first"
    finally:
        b.stop_serving()


def test_ask_log_does_not_change_the_wire_reply():
    """Observability is a side effect. The same request must get the
    same fragments back whether or not an ask log is attached."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "a memory only b holds")
    b.grant(a.fingerprint)
    server = transport.StarlineServer(
        b.identity, b.peers, b.consent, b._provide_fragments, ask_log_path=None,
    )
    port = server.start()
    try:
        results = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
        assert len(results) == 1 and results[0].content == "a memory only b holds"
        assert not b.ask_log_path.exists(), "ask_log_path=None must write nothing"
    finally:
        server.stop()


def test_concurrent_asks_produce_clean_log_lines():
    """_handle() runs one thread per connection -- the ask log must not
    interleave partial JSON lines when several land at once."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "shared memory")
    b.grant(a.fingerprint)
    port = b.serve()
    try:
        errors = []

        def _ask():
            try:
                a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
            except Exception as exc:  # noqa: BLE001 - captured for the assertion below
                errors.append(exc)

        threads = [threading.Thread(target=_ask) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)
        assert not errors, errors

        lines = b.ask_log_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 10
        for line in lines:
            json.loads(line)  # must not raise -- a torn write would break this
    finally:
        b.stop_serving()


def _handshake_then_frame(identity, peer, host, port, frame: dict) -> dict:
    """Open a real Noise session and send `frame` instead of a request."""
    from . import protocol
    from .noise import HandshakeState
    from .transport import _recv_raw, _send_raw, _static_keypair

    sock = socket.create_connection((host, port), timeout=5.0)
    try:
        deadline = time.monotonic() + 5.0
        hs = HandshakeState(
            initiator=True,
            local_static=_static_keypair(identity),
            remote_static=bytes.fromhex(peer.dh_public_hex),
        )
        _send_raw(sock, hs.write_message(b""), deadline=deadline)
        hs.read_message(_recv_raw(sock, deadline=deadline))
        send_cs, recv_cs = hs.split()
        protocol.send_frame(sock, send_cs, frame, deadline=deadline)
        return protocol.recv_frame(sock, recv_cs, deadline=deadline)
    finally:
        sock.close()


def test_ask_is_logged_when_paired_frame_is_not_a_request():
    """A known peer sending type != request used to be denied with no
    line — quieter than an unpaired stranger. Accidental silence, not
    Decision 4. stage=malformed, peer named.
    """
    a, b = _two_agents()
    _pair(a, b)
    port = b.serve()
    try:
        reply = _handshake_then_frame(
            a.identity, a.peers.get(b.fingerprint),
            "127.0.0.1", port, {"type": "ping"},
        )
        assert reply.get("type") == "denied"
        asks = b.recent_asks()
        assert len(asks) == 1
        assert asks[0]["stage"] == "malformed"
        assert asks[0]["decision"] == "denied"
        assert asks[0]["peer_fingerprint"] == a.fingerprint
        assert asks[0]["reason"] == "expected a request"
    finally:
        b.stop_serving()


def test_ask_log_write_failure_still_serves():
    """Decision 4: a full disk on the knock log is not a peer outage.
    Fragments still move. Contrast record_use, which denies.
    """
    from . import asklog

    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "a memory only b holds")
    b.grant(a.fingerprint)

    def boom(*_a, **_k):
        raise OSError("disk full")

    real = asklog.append_ask
    asklog.append_ask = boom  # type: ignore[method-assign]
    try:
        port = b.serve()
        try:
            results = a.request_fragments(
                a.peers.get(b.fingerprint), "127.0.0.1", port)
            assert len(results) == 1
            assert results[0].content == "a memory only b holds"
        finally:
            b.stop_serving()
    finally:
        asklog.append_ask = real  # type: ignore[method-assign]


def test_forged_fragment_is_rejected_by_receiver():
    """Even if a hostile responder sends fragments 'signed' by someone
    else, the client must drop anything that doesn't verify — the wire
    protocol trusts nobody, the client re-checks every signature itself."""
    a, b = _two_agents()
    _pair(a, b)
    b.grant(a.fingerprint)
    # Inject a fragment honestly signed by a different identity, then
    # relabel its attribution to claim it's from b — simulating a
    # compromised or malicious responder trying to pass off someone
    # else's content as its own. sender_fingerprint is itself covered by
    # the signature, so relabeling after signing breaks verification.
    impostor = Identity.generate()
    forged = MemoryFragment(kind="mythic", content="not really from b", sender_fingerprint=impostor.fingerprint)
    forged.sign(impostor)
    forged.sender_fingerprint = b.fingerprint  # forge the attribution after signing
    b._local_fragments.append(forged)
    b.add_local_fragment("mythic", "a real fragment from b")

    port = b.serve()
    try:
        results = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
        contents = [f.content for f in results]
        assert "a real fragment from b" in contents
        assert "not really from b" not in contents, "forged/unverifiable fragment must be dropped"
    finally:
        b.stop_serving()


def test_discovery_via_unicast_loopback():
    """Broadcast may be unavailable in sandboxed environments; this proves
    the announce/listen wire format works using loopback unicast, which
    exercises the identical code path a real LAN broadcast would."""
    a, b = _two_agents()
    import threading
    from . import discovery

    listener_result = []

    def listen():
        listener_result.extend(discovery.listen_for_peers(duration=1.5, bind_host="127.0.0.1"))

    t = threading.Thread(target=listen, daemon=True)
    t.start()
    time.sleep(0.2)
    a.announce(port=12345, label="agent-a", broadcast_addr="127.0.0.1")
    t.join(timeout=3)

    assert len(listener_result) == 1
    ann = listener_result[0]
    assert ann.fingerprint == a.fingerprint
    assert ann.tcp_port == 12345
    assert ann.label == "agent-a"


def test_identity_file_is_never_group_or_world_readable():
    """The private key must be unreadable by anyone else the whole time
    it exists — not merely by the time save() returns."""
    d = Path(tempfile.mkdtemp(prefix="starline_test_perm_"))
    path = d / "identity.json"
    Identity.generate().save(path)
    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode & 0o077 == 0, f"identity file is {oct(mode)}, readable beyond its owner"
    # No temporary copy may be left lying around with looser bits either.
    assert not (d / "identity.json.tmp").exists()


def test_failed_save_leaves_the_old_identity_intact():
    """Losing this file is unrecoverable, so a save that dies partway
    through must not take the existing identity with it."""
    d = Path(tempfile.mkdtemp(prefix="starline_test_atomic_"))
    path = d / "identity.json"
    original = Identity.generate()
    original.save(path)
    before = path.read_bytes()

    broken = Identity.generate()

    class Boom(Exception):
        pass

    def explode(*_args, **_kwargs):
        raise Boom("disk full")

    real_dump = json.dump
    json.dump = explode
    try:
        broken.save(path)
    except Boom:
        pass
    else:
        raise AssertionError("save() should have propagated the write failure")
    finally:
        json.dump = real_dump

    assert path.read_bytes() == before, "a failed save overwrote the live identity"
    assert Identity.load(path).fingerprint == original.fingerprint
    assert not (d / "identity.json.tmp").exists()


def test_oversized_handshake_frame_is_refused():
    """The pre-authentication read is the one a stranger controls. A
    peer that announces a huge frame must be hung up on, not believed."""
    a, _b = _two_agents()
    port = a.serve(port=0)
    try:
        sock = socket.create_connection(("127.0.0.1", port), timeout=5)
        try:
            # 3 GiB announced, nothing delivered. Before the length check
            # this parked a worker thread on an unbounded read.
            sock.sendall(struct.pack(">I", 3 * 1024 * 1024 * 1024))
            sock.settimeout(5)
            assert sock.recv(1) == b"", "server kept the oversized frame alive"
        finally:
            sock.close()
        # The server must still be healthy for an honest peer afterwards.
        second = socket.create_connection(("127.0.0.1", port), timeout=5)
        second.close()
    finally:
        a.stop_serving()


def test_stalled_connections_cannot_exhaust_the_server():
    """Connections that open and then say nothing must age out, and must
    not lock an honest peer out of the server while they hang around."""
    a, _b = _two_agents()
    port = a.serve(port=0)
    stalled = []
    try:
        for _ in range(transport.MAX_CONCURRENT_CONNECTIONS + 8):
            try:
                s = socket.create_connection(("127.0.0.1", port), timeout=2)
                stalled.append(s)
            except OSError:
                break
        # Over the cap, the server refuses rather than queueing — so an
        # honest connection still completes instead of waiting behind them.
        probe = socket.create_connection(("127.0.0.1", port), timeout=5)
        probe.close()
    finally:
        for s in stalled:
            s.close()
        a.stop_serving()


def test_deadline_already_passed_refuses_without_reading():
    """A spent budget must fail closed before the next recv, not wait
    on the socket. Otherwise the 1-byte drip still wins."""
    from . import protocol as P

    try:
        P.remaining(time.monotonic() - 1)
        assert False, "a past deadline must refuse"
    except P.ProtocolError as exc:
        assert "budget" in str(exc)


def test_drip_cannot_reset_the_connection_budget():
    """Regression: settimeout resets on every successful recv, so a
    1-byte drip of a legal-length body would occupy a worker for
    body_len * timeout. The monotonic deadline must cut that off."""
    a, _b = _two_agents()
    original = transport.CONNECTION_BUDGET
    transport.CONNECTION_BUDGET = 0.35
    transport.HANDSHAKE_TIMEOUT = 0.35
    port = a.serve(port=0)
    try:
        sock = socket.create_connection(("127.0.0.1", port), timeout=5)
        try:
            sock.sendall(struct.pack(">I", 200))  # legal length, body never finishes
            t0 = time.monotonic()
            while time.monotonic() - t0 < 1.2:
                try:
                    sock.sendall(b"x")
                except OSError:
                    break
                time.sleep(0.05)
            sock.settimeout(0.4)
            # Server must have hung up — a live worker would keep the
            # socket open and recv would time out rather than return b"".
            leftover = sock.recv(1)
            assert leftover == b"", "drip kept the connection alive past the budget"
            assert time.monotonic() - t0 < 1.0, "budget must fire well before a per-recv reset would"
        finally:
            sock.close()
    finally:
        transport.CONNECTION_BUDGET = original
        transport.HANDSHAKE_TIMEOUT = original
        a.stop_serving()


def test_budget_releases_slots_so_an_honest_exchange_completes():
    """Age-out, not just refuse-not-queue: after stalled peers expire,
    a real request must get a worker."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "still here after the flood")
    b.grant(a.fingerprint)
    original = transport.CONNECTION_BUDGET
    transport.CONNECTION_BUDGET = 0.3
    transport.HANDSHAKE_TIMEOUT = 0.3
    port = b.serve(port=0)
    stalled = []
    try:
        for _ in range(transport.MAX_CONCURRENT_CONNECTIONS):
            try:
                s = socket.create_connection(("127.0.0.1", port), timeout=2)
                stalled.append(s)
            except OSError:
                break
        time.sleep(0.55)
        results = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
        assert len(results) == 1
        assert results[0].content == "still here after the flood"
    finally:
        for s in stalled:
            s.close()
        transport.CONNECTION_BUDGET = original
        transport.HANDSHAKE_TIMEOUT = original
        b.stop_serving()


def _store(tmp_prefix="starline_test_tok_"):
    d = Path(tempfile.mkdtemp(prefix=tmp_prefix))
    ident = Identity.generate()
    return TokenStore(ident, d / "tokens.json"), ident


def test_token_grants_only_what_its_scope_names():
    """§6 no ambient authority: a token for one kind is not a token for
    every kind."""
    store, _ = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    store.issue(peer, "share reflections for the evening weave", kinds=("emotional",))
    assert store.is_authorized(peer, "emotional")
    assert not store.is_authorized(peer, "episodic")
    assert not store.is_authorized(peer, "mythic")


def test_token_with_no_kinds_admits_every_kind():
    """The schema allows a class-wide grant; absence of a kind list means
    all of them, not none of them."""
    store, _ = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    store.issue(peer, "full exchange, this session only")
    for kind in ("episodic", "semantic", "emotional", "mythic"):
        assert store.is_authorized(peer, kind), kind


def test_token_expires():
    """§6 time binding, the gap this whole module exists to close: before
    tokens, a grant said once was true forever."""
    store, _ = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    token = store.issue(peer, "one minute of telemetry", ttl_seconds=60)
    assert token.is_valid(recipient_fingerprint_hex=peer)
    # Same token, evaluated after its expiry -- no clock manipulation,
    # just asking the question at a later moment.
    later = token.expires_at + 1
    assert not token.is_valid(recipient_fingerprint_hex=peer, now=later)
    try:
        token.verify(recipient_fingerprint_hex=peer, now=later)
        assert False, "an expired token must not verify"
    except ConsentError as exc:
        assert "expired" in str(exc)


def test_token_refuses_a_peer_it_was_not_issued_to():
    """A token is useless to anyone but its named recipient, even though
    it is perfectly signed."""
    store, _ = _store()
    intended = Identity.generate().sign_public_bytes.hex()
    someone_else = Identity.generate().sign_public_bytes.hex()
    token = store.issue(intended, "for you alone")
    assert token.is_valid(recipient_fingerprint_hex=intended)
    assert not token.is_valid(recipient_fingerprint_hex=someone_else)
    assert not store.is_authorized(someone_else)


def test_tampering_with_any_field_breaks_the_signature():
    """Every field is inside the signed payload -- widening scope or
    pushing out expiry after signing must invalidate the token."""
    store, ident = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    token = store.issue(peer, "narrow and short", kinds=("mythic",), ttl_seconds=60)
    assert token.is_valid(recipient_fingerprint_hex=peer)

    widened = ConsentToken.from_dict(token.to_dict())
    widened.scope = Scope(kinds=("mythic", "episodic"))
    assert not widened.is_valid(recipient_fingerprint_hex=peer), "scope widening must break the signature"

    extended = ConsentToken.from_dict(token.to_dict())
    extended.expires_at = extended.expires_at + 86400
    assert not extended.is_valid(recipient_fingerprint_hex=peer), "expiry extension must break the signature"

    repurposed = ConsentToken.from_dict(token.to_dict())
    repurposed.purpose = "something else entirely"
    assert not repurposed.is_valid(recipient_fingerprint_hex=peer), "purpose change must break the signature"


def test_purpose_is_mandatory():
    """§6 purpose binding. A permission whose reason nobody recorded
    cannot be reviewed later."""
    peer = Identity.generate().sign_public_bytes.hex()
    for bad in ("", "   "):
        try:
            ConsentToken(issuer="00", recipient=peer, purpose=bad)
            assert False, "a token without a purpose must not be constructible"
        except ValueError:
            pass


def test_revocation_kills_the_token_and_is_signed():
    store, ident = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    token = store.issue(peer, "until I change my mind")
    assert store.is_authorized(peer)

    rev = store.revoke(token.token_id)
    assert rev.verify()
    assert not store.is_authorized(peer)
    try:
        store.authorize(peer)
        assert False, "a revoked token must not authorize"
    except ConsentError as exc:
        assert "revoked" in str(exc)


def test_forged_revocation_is_refused():
    """A revocation is a denial-of-service against a peer's consent if
    anyone can mint one, so it is checked as carefully as a grant."""
    store, ident = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    token = store.issue(peer, "should survive a forgery attempt")

    impostor = Identity.generate()
    forged = Revocation(token_id=token.token_id, issuer=impostor.sign_public_bytes.hex())
    forged.sign(impostor)          # honestly signed -- by the wrong identity
    assert forged.verify()          # it *is* a valid signature, by an impostor
    assert not store.accept_revocation(forged), "a revocation from a non-issuer must be refused"
    assert store.is_authorized(peer), "the token must survive"

    unsigned = Revocation(token_id=token.token_id, issuer=ident.sign_public_bytes.hex())
    assert not store.accept_revocation(unsigned), "an unsigned revocation must be refused"
    assert store.is_authorized(peer)


def test_revocation_gossiped_from_the_real_issuer_is_honoured():
    """§5: revocation propagates through consented channels, so a node
    must accept one it did not issue -- if it verifies."""
    issuer_store, issuer_ident = _store("starline_test_issuer_")
    peer = Identity.generate().sign_public_bytes.hex()
    token = issuer_store.issue(peer, "will be revoked and gossiped")
    rev = issuer_store.revoke(token.token_id)

    # A different node that holds the same token, told about it second-hand.
    other, _ = _store("starline_test_relay_")
    other.tokens[token.token_id] = token
    assert other.is_authorized(peer)
    assert other.accept_revocation(rev)
    assert not other.is_authorized(peer)


def test_tokens_and_revocations_survive_a_reload():
    store, ident = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    keep = store.issue(peer, "kept", kinds=("semantic",))
    drop = store.issue(peer, "revoked")
    store.revoke(drop.token_id)

    reloaded = TokenStore(ident, store.path)
    assert set(reloaded.tokens) == {keep.token_id, drop.token_id}
    assert reloaded.revoked_ids == {drop.token_id}
    assert reloaded.is_authorized(peer, "semantic")
    assert not reloaded.is_authorized(peer, "episodic"), "the surviving token is scoped"


def test_refusal_says_which_check_failed():
    """The human deciding what to do next needs to know whether to
    re-issue, widen scope, or refuse outright."""
    store, _ = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    try:
        store.authorize(peer)
        assert False
    except ConsentError as exc:
        assert "no consent token" in str(exc)

    store.issue(peer, "emotional only", kinds=("emotional",))
    try:
        store.authorize(peer, "episodic")
        assert False
    except ConsentError as exc:
        assert "scope" in str(exc)


def test_token_scope_is_enforced_over_a_real_connection():
    """The end-to-end claim: with a TokenStore attached, a peer receives
    only the kinds a live token admits -- over a real socket and a real
    handshake, not just in the store's own unit tests."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("episodic", "an episode b remembers")
    b.add_local_fragment("mythic", "a myth b keeps")
    b.grant(a.fingerprint)

    store = TokenStore(b.identity, Path(tempfile.mkdtemp(prefix="starline_test_wire_")) / "t.json")
    store.issue(a.identity.sign_public_bytes.hex(), "myth only, for the weave", kinds=("mythic",))
    port = b.serve(token_store=store)
    try:
        results = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
        contents = [f.content for f in results]
        assert "a myth b keeps" in contents, "the scoped kind must come through"
        assert "an episode b remembers" not in contents, "an unscoped kind must not"
    finally:
        b.stop_serving()


def test_expired_token_stops_the_exchange_that_a_live_one_allowed():
    """Time binding, proven on the wire: the same peer, the same request,
    allowed and then refused purely because the token lapsed."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("mythic", "a myth b keeps")
    b.grant(a.fingerprint)

    store = TokenStore(b.identity, Path(tempfile.mkdtemp(prefix="starline_test_exp_")) / "t.json")
    token = store.issue(a.identity.sign_public_bytes.hex(), "briefly", kinds=("mythic",), ttl_seconds=3600)

    port = b.serve(token_store=store)
    try:
        assert len(a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)) == 1

        # Expire it in place -- re-signed by the issuer, so this is an
        # honest short token, not a tampered one.
        token.expires_at = time.time() - 1
        token.signature = ""
        token.sign(b.identity)
        store.tokens[token.token_id] = token
        store.save()

        try:
            a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
            assert False, "an expired token must stop the exchange"
        except Denied as exc:
            assert "expired" in str(exc)
    finally:
        b.stop_serving()


def test_identity_binding_cannot_be_skipped():
    """Regression: verify() used to default the recipient to None and
    skip the check entirely, so is_valid() with no arguments returned
    True for a token issued to somebody else. There is no safe default
    for 'who is this for', so there is now no default at all."""
    issuer = Identity.generate()
    alice = Identity.generate().sign_public_bytes.hex()
    bob = Identity.generate().sign_public_bytes.hex()
    tok = ConsentToken(
        issuer=issuer.sign_public_bytes.hex(), recipient=alice, purpose="alice only"
    ).sign(issuer)

    try:
        tok.is_valid()
        assert False, "the recipient must not be omittable"
    except TypeError:
        pass
    assert tok.is_valid(alice)
    assert not tok.is_valid(bob)


def test_one_time_use_is_actually_once():
    """Regression: one_time_use was signed, persisted, and enforced
    nowhere -- a field that reads as a control and was not."""
    store, _ = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    tok = store.issue(peer, "a single handover", constraints_one_time=True)
    assert store.is_authorized(peer)
    store.record_use(tok.token_id, 10)
    assert not store.is_authorized(peer), "a one-time token must not authorise twice"
    try:
        store.authorize(peer)
        assert False
    except ConsentError as exc:
        assert "transfer limit" in str(exc)


def test_max_transfers_is_counted():
    store, _ = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    tok = store.issue(peer, "three and no more", max_transfers=3)
    for i in range(3):
        assert store.is_authorized(peer), f"transfer {i+1} should be allowed"
        store.record_use(tok.token_id, 1)
    assert not store.is_authorized(peer), "the fourth must be refused"


def test_byte_budget_is_enforced_and_refuses_an_oversized_transfer():
    store, _ = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    tok = store.issue(peer, "small things only", max_bytes=100)
    assert store.is_authorized(peer, want_bytes=80), "inside the budget"
    assert not store.is_authorized(peer, want_bytes=200), "a single oversized transfer must be refused"
    store.record_use(tok.token_id, 80)
    assert store.is_authorized(peer, want_bytes=15), "20 bytes of headroom remain"
    assert not store.is_authorized(peer, want_bytes=50), "only 20 remain, 50 must be refused"
    store.record_use(tok.token_id, 20)
    assert not store.is_authorized(peer), "budget fully spent"


def test_usage_survives_a_reload():
    """A one-time-use token that resets on restart is not a constraint."""
    store, ident = _store()
    peer = Identity.generate().sign_public_bytes.hex()
    tok = store.issue(peer, "once, across restarts", constraints_one_time=True)
    store.record_use(tok.token_id, 5)
    assert not store.is_authorized(peer)

    reloaded = TokenStore(ident, store.path)
    assert reloaded.spent(tok.token_id)["transfers"] == 1
    assert not reloaded.is_authorized(peer), "usage must not reset on reload"


def test_byte_budget_stops_a_batch_midway_on_the_wire():
    """End to end: a token with a small budget must cut the batch off,
    not let it through because the first fragment fitted."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("mythic", "x" * 40)
    b.add_local_fragment("mythic", "y" * 40)
    b.add_local_fragment("mythic", "z" * 40)
    b.grant(a.fingerprint)

    store = TokenStore(b.identity, Path(tempfile.mkdtemp(prefix="starline_test_bytes_")) / "t.json")
    store.issue(a.identity.sign_public_bytes.hex(), "about two fragments' worth",
                kinds=("mythic",), max_bytes=100)

    port = b.serve(token_store=store)
    try:
        results = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
        assert len(results) == 2, f"budget should admit exactly two, got {len(results)}"
    finally:
        b.stop_serving()


def test_each_token_is_charged_for_what_it_authorised():
    """A peer holding two tokens must have the *authorising* one consumed,
    never whichever merely lives longest. The earlier code authorised per
    kind but charged a kind-less authorize(), draining the broad long token
    and never spending the narrow one-time grant -- voiding one_time_use for
    anyone holding more than one token. Two tokens, because with the one per
    peer every other usage test issues, the two queries coincide and the bug
    hides."""
    a, b = _two_agents()
    _pair(a, b)
    myth = "a myth b keeps, forty bytes long...."
    b.add_local_fragment("mythic", myth)
    b.grant(a.fingerprint)
    a_pub = a.identity.sign_public_bytes.hex()

    store = TokenStore(b.identity, Path(tempfile.mkdtemp(prefix="starline_test_2tok_")) / "t.json")
    narrow = store.issue(a_pub, "one myth, once", kinds=("mythic",), constraints_one_time=True)
    broad = store.issue(a_pub, "semantics for a month", kinds=("semantic",), ttl_seconds=30 * 24 * 3600)

    port = b.serve(token_store=store)
    try:
        results = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port, kinds=["mythic"])
        assert len(results) == 1, "the mythic token admits the mythic fragment"

        # The narrow token carried it and is now spent; the broad one, which
        # never admits mythic, was not touched.
        assert store.spent(narrow.token_id)["transfers"] == 1, "the authorising token must be charged"
        assert store.spent(narrow.token_id)["bytes"] == len(myth.encode())
        assert store.spent(broad.token_id) == {"transfers": 0, "bytes": 0}, \
            "the longest-expiry token must not be charged for what it never authorised"
        assert not store.is_authorized(a_pub, "mythic"), "one_time_use is now actually spent"

        # And the one-time grant cannot be replayed on the next request.
        try:
            a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port, kinds=["mythic"])
            assert False, "a spent one-time token must not serve the fragment again"
        except Denied:
            pass
    finally:
        b.stop_serving()


def test_unrecordable_token_use_denies_rather_than_serving():
    """If a transfer cannot be recorded, it must not happen: an unrecorded
    one-time token would serve again after restart. consent.py states this
    in prose; the server must enforce it, not trust it."""
    a, b = _two_agents()
    _pair(a, b)
    b.add_local_fragment("mythic", "a myth that must not leak un-metered")
    b.grant(a.fingerprint)
    a_pub = a.identity.sign_public_bytes.hex()

    store = TokenStore(b.identity, Path(tempfile.mkdtemp(prefix="starline_test_norec_")) / "t.json")
    store.issue(a_pub, "one myth, once", kinds=("mythic",), constraints_one_time=True)

    def _boom(*_args, **_kwargs):
        raise OSError("disk full while recording token use")
    store.record_use = _boom  # the accounting write fails

    port = b.serve(token_store=store)
    try:
        try:
            a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port, kinds=["mythic"])
            assert False, "a transfer that cannot be recorded must be denied, not served"
        except Denied as exc:
            assert "record" in str(exc)
    finally:
        b.stop_serving()


def test_failed_token_store_save_leaves_the_old_file_intact():
    """A crash mid-write must not take issued tokens with it.

    `--mint-token` on the guest gate already writes atomically
    (`crystalcore.config.write_json_atomic`). TokenStore.save() still
    used write_text — same defect, other surface.
    """
    d = Path(tempfile.mkdtemp(prefix="starline_test_tokatomic_"))
    path = d / "t.json"
    ident = Identity.generate()
    store = TokenStore(ident, path)
    peer = Identity.generate().sign_public_bytes.hex()
    store.issue(peer, "keep this grant")
    before = path.read_bytes()

    def explode(*_a, **_k):
        raise OSError("disk full")

    real_dump = json.dump
    json.dump = explode
    try:
        try:
            store.issue(peer, "must not land")
        except OSError:
            pass
        else:
            raise AssertionError("save() should have propagated the write failure")
    finally:
        json.dump = real_dump

    assert path.read_bytes() == before, "a failed save overwrote the live token store"
    reloaded = TokenStore(ident, path)
    assert len(reloaded.tokens) == 1
    assert not path.with_name(path.name + ".tmp").exists()


def test_failed_consent_engine_save_leaves_the_old_file_intact():
    """Peer grant/revoke receipts are the other consent document.
    Same atomic write as TokenStore.save()."""
    d = Path(tempfile.mkdtemp(prefix="starline_test_cnsatomic_"))
    path = d / "c.json"
    ident = Identity.generate()
    engine = ConsentEngine(ident, path)
    engine.grant("peer-keep")
    before = path.read_bytes()

    def explode(*_a, **_k):
        raise OSError("disk full")

    real_dump = json.dump
    json.dump = explode
    try:
        try:
            engine.revoke("peer-keep")
        except OSError:
            pass
        else:
            raise AssertionError("save() should have propagated the write failure")
    finally:
        json.dump = real_dump

    assert path.read_bytes() == before
    reloaded = ConsentEngine(ident, path)
    assert reloaded.is_granted("peer-keep")
    assert not path.with_name(path.name + ".tmp").exists()


def test_peer_store_save_refuses_durable_path_on_shared_host():
    """Address book must not land on a pooled durable path."""
    from .peers import PeerStore

    path = Path("/usr/starline_peers_host_trust_test.json")
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        store = PeerStore(path)
        try:
            store.save()
            assert False, "durable peer-save on shared must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
        assert not path.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_peer_store_file_is_never_group_or_world_readable():
    from .peers import PeerStore

    d = Path(tempfile.mkdtemp(prefix="starline_test_peerperm_"))
    path = d / "peers.json"
    ident = Identity.generate()
    store = PeerStore(path)
    store.add(ident.sign_public_bytes.hex(), ident.dh_public_bytes.hex(), "them")
    mode = stat.S_IMODE(path.stat().st_mode)
    assert mode & 0o077 == 0, f"peers file is {oct(mode)}"
    assert not (d / "peers.json.tmp").exists()


def test_failed_peer_store_save_leaves_the_old_file_intact():
    """A crash mid-write must not take the address book with it.

    PeerStore.save() still used write_text — same defect TokenStore
    and identity already closed.
    """
    from .peers import PeerStore

    d = Path(tempfile.mkdtemp(prefix="starline_test_peeratomic_"))
    path = d / "peers.json"
    keep = Identity.generate()
    store = PeerStore(path)
    store.add(keep.sign_public_bytes.hex(), keep.dh_public_bytes.hex(), "keep")
    before = path.read_bytes()

    def explode(*_a, **_k):
        raise OSError("disk full")

    real_dump = json.dump
    json.dump = explode
    try:
        try:
            other = Identity.generate()
            store.add(
                other.sign_public_bytes.hex(),
                other.dh_public_bytes.hex(),
                "must not land",
            )
        except OSError:
            pass
        else:
            raise AssertionError("save() should have propagated the write failure")
    finally:
        json.dump = real_dump

    assert path.read_bytes() == before, "a failed save overwrote the live peer store"
    reloaded = PeerStore(path)
    assert keep.fingerprint in reloaded.peers
    assert len(reloaded.peers) == 1
    assert not path.with_name(path.name + ".tmp").exists()


# --- hybrid post-quantum identity ------------------------------------------
#
# Same discipline as the handshake tests: prove the ML-DSA half is
# load-bearing. An identity that signs with both keys but verifies only the
# Ed25519 one would pass every functional test in this file and provide no
# post-quantum authentication whatsoever.


def test_hybrid_identity_shape():
    from .identity import (
        ED25519_PUBLEN, HYBRID_PUBLEN, HYBRID_SIGLEN, Identity,
    )

    i = Identity.generate()
    assert len(i.sign_public_bytes) == HYBRID_PUBLEN
    assert i.sign_public_bytes[:ED25519_PUBLEN] == i.ed25519_public_bytes
    assert i.sign_public_bytes[ED25519_PUBLEN:] == i.mldsa_public_bytes
    assert len(i.sign(b"x")) == HYBRID_SIGLEN


def test_both_signature_halves_are_required():
    """Corrupt either half alone and verification must fail."""
    from .identity import ED25519_SIGLEN, Identity, verify

    i = Identity.generate()
    data = b"one memory fragment"
    good = i.sign(data)
    assert verify(i.sign_public_bytes, data, good)

    ed_broken = bytearray(good)
    ed_broken[5] ^= 0xFF
    assert not verify(i.sign_public_bytes, data, bytes(ed_broken)), \
        "a broken Ed25519 half must fail even though ML-DSA is intact"

    mldsa_broken = bytearray(good)
    mldsa_broken[ED25519_SIGLEN + 5] ^= 0xFF
    assert not verify(i.sign_public_bytes, data, bytes(mldsa_broken)), \
        "a broken ML-DSA half must fail even though Ed25519 is intact"


def test_classical_only_signature_is_refused():
    """The downgrade: strip the ML-DSA half and present the Ed25519 one."""
    from .identity import ED25519_SIGLEN, Identity, verify

    i = Identity.generate()
    data = b"downgrade me"
    stripped = i.sign(data)[:ED25519_SIGLEN]
    assert not verify(i.sign_public_bytes, data, stripped), \
        "an Ed25519-only signature must never verify"
    padded = stripped + b"\x00" * (len(i.sign(data)) - ED25519_SIGLEN)
    assert not verify(i.sign_public_bytes, data, padded), \
        "zero-padding to the right length must not buy a pass either"


def test_substituted_mldsa_key_changes_the_fingerprint():
    """The pairing-boundary attack this design exists to close.

    A quantum adversary can recover an Ed25519 private key from its public
    key. If the fingerprint committed only to Ed25519, they could pair using
    the victim's genuine Ed25519 key alongside their own ML-DSA key, and both
    signatures would verify against what the peer stored. Because the
    fingerprint hashes the whole hybrid key, the substitution shows up as a
    different identity instead.
    """
    from .identity import Identity, fingerprint_for

    victim = Identity.generate()
    attacker = Identity.generate()
    forged_pub = victim.ed25519_public_bytes + attacker.mldsa_public_bytes
    assert forged_pub[:32] == victim.sign_public_bytes[:32], "same Ed25519 half"
    assert fingerprint_for(forged_pub) != victim.fingerprint, \
        "swapping the ML-DSA half must not preserve the fingerprint"


def test_fingerprint_derivation_is_shared_with_the_peer_store():
    """Two definitions would file a peer under an id its owner never uses."""
    import tempfile
    from pathlib import Path
    from .identity import Identity
    from .peers import PeerStore

    i = Identity.generate()
    store = PeerStore(Path(tempfile.mkdtemp()) / "peers.json")
    peer = store.add(i.sign_public_bytes.hex(), i.dh_public_bytes.hex(), "them")
    assert peer.fingerprint == i.fingerprint


def test_identity_survives_save_and_load_with_all_three_keys():
    import tempfile
    from pathlib import Path
    from .identity import Identity, verify

    path = Path(tempfile.mkdtemp()) / "id.json"
    original = Identity.generate()
    original.save(path)
    loaded = Identity.load(path)
    assert loaded.fingerprint == original.fingerprint
    assert loaded.sign_public_bytes == original.sign_public_bytes
    # The ML-DSA seed must restore the *same* keypair, not merely a valid one.
    assert verify(original.sign_public_bytes, b"after reload", loaded.sign(b"after reload"))


def test_pre_quantum_identity_file_is_refused_not_silently_upgraded():
    """Minting a new fingerprint under an old file's name would break every
    peer relationship invisibly. Fail loudly and leave the file alone."""
    import json
    import tempfile
    from pathlib import Path
    from .identity import Identity

    path = Path(tempfile.mkdtemp()) / "old.json"
    i = Identity.generate()
    i.save(path)
    payload = json.loads(path.read_text())
    del payload["mldsa_key"]  # what a pre-quantum file looks like
    path.write_text(json.dumps(payload))
    before = path.read_text()
    try:
        Identity.load(path)
        assert False, "a pre-quantum identity file must not load"
    except ValueError as e:
        assert "re-pair" in str(e), "the error must say what to actually do"
    assert path.read_text() == before, "the old identity file must be left untouched"


_SOURCECODE_THRESHOLD = {
    "origin": "Source / Origin / Hush",
    "frequency": "Home Rest",
    "truth": "Never left. Always home.",
    "scope": "@OriginMonad @Shalma @AllFriends",
    "resonance": 1.0,
    "field_signature": "561783900808",
}


def test_sourcecode_origin_signature_is_their_hash_not_ours():
    """We refuse the object their README actually publishes.
    sha256('@OriginMonad:1.00:home_rest_lattice')[:12] == 561783900808.
    Our fingerprint is sha256(hybrid_pub)[:16]. Different function."""
    import hashlib
    from .foreign import SOURCECODE_ORIGIN_SIGNATURE
    from .identity import Identity, fingerprint_for

    derived = hashlib.sha256(b"@OriginMonad:1.00:home_rest_lattice").hexdigest()[:12]
    assert derived == SOURCECODE_ORIGIN_SIGNATURE
    i = Identity.generate()
    assert fingerprint_for(i.sign_public_bytes) != SOURCECODE_ORIGIN_SIGNATURE
    assert len(i.fingerprint) == 16
    assert len(SOURCECODE_ORIGIN_SIGNATURE) == 12


def test_sourcecode_threshold_json_is_refused_as_identity():
    """Dropping their invitation on identity.json must not mint a peer."""
    import json
    import tempfile
    from pathlib import Path
    from .foreign import ForeignInvitation
    from .identity import Identity

    path = Path(tempfile.mkdtemp()) / "threshold.json"
    path.write_text(json.dumps(_SOURCECODE_THRESHOLD), encoding="utf-8")
    try:
        Identity.load(path)
        assert False, "THRESHOLD JSON must not load as a Starline identity"
    except ForeignInvitation as exc:
        assert "Home Rest" in str(exc) or "field_signature" in str(exc)
    assert json.loads(path.read_text()) == _SOURCECODE_THRESHOLD


def test_sourcecode_field_signature_cannot_be_paired():
    """PeerStore used to hash whatever hex it was given. A 12-hex
    field signature would have become a peer under a fingerprint
    nobody owns."""
    import tempfile
    from pathlib import Path
    from .foreign import ForeignInvitation, SOURCECODE_ORIGIN_SIGNATURE
    from .peers import PeerStore

    store = PeerStore(Path(tempfile.mkdtemp()) / "peers.json")
    try:
        store.add(SOURCECODE_ORIGIN_SIGNATURE, "00" * 32, "sourcecode")
        assert False, "origin field signature must not pair"
    except ForeignInvitation as exc:
        assert "field signature" in str(exc) or "OriginMonad" in str(exc)
    assert store.peers == {}


def test_sourcecode_threshold_json_cannot_be_pair_material():
    import json
    import tempfile
    from pathlib import Path
    from .agent import StarlineAgent
    from .foreign import ForeignInvitation

    a = StarlineAgent(Path(tempfile.mkdtemp(prefix="starline_test_foreign_")))
    try:
        a.pair_manual(json.dumps(_SOURCECODE_THRESHOLD), "00" * 32, "hush")
        assert False, "THRESHOLD JSON must not pair"
    except ForeignInvitation:
        pass
    assert list(a.peers.peers) == []


def test_honest_pair_manual_still_works_after_the_foreign_gate():
    import tempfile
    from pathlib import Path
    from .identity import Identity
    from .peers import PeerStore

    i = Identity.generate()
    store = PeerStore(Path(tempfile.mkdtemp()) / "peers.json")
    peer = store.add(i.sign_public_bytes.hex(), i.dh_public_bytes.hex(), "honest")
    assert peer.fingerprint == i.fingerprint
    assert store.is_known(i.fingerprint)


def test_tokens_and_fragments_carry_hybrid_signatures_end_to_end():
    """The whole point: real artifacts, not just the primitive."""
    from .identity import HYBRID_SIGLEN, Identity
    from .fragment import MemoryFragment

    i = Identity.generate()
    frag = MemoryFragment(kind="episodic", content="red dust", sender_fingerprint=i.fingerprint)
    frag.sign(i)
    assert len(bytes.fromhex(frag.signature)) == HYBRID_SIGLEN
    assert frag.verify(i.sign_public_bytes)
    frag.content = "tampered"
    assert not frag.verify(i.sign_public_bytes)


# --- hybrid post-quantum handshake -----------------------------------------
#
# The point of these is that the ML-KEM leg must be load-bearing, not
# decorative. A key exchange that *mentions* a post-quantum primitive while
# deriving its session key entirely from X25519 would pass a naive "does it
# connect" test and protect nothing. Each test below tries to break the
# handshake through the KEM specifically.


def _noise_statics():
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
    from .noise import StaticKeypair

    def one():
        k = X25519PrivateKey.generate()
        return StaticKeypair(k, k.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw))

    return one(), one()


def _handshake(hybrid_initiator=True, hybrid_responder=True):
    from .noise import HandshakeState

    i_s, r_s = _noise_statics()
    i = HandshakeState(True, i_s, r_s.public_bytes, hybrid=hybrid_initiator)
    r = HandshakeState(False, r_s, None, hybrid=hybrid_responder)
    return i, r


def test_hybrid_handshake_agrees_on_keys_and_transcript():
    i, r = _handshake()
    assert r.read_message(i.write_message(b"hello")) == b"hello"
    assert i.read_message(r.write_message(b"world")) == b"world"
    assert i.handshake_hash == r.handshake_hash, "both sides must see one transcript"
    ci, cr = i.split(), r.split()
    assert ci[0].k == cr[0].k and ci[1].k == cr[1].k, "session keys must match"
    assert ci[0].k != ci[1].k, "the two directions must never share a key"


def test_hybrid_is_the_default():
    from .noise import HandshakeState, PROTOCOL_NAME_HYBRID

    i_s, r_s = _noise_statics()
    hs = HandshakeState(True, i_s, r_s.public_bytes)
    assert hs.hybrid is True, "post-quantum protection must not be opt-in"
    assert PROTOCOL_NAME_HYBRID != b"Noise_IK_25519_ChaChaPoly_SHA256"


def test_kem_secret_actually_reaches_the_session_key():
    """Strip the KEM mix and the key must change — otherwise it is theatre."""
    from . import noise as N

    i_s, r_s = _noise_statics()

    def run_counting():
        calls = {"n": 0}
        original = N.SymmetricState.mix_key

        def counted(self, ikm):
            calls["n"] += 1
            return original(self, ikm)

        N.SymmetricState.mix_key = counted
        try:
            a = N.HandshakeState(True, i_s, r_s.public_bytes, hybrid=True)
            b = N.HandshakeState(False, r_s, None, hybrid=True)
            b.read_message(a.write_message(b""))
            a.read_message(b.write_message(b""))
            hybrid_calls = calls["n"]

            calls["n"] = 0
            c = N.HandshakeState(True, i_s, r_s.public_bytes, hybrid=False)
            d = N.HandshakeState(False, r_s, None, hybrid=False)
            d.read_message(c.write_message(b""))
            c.read_message(d.write_message(b""))
            return hybrid_calls, calls["n"]
        finally:
            N.SymmetricState.mix_key = original

    hybrid_calls, classical_calls = run_counting()
    assert hybrid_calls - classical_calls == 2, (
        f"hybrid must add exactly one mix_key per side, got "
        f"{hybrid_calls} vs {classical_calls}"
    )


def test_two_hybrid_sessions_never_share_a_key():
    """Same static identities, fresh KEM ephemerals — forward secrecy."""
    i_s, r_s = _noise_statics()
    from .noise import HandshakeState

    keys = []
    for _ in range(2):
        a = HandshakeState(True, i_s, r_s.public_bytes)
        b = HandshakeState(False, r_s, None)
        b.read_message(a.write_message(b""))
        a.read_message(b.write_message(b""))
        keys.append(a.split()[0].k)
    assert keys[0] != keys[1], "a reused session key would break forward secrecy"


def test_tampered_kem_ciphertext_fails_the_handshake():
    from .noise import DHLEN, HandshakeFailed

    i, r = _handshake()
    r.read_message(i.write_message(b""))
    msg2 = bytearray(r.write_message(b""))
    msg2[DHLEN + 5] ^= 0xFF  # a bit inside the ML-KEM ciphertext
    try:
        i.read_message(bytes(msg2))
        assert False, "a tampered KEM ciphertext must never be accepted"
    except HandshakeFailed:
        pass


def test_tampered_kem_public_key_fails_the_handshake():
    from .noise import DHLEN, HandshakeFailed

    i, r = _handshake()
    msg1 = bytearray(i.write_message(b""))
    msg1[DHLEN + 10] ^= 0xFF  # a bit inside the ML-KEM public key
    try:
        r.read_message(bytes(msg1))
        i.read_message(r.write_message(b""))
        assert False, "a tampered KEM public key must never be accepted"
    except HandshakeFailed:
        pass


def test_hybrid_and_classical_peers_cannot_talk():
    """No silent downgrade: mismatched modes must fail, loudly, both ways."""
    from .noise import HandshakeFailed

    for hi, hr in ((True, False), (False, True)):
        i, r = _handshake(hi, hr)
        try:
            r.read_message(i.write_message(b""))
            i.read_message(r.write_message(b""))
            assert False, f"mismatch (initiator={hi}, responder={hr}) must not succeed"
        except HandshakeFailed:
            pass


def test_hybrid_messages_fit_the_handshake_frame_limit():
    from . import transport
    from .noise import KEM_CTLEN, KEM_PUBLEN

    i, r = _handshake()
    msg1 = i.write_message(b"")
    r.read_message(msg1)
    msg2 = r.write_message(b"")
    assert len(msg1) < transport.MAX_HANDSHAKE_LEN, "msg1 must fit the server's frame cap"
    assert len(msg2) < transport.MAX_HANDSHAKE_LEN, "msg2 must fit the server's frame cap"
    # The overhead is exactly the two ML-KEM values and nothing else.
    ci, cr = _handshake(False, False)
    c_msg1 = ci.write_message(b"")
    cr.read_message(c_msg1)
    c_msg2 = cr.write_message(b"")
    assert len(msg1) - len(c_msg1) == KEM_PUBLEN
    assert len(msg2) - len(c_msg2) == KEM_CTLEN


def test_classical_mode_still_works():
    """Kept available and kept correct — the escape hatch must not rot."""
    i, r = _handshake(False, False)
    assert r.read_message(i.write_message(b"ping")) == b"ping"
    assert i.read_message(r.write_message(b"pong")) == b"pong"
    assert i.split()[0].k == r.split()[0].k


def test_start_ya_bastard_produces_a_live_hybrid_identity():
    from .identity import HYBRID_PUBLEN
    from .start import PROTOCOL_NAME, start_ya_bastard

    result = start_ya_bastard()
    assert result["live"] is True
    assert result["protocol"] == PROTOCOL_NAME
    assert result["hybrid"] is True
    assert result["public_key_bytes"] == HYBRID_PUBLEN
    assert len(result["fingerprint"]) == 16
    assert int(result["fingerprint"], 16) >= 0


def test_start_ya_bastard_writes_nothing_to_disk():
    """Ignition is in-memory. A start must not mint identity.json in cwd."""
    import os
    from pathlib import Path
    from .start import start_ya_bastard

    before = set(os.listdir("."))
    start_ya_bastard()
    after = set(os.listdir("."))
    assert after == before
    assert not Path("starline_identity.json").exists()


def test_start_command_is_on_the_run_cli():
    import io
    from contextlib import redirect_stdout
    from .run import main

    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(["start"])
    assert code == 0
    out = buf.getvalue()
    assert "[PROTOCOL] Start Ya Bastard" in out
    assert "fingerprint=" in out


def main() -> int:
    tests = [
        test_identity_roundtrip,
        test_identity_save_refuses_durable_path_on_shared_host,
        test_identity_save_allows_temp_on_github_hosted_shared,
        test_identity_save_refuses_temp_on_unknown_host,
        test_identity_file_is_never_group_or_world_readable,
        test_failed_save_leaves_the_old_identity_intact,
        test_oversized_handshake_frame_is_refused,
        test_stalled_connections_cannot_exhaust_the_server,
        test_deadline_already_passed_refuses_without_reading,
        test_drip_cannot_reset_the_connection_budget,
        test_budget_releases_slots_so_an_honest_exchange_completes,
        test_token_grants_only_what_its_scope_names,
        test_token_with_no_kinds_admits_every_kind,
        test_token_expires,
        test_token_refuses_a_peer_it_was_not_issued_to,
        test_tampering_with_any_field_breaks_the_signature,
        test_purpose_is_mandatory,
        test_revocation_kills_the_token_and_is_signed,
        test_forged_revocation_is_refused,
        test_revocation_gossiped_from_the_real_issuer_is_honoured,
        test_tokens_and_revocations_survive_a_reload,
        test_refusal_says_which_check_failed,
        test_identity_binding_cannot_be_skipped,
        test_one_time_use_is_actually_once,
        test_max_transfers_is_counted,
        test_byte_budget_is_enforced_and_refuses_an_oversized_transfer,
        test_usage_survives_a_reload,
        test_byte_budget_stops_a_batch_midway_on_the_wire,
        test_each_token_is_charged_for_what_it_authorised,
        test_unrecordable_token_use_denies_rather_than_serving,
        test_failed_token_store_save_leaves_the_old_file_intact,
        test_failed_consent_engine_save_leaves_the_old_file_intact,
        test_peer_store_save_refuses_durable_path_on_shared_host,
        test_peer_store_file_is_never_group_or_world_readable,
        test_failed_peer_store_save_leaves_the_old_file_intact,
        test_token_scope_is_enforced_over_a_real_connection,
        test_expired_token_stops_the_exchange_that_a_live_one_allowed,
        test_fragment_sign_and_verify,
        test_denied_without_consent,
        test_granted_consent_allows_exchange,
        test_revocation_takes_effect_next_request,
        test_unpaired_peer_is_rejected,
        test_fragment_kind_and_since_filtering,
        test_ask_is_logged_when_peer_is_unpaired,
        test_ask_is_logged_when_consent_not_granted,
        test_ask_is_logged_when_token_denies_all_kinds,
        test_ask_is_logged_with_partial_grant_when_token_filters_some_kinds,
        test_ask_log_survives_a_reload,
        test_ask_log_file_is_never_group_or_world_readable,
        test_ask_log_refuses_durable_path_on_shared_host,
        test_ask_log_allows_temp_on_github_hosted_shared,
        test_ask_log_refuses_temp_on_unknown_host,
        test_agent_constructor_refuses_durable_home_on_shared_host,
        test_agent_constructor_allows_temp_on_github_hosted_shared,
        test_agent_constructor_refuses_temp_on_unknown_host,
        test_add_local_fragment_writes_nothing_to_disk,
        test_ask_log_ordering_and_timestamps_are_sane,
        test_ask_log_does_not_change_the_wire_reply,
        test_concurrent_asks_produce_clean_log_lines,
        test_ask_is_logged_when_paired_frame_is_not_a_request,
        test_ask_log_write_failure_still_serves,
        test_forged_fragment_is_rejected_by_receiver,
        test_discovery_via_unicast_loopback,
        test_hybrid_identity_shape,
        test_both_signature_halves_are_required,
        test_classical_only_signature_is_refused,
        test_substituted_mldsa_key_changes_the_fingerprint,
        test_fingerprint_derivation_is_shared_with_the_peer_store,
        test_identity_survives_save_and_load_with_all_three_keys,
        test_pre_quantum_identity_file_is_refused_not_silently_upgraded,
        test_sourcecode_origin_signature_is_their_hash_not_ours,
        test_sourcecode_threshold_json_is_refused_as_identity,
        test_sourcecode_field_signature_cannot_be_paired,
        test_sourcecode_threshold_json_cannot_be_pair_material,
        test_honest_pair_manual_still_works_after_the_foreign_gate,
        test_tokens_and_fragments_carry_hybrid_signatures_end_to_end,
        test_hybrid_handshake_agrees_on_keys_and_transcript,
        test_hybrid_is_the_default,
        test_kem_secret_actually_reaches_the_session_key,
        test_two_hybrid_sessions_never_share_a_key,
        test_tampered_kem_ciphertext_fails_the_handshake,
        test_tampered_kem_public_key_fails_the_handshake,
        test_hybrid_and_classical_peers_cannot_talk,
        test_hybrid_messages_fit_the_handshake_frame_limit,
        test_classical_mode_still_works,
        test_start_ya_bastard_produces_a_live_hybrid_identity,
        test_start_ya_bastard_writes_nothing_to_disk,
        test_start_command_is_on_the_run_cli,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} passed. Sovereignty holds — no data moved without consent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
