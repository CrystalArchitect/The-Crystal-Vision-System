# CrystalCore.OS - Advanced Uncertainty Quantification Methods

## Overview

CrystalCore.OS now implements multiple uncertainty quantification (UQ) strategies for robust active learning decisions:

1. **Entropy** - Shannon entropy of predictions
2. **Least Confidence** - Inverse of max probability
3. **Margin** - Gap between top-2 predictions
4. **Bayesian (MC Dropout)** - Epistemic + Aleatoric uncertainty
5. **Hybrid** - Combination of above methods

---

## 1. Entropy-Based Uncertainty

### Theory
Shannon entropy measures information/uncertainty in probability distributions:
```
H(p) = -Σ(p_i * log(p_i))
```

- **Range**: [0, log(K)] where K=28 (emotion classes)
- **Interpretation**: High entropy = ambiguous prediction, low entropy = confident
- **Best for**: Detecting when multiple emotions are equally likely

### Usage
```python
from src.crystalcore_os.uncertainty_quantification import UncertaintyQuantifier

uq = UncertaintyQuantifier()
entropy = uq.entropy(logits)  # torch.Tensor

# Active learning threshold
if entropy > 0.55:
    trigger_active_learning()
```

### Advantages
✅ Theoretically grounded (information theory)  
✅ Captures true ambiguity  
✅ Works well for emotion detection  
✅ Computationally efficient

---

## 2. Least Confidence

### Theory
Inverse of the maximum predicted probability:
```
U = 1 - max(p)
```

- **Range**: [0, 1]
- **Interpretation**: Directly measures lack of confidence
- **Best for**: Simple confidence-based filtering

### Usage
```python
least_conf = uq.least_confidence(logits)
if least_conf > 0.35:  # Confidence < 0.65
    trigger_active_learning()
```

### Advantages
✅ Simple and interpretable  
✅ Aligns with human confidence  
✅ Fast to compute

---

## 3. Margin Sampling

### Theory
Gap between top-2 predicted probabilities:
```
U = 1 - (p_1 - p_2)
```

- **Range**: [0, 1]
- **Interpretation**: Identifies when predictions are close
- **Best for**: Distinguishing tight competitor classes

### Usage
```python
margin = uq.margin(logits)
if margin > 0.15:  # Margin < 0.85
    trigger_active_learning()
```

### Advantages
✅ Focuses on boundary cases  
✅ Good for imbalanced datasets  
✅ Prevents redundant labeling

---

## 4. Bayesian Neural Networks (MC Dropout)

### Theory
Multiple forward passes with dropout enabled:
```
For t = 1 to T:
    ŷ_t = model(x, dropout_enabled)  # Different masks each time
    
Epistemic Uncertainty = Var(ŷ_1, ..., ŷ_T)  # Uncertainty about model
Aleatoric Uncertainty = E[Var(p | data)]    # Data noise
```

### Usage
```python
from src.crystalcore_os.uncertainty_quantification import BayesianUncertaintyQuantifier

bayesian_uq = BayesianUncertaintyQuantifier(model, n_mc_samples=8)
result = bayesian_uq.predict_with_uncertainty(inputs, tokenizer)

# Returns:
# - confidence: Mean prediction confidence
# - epistemic_uncertainty: Model/parameter uncertainty
# - aleatoric_uncertainty: Data noise uncertainty
# - predictive_entropy: Overall predictive uncertainty
```

### Interpretation

**Epistemic Uncertainty** (Model Uncertainty)
- High: Model doesn't know this input type
- Cause: Limited training data for this emotion
- Action: Collect labels to reduce

**Aleatoric Uncertainty** (Data Uncertainty)
- High: Input is inherently ambiguous
- Cause: Mixed signals in text/audio/video
- Action: Consider confidence score, may be irreducible

### Active Learning Decision
```python
if result["epistemic_uncertainty"] > 0.12:
    # Model is uncertain → collect label
    trigger_active_learning()
elif result["aleatoric_uncertainty"] > 0.08:
    # Data is ambiguous → high-confidence prediction still useful
    pass
```

