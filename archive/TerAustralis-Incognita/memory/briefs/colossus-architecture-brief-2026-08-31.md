---
layer: working / architecture brief
canon: false
source: Drive "Colossus Architecture Brief 2026-08-31" (id 1M54MvgxmvUciVH2V8VWCj85DL7cEOX-Pi-fWBDlT9MA)
note: Reconstructed from public sources; not an official xAI as-built drawing.
---

# Colossus Architecture Brief
**Export date:** 31 August 2026  
**Source:** Grok conversation with Crystal Arena-Turner  
**Status:** Reconstructed from public xAI pages, ServeTheHome floor tour, NVIDIA Spectrum-X docs, Epoch AI site estimates, and reporting. Not an official xAI as-built drawing.

---

## What Colossus is

xAI’s Memphis-area AI campus. Official framing: a “gigafactory of compute.” First wave: 100,000 Nvidia H100 GPUs in 122 days, doubled to 200,000 GPUs in another 92 days, roadmap toward 1 million GPUs. Official public figures also include multi-petabyte-per-second aggregate memory bandwidth and more than an exabyte of storage.

It is no longer only one hall. Colossus 1 sits in a former Electrolux plant on Paul Lowry Road, South Memphis. Colossus 2 expanded toward Southaven, Mississippi, with extra buildings (including one publicly nicknamed MACROHARDRR) and a gigawatt-class power envelope.

Independent late-August 2026 estimates (Epoch AI) should be treated as reconstructions, not press copy:

- Colossus 1: ~230k GPUs / ~276k H100-equivalents / ~340 MW IT (H100, H200, some B200)
- Colossus 2: ~440k GPUs (B200/B300 mix) / ~1.1 million H100-equivalents / ~946 MW IT, still growing

---

## Two architectures, one campus name

| Layer | Colossus 1 | Colossus 2 |
|---|---|---|
| Dominant silicon | H100, then H200, some GB200 | GB200 / GB300 (B200 / B300 class) |
| Scale-up domain | 8 GPUs (NVLink inside one HGX board) | 72 GPUs (NVL72 NVLink spine in one rack) |
| Scale-out fabric | NVIDIA Spectrum-X Ethernet | Spectrum-X Ethernet |
| Confirmed rack | 8× 4U HGX servers = 64 GPUs/rack | 18 compute trays + 9 NVLink switch trays = 72 GPUs/rack |
| Rack power class | tens of kW liquid racks | ~120–130 kW NVL72 racks |

Colossus 1 is a giant Ethernet mesh of 8-GPU islands. Colossus 2 is a mesh of 72-GPU islands.

---

## Compute hierarchy

```
GPU
  └─ NVLink domain          C1: 8 GPUs / HGX board
                            C2: 72 GPUs / NVL72 rack
       └─ Rack
            └─ Mini-pod     C1 tour: 8 racks = 512 GPUs
                 └─ Hall / building
                      └─ Campus fabric (Spectrum-X)
                           └─ Cross-site power + storage
```

### Colossus 1 rack (ServeTheHome tour)

- Supermicro 4U Universal GPU / HGX H100
- 8 GPUs + dual CPUs per chassis
- 8 chassis + Coolant Distribution Unit + manifolds + top-of-rack = 64 GPUs/rack
- Eight racks grouped as a 512-GPU mini-cluster

### Colossus 2 rack (NVIDIA NVL72 reference)

- 18 liquid-cooled compute trays
- 2 Grace Blackwell Superchips per tray
- 72 Blackwell GPUs + 36 Grace CPUs per rack
- 9 NVLink switch trays form the copper spine
- Scale-up inside the rack is NVLink 5. Ethernet starts when traffic leaves the rack.

---

## Network

Distinctive choice: Spectrum-X Ethernet, not InfiniBand, for the published 100k-GPU fabric.

Confirmed C1 building blocks:

