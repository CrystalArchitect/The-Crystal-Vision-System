"""Mesh transport stub tests."""

from node.mesh import MeshStub


def test_dial_and_publish_manifest():
    mesh = MeshStub()
    a = mesh.spawn(did="did:crystal:a")
    b = mesh.spawn(did="did:crystal:b")
    assert mesh.dial(a.peer_id, b.peer_id)

    got = []
    b.on(MeshStub.PROTOCOL_MANIFEST, lambda src, msg: got.append((src, msg)))
    n = mesh.publish(
        a.peer_id,
        MeshStub.PROTOCOL_MANIFEST,
        {"epoch": "sister-2-danube-gate", "region": "budapest-starline"},
    )
    assert n == 1
    assert len(got) == 1
    assert got[0][0] == a.peer_id
    assert got[0][1]["epoch"] == "sister-2-danube-gate"


def test_broadcast_reaches_all():
    mesh = MeshStub()
    hub = mesh.spawn()
    edges = [mesh.spawn() for _ in range(3)]
    for e in edges:
        mesh.dial(hub.peer_id, e.peer_id)

    boxes = []
    for e in edges:
        e.on(MeshStub.PROTOCOL_TWIN, lambda src, msg, box=boxes: box.append(msg))

    n = mesh.broadcast(hub.peer_id, MeshStub.PROTOCOL_TWIN, {"layer": "energy", "delta": 1.2})
    assert n == 3
    assert len(boxes) == 3


def test_snapshot_hold():
    mesh = MeshStub(region="budapest-starline")
    mesh.spawn()
    snap = mesh.snapshot()
    assert snap["authority"] == "HOLD"
    assert snap["transport"] == "in-process-stub"
    assert snap["peer_count"] == 1
