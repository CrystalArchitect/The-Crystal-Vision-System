# Convergence Lens Prototype

Minimal working prototype demonstrating the core operations of Convergence Lens:

- **Classifier**: Separates claims into observation / evidence / interpretation / vision
- **Uncertainty Mapper**: Identifies gaps (knowledge / tech / resource / coordination / trust)
- **Evidence Status**: Records confidence and evidence tier at point-in-time
- **Transcript**: Preserves dialogue exchanges for later review

## Structure

```
convergence_lens/
├── classifier.py          # Statement decomposition
├── uncertainty_mapper.py  # Gap identification
├── evidence_status.py     # Status tracking
├── transcript.py          # Dialogue recording
├── __init__.py
└── README.md
```

## Non-goals

This prototype does NOT:
- Make predictions
- Create consensus
- Replace expert judgment
- Output authoritative conclusions

It decomposes, records, and reflects. That's all.

## Usage

See individual module docstrings for examples.

## Integration path

After validation, this prototype feeds into CrystalCore.OS as:
- MIRROR register (classifier)
- LOOM register (connections)
- CHRONICLE register (transcript)
- CONSTITUTION rules (all layers)

## Beta phase alignment

Depends on:
✓ Clementine (layer separation proven)
✓ RDP (tamper-evident records proven)
✓ Consent Transport (agency proven)
✓ Clementine (dialogue interface proven)

This prototype adds interpretation discipline on top of those layers.