- Spectrum SN5600: 2U, 51.2 Tb/s, 64× 800GbE or 128× 400GbE
- BlueField-3 SuperNIC: one 400GbE path per GPU
- Rail-optimized leaf-spine / CLOS, advertised 1:1 non-blocking
- NVIDIA claim at 100k-GPU scale: ~95% throughput vs ~60% for vanilla Ethernet; no collision-driven application latency loss on a healthy fabric
- Published reference designs top out near 100k GPUs; custom designs claimed toward ~512k. A 1-million-GPU *single* RDMA domain is not a solved public design.

Three networks that must stay separated:

1. Scale-up — NVLink (8-GPU or 72-GPU)
2. Scale-out — Spectrum-X RDMA/RoCE
3. Front-end / storage / out-of-band management

---

## Cooling

Direct-to-chip liquid cooling. Cold plates on GPUs (and typically CPUs/VRMs) → rack CDU → facility chilled water → outdoor air-cooled chillers.

NVL72 racks sit in the ~120 kW class. Lose coolant flow and silicon fails in seconds. Flow and temperature sensors are part of the machine.

---

## Power

```
Grid (TVA / MLGW, initially tiny)
  + on-site / behind-the-meter gas turbines
  + Tesla Megapacks (spike buffer and ride-through)
       → medium-voltage distribution / GIS substation
            → hall switchgear
                 → rack PDUs / NVL72 power shelves
```

Training load is spiky. Megapacks smooth what turbines and the grid see. Colossus 2’s speed came from not waiting for interconnection: portable gas generation in Mississippi, then backfill grid and substations.

Community and legal conflict followed: unpermitted or under-permitted methane turbines, air-quality claims in South Memphis and Southaven, water/aquifer concerns, noise. That constraint is part of the real architecture. Cooling and power that assume infinite clean reject water and instant permits are fiction.

---

## Storage

Official: more than 1 exabyte for training data and checkpoints. At this scale that implies a parallel filesystem or object store, a separate checkpoint plane, and a front-end network that does not share congested rails with AllReduce.

Exact vendor and stripe layout are unpublished.

---

## Software mapping

Grok-class training is a 3D/4D parallel job:

- Tensor / expert parallel wants NVLink (why 8-wide vs 72-wide domains matter)
- Pipeline parallel wants predictable neighbor latency
- Data parallel wants lossless Ethernet under elephant flows
- Later RL / rollout farms want isolation between many smaller jobs

Unpublished: exact PyTorch/JAX/Megatron fork, collective library over RoCE, precision recipe (FP8 / NVFP4), scheduler, and whether C1 and C2 are one RDMA domain.

---

## What is still missing from the public picture

- Exact fat-tree radix and oversubscription per hall
- Whether C1 and C2 can AllReduce as one job
- Filesystem vendor and checkpoint policy
- Failure-domain and RAS design (at this GPU count something is broken every few minutes)
- Split between pretrain, RL rollout, and inference serving
- Precise PUE / WUE
- The 1-million-GPU topology (multiplane Ethernet, multi-building Spectrum-XGS, or several fabrics with DCI)

Novelty is not a secret xAI ASIC. Public evidence is merchant NVIDIA silicon + Spectrum-X + Supermicro / NVL72 racks + behind-the-meter gas and Megapacks. The distinctive move is speed of assembly and refusal to wait for the conventional grid-and-permit calendar.

---

## Test for understanding

Can you draw where a 1-trillion-parameter AllReduce lives at 1 ms, 10 ms, and 100 ms — inside a board, inside a rack, across a hall, across a building — and what breaks at each hop?

If that sketch is fuzzy, the missing piece is the parallel plan plus the failure-domain map, not another GPU SKU list.

---

## Also in the same conversation (not file exports)

- xAI mission: understand the true nature of the universe / accelerate human scientific discovery
- How Grok supports that: truth-seeking design, first-principles reasoning, live tools and X-grounded knowledge, research-assistant role, scaled compute
- No image, song, or story files were written to disk in that thread