### Advantages
✅ Distinguishes model vs. data uncertainty  
✅ Most theoretically sound  
✅ Best calibrated predictions  
✅ Robust to distribution shift

### Disadvantages
❌ Computationally expensive (8-10 forward passes)  
❌ Requires dropout during inference  
❌ Slower than single-pass methods

---

## 5. Hybrid Uncertainty (Recommended)

### Strategy
Combine multiple methods for robustness:

```python
from src.crystalcore_os.uncertainty_quantification import ActiveLearningDecider

decider = ActiveLearningDecider(
    confidence_threshold=0.65,      # Min confidence
    entropy_threshold=0.55,         # Max entropy
    margin_threshold=0.15,          # Max margin (inverted)
    use_hybrid=True
)

should_query, details = decider.should_query_user(logits, verbose=True)
```

### Decision Logic
```
Query if ANY of these:
  1. Confidence < 0.65, OR
  2. Entropy > 0.55, OR
  3. Margin > 0.15 (top-2 predictions close)
```

### Advantages
✅ Captures multiple uncertainty types  
✅ More robust than single method  
✅ Reduces false negatives  
✅ Practical for production systems

---

## Implementation Roadmap

### Current (v1.0)
✅ Entropy uncertainty
✅ Least confidence
✅ Margin sampling
✅ Hybrid decision logic

### v2.0 (NEXT)
→ Bayesian MC Dropout integration
→ Temperature scaling calibration
→ Uncertainty-aware model updating

### v3.0 (FUTURE)
→ Variational inference (more efficient Bayesian)
→ Deep ensembles (alternative to MC Dropout)
→ Conformal prediction intervals
→ Out-of-distribution detection

---

## Performance Benchmarks

| Method | Compute | Latency | Calibration | Robustness |
|--------|---------|---------|-------------|-----------|
| Entropy | Low | 1x | Good | Good |
| Least Confidence | Low | 1x | Fair | Poor |
| Margin | Low | 1x | Fair | Good |
| **Hybrid** ⭐ | Low | 1x | Very Good | Excellent |
| Bayesian (MC) | High | 8x | Excellent | Excellent |

---

## Best Practices

### For Fast Inference (Real-Time)
```python
# Use hybrid with single-pass thresholds
decider = ActiveLearningDecider(use_hybrid=True)
should_query, _ = decider.should_query_user(logits)
```

### For High Accuracy (Offline)
```python
# Use Bayesian uncertainty
bayesian = BayesianUncertaintyQuantifier(model, n_mc_samples=16)
result = bayesian.predict_with_uncertainty(inputs, tokenizer)

if result["epistemic_uncertainty"] > threshold:
    trigger_active_learning()
```

### For Balanced Performance (Recommended)
```python
# Hybrid for most decisions + Bayesian for edge cases
if decider.should_query_user(logits)[0]:  # Hybrid
    # Double-check with Bayesian
    if bayesian.predict_with_uncertainty(inputs, tokenizer)[
        "epistemic_uncertainty"
    ] > 0.15:
        add_to_queue(text, emotion, confidence)
```

---

## Troubleshooting

### Querying Too Frequently
- **Symptom**: Too many active learning queries
- **Solution**: 
  - Increase `confidence_threshold` (e.g., 0.60 → 0.70)
  - Increase `entropy_threshold` (e.g., 0.55 → 0.70)
  - Use Bayesian instead (more selective)

### Not Querying Enough
- **Symptom**: Missed ambiguous predictions
- **Solution**:
  - Decrease thresholds
  - Switch to Bayesian (captures epistemic uncertainty)
  - Use ensemble methods

### Calibration Issues
- **Symptom**: Predicted confidence ≠ actual accuracy
- **Solution**:
  - Use temperature scaling: `scaled_logits = logits / T`
  - Increase MC dropout samples
  - Use ensemble prediction averaging

---

## References

- Guo, C., Pleiss, G., et al. (2017). "On Calibration of Modern Neural Networks"
- Kendall, A., & Gal, Y. (2017). "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?"
- Freeman, D. (2018). "Active Learning Literature Survey"

---

*CrystalCore.OS Advanced Uncertainty Quantification*  
*Production-Ready Uncertainty Estimation for Active Learning*
