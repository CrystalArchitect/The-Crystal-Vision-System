# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""TCP transport — where the Noise handshake meets a real socket.

Binds to 127.0.0.1 by default, same rule as everything else in this repo
that opens a port (the Starline Weaver server does the same). Exposing this
beyond localhost/LAN is an explicit operator choice, not a default.
"""

from __future__ import annotations

import socket
import struct
import threading
import time
from pathlib import Path

from . import asklog, protocol
from .consent import ConsentEngine
from .fragment import MemoryFragment
from .identity import Identity
from .noise import HandshakeFailed, HandshakeState, StaticKeypair
from .peers import Peer, PeerStore
from .token import ConsentError

DEFAULT_PORT = 8890

# An IK handshake message is tiny and fixed-shape: 96 bytes for the
# initiator's (e, encrypted s, encrypted payload), 48 for the responder's.
# Anything claiming more than this is not a handshake. This is the one
# read that happens before we know who the peer is, so it gets the
# tightest bound in the module — an unauthenticated stranger must never
# be able to size our allocations.
MAX_HANDSHAKE_LEN = 4096

# How long an unauthenticated (and then the whole one-request) connection
# may keep a worker thread, and how many such connections may be in flight
# at once. Per-recv socket timeouts reset on every successful read — a
# 1-byte drip would never hit them — so CONNECTION_BUDGET is a monotonic
# wall-clock from accept/connect that does not reset.
CONNECTION_BUDGET = 10.0
HANDSHAKE_TIMEOUT = CONNECTION_BUDGET  # alias: tests and older call sites
MAX_CONCURRENT_CONNECTIONS = 32


def _recv_exact(
    sock: socket.socket, n: int, deadline: float | None = None
) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        protocol._arm(sock, deadline)
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise protocol.ProtocolError("connection closed mid-frame")
        buf += chunk
    return bytes(buf)


def _send_raw(
    sock: socket.socket, data: bytes, deadline: float | None = None
) -> None:
    protocol._arm(sock, deadline)
    sock.sendall(struct.pack(">I", len(data)) + data)


def _recv_raw(
    sock: socket.socket,
    max_len: int = MAX_HANDSHAKE_LEN,
    deadline: float | None = None,
) -> bytes:
    (length,) = struct.unpack(">I", _recv_exact(sock, 4, deadline))
    if length > max_len:
        raise protocol.ProtocolError("peer announced an oversized handshake frame")
    return _recv_exact(sock, length, deadline)


def _static_keypair(identity: Identity) -> StaticKeypair:
    return StaticKeypair(identity.dh_key, identity.dh_public_bytes)


class Denied(Exception):
    """The responder is aware of the request and declined it — distinct
    from a network or handshake failure."""


FragmentProvider = "Callable[[list[str], float, str], list[MemoryFragment]]"


class StarlineServer:
    """Responder role: accepts connections, authenticates the peer via the
    pinned Noise handshake, and serves requests only for peers who are
    both known (paired) and consented — checked fresh on every request,
    so a mid-session revoke takes effect on the very next connection."""

    def __init__(
        self,
        identity: Identity,
        peer_store: PeerStore,
        consent_engine: ConsentEngine,
        fragment_provider,
        host: str = "127.0.0.1",
        port: int = DEFAULT_PORT,
        token_store=None,
        ask_log_path: Path | None = asklog.DEFAULT_ASK_LOG_PATH,
    ):
        self.identity = identity
        self.peer_store = peer_store
        self.consent_engine = consent_engine
        self.fragment_provider = fragment_provider
        # Optional second gate. The boolean engine answers "may this peer
        # ask at all"; a TokenStore answers the narrower question the
        # Consent Token schema specifies -- may they have *this kind*,
        # right now, under a token that has not expired or been revoked.
        # Both must say yes. Omitted, the server behaves exactly as before,
        # which is why every existing deployment keeps working.
        #
        # No wire change is needed for this: the issuer holds its own
        # tokens and checks them before releasing anything, the same shape
        # as the consent check above it.
        self.token_store = token_store
        # Every ask this node receives, granted or not, appended here so
        # the human can see who has been knocking -- not just the grants
        # and revocations they themselves made. None disables logging.
        self.ask_log_path = ask_log_path
        self._ask_log_lock = threading.Lock()
        self.host = host
        self.port = port
        self._sock: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._slots = threading.BoundedSemaphore(MAX_CONCURRENT_CONNECTIONS)

    def _log_ask(
        self,
        *,
        dh_public_hex: str,
        peer: Peer | None,
        kinds_requested: list[str],
        since: float,
        kinds_granted: list[str],
        stage: str,
        decision: str,
        reason: str,
    ) -> None:
        if self.ask_log_path is None:
            return
        try:
            with self._ask_log_lock:
                asklog.append_ask(
                    self.ask_log_path,
                    dh_public_hex=dh_public_hex,
                    peer_fingerprint=peer.fingerprint if peer else None,
                    peer_label=peer.label if peer else "",
                    kinds_requested=kinds_requested,
                    since=since,
                    kinds_granted=kinds_granted,
                    stage=stage,
                    decision=decision,
                    reason=reason,
                )
        except OSError:
            # Law, decided 2026-08-12 (CONSENT-GATE-SPEC.md, decision 4):
            # this log is knock telemetry, and a *write* failure proceeds.
            # TypeError and friends are bugs — they must surface. A full
            # disk must not become a peer outage. The consent chain on
            # this surface fails closed on its own — pairing, peer grant,
            # token verify, and a spend that cannot be recorded denies
            # the transfer. Contrast the guest gate, where the pending
            # record is part of the consent chain (request_id joins ask
            # to answer) and an unrecordable ask refuses. Same project,
            # two records, two jobs — by decision, not by accident.
            pass

    def start(self) -> int:
        """Bind and begin serving in a background thread. Returns the
        bound port (useful when port=0 asks the OS to pick one)."""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._sock.listen(5)
        self.port = self._sock.getsockname()[1]
        self._thread = threading.Thread(target=self._serve_loop, daemon=True)
        self._thread.start()
        return self.port

    def stop(self) -> None:
        self._stop.set()
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
        if self._thread:
            self._thread.join(timeout=2)

    def _serve_loop(self) -> None:
        while not self._stop.is_set():
            try:
                conn, _addr = self._sock.accept()
            except OSError:
                return
            # Refuse rather than queue when every slot is busy: a caller
            # that is turned away retries, a caller parked on a semaphore
            # is indistinguishable from the flood that parked it.
            if not self._slots.acquire(blocking=False):
                conn.close()
                continue
            conn.settimeout(HANDSHAKE_TIMEOUT)
            threading.Thread(target=self._handle, args=(conn,), daemon=True).start()

    def _handle(self, conn: socket.socket) -> None:
        deadline = time.monotonic() + CONNECTION_BUDGET
        try:
            hs = HandshakeState(
                initiator=False, local_static=_static_keypair(self.identity), remote_static=None
            )
            msg1 = _recv_raw(conn, deadline=deadline)
            hs.read_message(msg1)
            msg2 = hs.write_message(b"")
            _send_raw(conn, msg2, deadline=deadline)

            c1, c2 = hs.split()  # c1 = initiator->responder, c2 = responder->initiator
            recv_cs, send_cs = c1, c2

            peer = self.peer_store.find_by_dh(hs.rs.hex())
            frame = protocol.recv_frame(conn, recv_cs, deadline=deadline)
            kinds_requested = frame.get("kinds", [])
            since = frame.get("since", 0.0)

            if peer is None:
                self._log_ask(
                    dh_public_hex=hs.rs.hex(), peer=None, kinds_requested=kinds_requested,
                    since=since, kinds_granted=[], stage="unpaired", decision="denied",
                    reason="unpaired peer",
                )
                protocol.send_frame(conn, send_cs, protocol.denied("unpaired peer"), deadline=deadline)
                return
            if frame.get("type") != "request":
                # Paired, but not a request. Quieter than an unpaired
                # stranger until this line existed — accidental silence,
                # not Decision 4. The peer is known; the knock is real.
                self._log_ask(
                    dh_public_hex=hs.rs.hex(), peer=peer,
                    kinds_requested=kinds_requested if isinstance(kinds_requested, list) else [],
                    since=since if isinstance(since, (int, float)) else 0.0,
                    kinds_granted=[], stage="malformed", decision="denied",
                    reason="expected a request",
                )
                protocol.send_frame(conn, send_cs, protocol.denied("expected a request"), deadline=deadline)
                return
            if not self.consent_engine.is_granted(peer.fingerprint):
                self._log_ask(
                    dh_public_hex=hs.rs.hex(), peer=peer, kinds_requested=kinds_requested,
                    since=since, kinds_granted=[], stage="consent", decision="denied",
                    reason="consent not granted",
                )
                protocol.send_frame(conn, send_cs, protocol.denied("consent not granted"), deadline=deadline)
                return

            items = self.fragment_provider(frame.get("kinds", []), frame.get("since", 0.0), peer.fingerprint)

            if self.token_store is not None:
                # Filter by what a live token actually admits, per fragment.
                # Filtering rather than refusing the whole request: a peer
                # holding a token for one kind should get that kind, not a
                # blanket denial because they also asked for another.
                #
                # Each admitted fragment is charged to the *same* token that
                # admitted it -- keyed by kind -- and a token's byte budget
                # is accumulated across the batch for that token alone. The
                # earlier version authorised per kind but charged a single
                # kind-less authorize(), which returns whichever of the
                # peer's live tokens expires latest; a peer holding two
                # tokens therefore had its one-time / transfer / byte limits
                # silently voided, the narrow grant never consumed and the
                # broad one drained by bytes it never authorised.
                #
                # Conservative edge: authorize() picks the longest-expiry
                # token that admits the kind for this fragment alone; if that
                # token's budget is already spent by earlier fragments of the
                # same batch, the fragment is dropped even where a second
                # same-kind token could still carry it. That fails safe
                # (deny, never over-serve) and only bites a peer holding
                # multiple byte-budgeted tokens of one kind.
                allowed = []
                charged: dict[str, dict] = {}  # token_id -> {"bytes": int}
                for frag in items:
                    cost = len(frag.content.encode())
                    try:
                        tok = self.token_store.authorize(
                            peer.sign_public_hex, frag.kind, want_bytes=cost
                        )
                    except ConsentError:
                        continue
                    running = charged.get(tok.token_id, {"bytes": 0})
                    # Re-check the token that will actually be charged against
                    # what this batch has already promised it, so a max_bytes
                    # budget stops mid-list instead of letting every fragment
                    # through on the same still-unspent persisted total.
                    if not self.token_store.is_authorized(
                        peer.sign_public_hex, frag.kind, want_bytes=running["bytes"] + cost
                    ):
                        continue
                    allowed.append(frag)
                    running["bytes"] += cost
                    charged[tok.token_id] = running
                if not allowed and items:
                    try:
                        self.token_store.authorize(peer.sign_public_hex)
                        reason = "no token admits the requested kinds"
                    except Exception as exc:
                        reason = str(exc)
                    self._log_ask(
                        dh_public_hex=hs.rs.hex(), peer=peer, kinds_requested=kinds_requested,
                        since=since, kinds_granted=[], stage="token", decision="denied",
                        reason=reason,
                    )
                    protocol.send_frame(conn, send_cs, protocol.denied(reason), deadline=deadline)
                    return
                if allowed:
                    # Charge each authorising token once for this exchange --
                    # one transfer per token, the bytes it actually carried --
                    # only as data is about to move, so a refused request
                    # never consumes a grant. A transfer that cannot be
                    # recorded must not happen: an unrecorded one-time token
                    # would serve again after restart, which consent.py's
                    # record_use() calls out in prose. Enforce it: deny.
                    try:
                        for token_id, rec in charged.items():
                            self.token_store.record_use(token_id, rec["bytes"])
                    except Exception:
                        self._log_ask(
                            dh_public_hex=hs.rs.hex(), peer=peer, kinds_requested=kinds_requested,
                            since=since, kinds_granted=[], stage="token", decision="denied",
                            reason="cannot record token use",
                        )
                        protocol.send_frame(conn, send_cs, protocol.denied("cannot record token use"), deadline=deadline)
                        return
                items = allowed

            self._log_ask(
                dh_public_hex=hs.rs.hex(), peer=peer, kinds_requested=kinds_requested,
                since=since, kinds_granted=sorted({f.kind for f in items}), stage="served",
                decision="granted", reason="ok",
            )
            protocol.send_frame(conn, send_cs, protocol.fragments([f.to_dict() for f in items]), deadline=deadline)
        except (HandshakeFailed, protocol.ProtocolError, OSError):
            pass  # a failed/hostile connection just gets dropped, no diagnostic leak
        finally:
            conn.close()
            self._slots.release()


class StarlineClient:
    """Initiator role: connects to a known, pinned peer and requests
    fragments. The Noise handshake itself is the authentication — if the
    peer on the other end doesn't hold the private key matching the
    pinned dh_public_hex, the handshake fails before any request is sent."""

    def __init__(self, identity: Identity):
        self.identity = identity

    def request_fragments(
        self, peer: Peer, host: str, port: int, kinds: list[str], since: float = 0.0, timeout: float = 5.0
    ) -> list[MemoryFragment]:
        sock = socket.create_connection((host, port), timeout=timeout)
        try:
            deadline = time.monotonic() + timeout
            hs = HandshakeState(
                initiator=True,
                local_static=_static_keypair(self.identity),
                remote_static=bytes.fromhex(peer.dh_public_hex),
            )
            msg1 = hs.write_message(b"")
            _send_raw(sock, msg1, deadline=deadline)
            msg2 = _recv_raw(sock, deadline=deadline)
            hs.read_message(msg2)  # raises HandshakeFailed if this isn't really `peer`

            c1, c2 = hs.split()
            send_cs, recv_cs = c1, c2

            protocol.send_frame(sock, send_cs, protocol.request(kinds, since), deadline=deadline)
            reply = protocol.recv_frame(sock, recv_cs, deadline=deadline)

            if reply.get("type") == "denied":
                raise Denied(reply.get("reason", "denied"))
            if reply.get("type") != "fragments":
                raise protocol.ProtocolError(f"unexpected reply type {reply.get('type')!r}")

            results = []
            for raw in reply.get("fragments", []):
                frag = MemoryFragment.from_dict(raw)
                if not frag.verify(bytes.fromhex(peer.sign_public_hex)):
                    continue  # drop anything that doesn't verify — never trust unverified content
                results.append(frag)
            return results
        finally:
            sock.close()
