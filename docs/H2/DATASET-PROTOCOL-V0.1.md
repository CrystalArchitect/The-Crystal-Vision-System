# CrystalCore H2 — Dataset & Question Protocol V0.1

## Dataset

Procedurally generated synthetic long-context retrieval data. Each document contains controlled evidence items, distractors (including semantically similar), independently generated entities, and experimenter-controlled evidence locations. No reliance on external memorised knowledge. Final evaluation corpus generated from fixed, pre-registered seeds.

## Evidence-distance buckets

* Local: <8k
* Near: 8–32k
* Medium: 32–128k
* Long: 128–256k
* Very long: 256–512k
* Extreme: 512k–1M

## Question classes (all retained)

1. Single distant-fact retrieval
2. Two-source retrieval
3. Cross-context composition
4. Distractor discrimination
5. Position-balanced retrieval

## Sample size

1000 primary questions per context length (6000 total per condition). 1M evaluation has its own immutable final-test subset.

## Partitions

* Development
* Validation
* Final (independent seed family, untouched until experiment complete)

## Statistical Gate

At 1M tokens the lower confidence bound of the quality ratio must be ≥ 0.90 AND bandwidth ratio ≤ 0.40.
