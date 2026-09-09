# Mesh transport stub (libp2p-shaped)

In-process peer fabric for Crystal Core **Phase 1**. Same API surface we expect from a future rust-libp2p / js-libp2p host — **no real multiaddrs on the wire**.

## Status

| Item | State |
|------|--------|
| In-process dial / publish | yes |
| gossipsub / noise / yamux | planned |
| Bootstrap + mDNS | planned |
| Mainnet mesh | HOLD |

## Quick use

```python
from node.mesh import MeshStub

mesh = MeshStub(region="budapest-starline")
hub = mesh.spawn(did="did:crystal:hub-bud")
edge = mesh.spawn(did="did:crystal:edge-vie")
mesh.dial(hub.peer_id, edge.peer_id)

received = []
edge.on(MeshStub.PROTOCOL_MANIFEST, lambda src, msg: received.append((src, msg)))
mesh.publish(hub.peer_id, MeshStub.PROTOCOL_MANIFEST, {"epoch": "sister-2-danube-gate"})
assert received
print(mesh.snapshot())
```

## Protocols (v0.5 draft)

| Protocol | Payload |
|----------|---------|
| `/crystal/manifest/1.0.0` | Node manifest + stake summary |
| `/crystal/receipt/1.0.0` | ServiceReceipt envelope (hash + dual attest refs) |
| `/crystal/twin-delta/1.0.0` | Twin layer CRDT delta |

## Tests

```powershell
python -m pytest tests/test_mesh_stub.py -q
```

## Next (real libp2p)

1. Swap `MeshStub` for adapter implementing `spawn` / `dial` / `publish` / `on`
2. Pin bootstrap multiaddrs in `deploy/regions/*/values.yaml`
3. Fail-closed: unknown protocol → drop + audit line
