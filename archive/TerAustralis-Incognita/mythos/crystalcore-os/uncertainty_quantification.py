# CrystalCore.OS - Uncertainty Quantification Methods
# Multiple strategies for estimating prediction uncertainty and active learning decisions

import logging
from typing import Dict, Literal, Optional, Tuple

import torch
import torch.nn.functional as F

logger = logging.getLogger(__name__)


class UncertaintyQuantifier:
    """Multiple uncertainty quantification methods for emotion detection."""

    def __init__(self):
        """Initialize uncertainty quantifier."""
        logger.info("UncertaintyQuantifier initialized")

    def entropy(self, logits: torch.Tensor) -> torch.Tensor:
        """
        Shannon Entropy - measures predictive uncertainty.
        H(p) = -sum(p * log(p))
        - Range: [0, log(K)] where K is number of classes
        - High entropy → ambiguous/uncertain prediction
        - Low entropy → confident prediction
        """
        probs = F.softmax(logits, dim=-1)
        entropy = -torch.sum(probs * torch.log(probs + 1e-9), dim=-1)
        return entropy

    def least_confidence(self, logits: torch.Tensor) -> torch.Tensor:
        """
        Least Confidence - inverted max probability.
        U = 1 - max(p)
        - Range: [0, 1]
        - High uncertainty when model is not confident
        """
        probs = F.softmax(logits, dim=-1)
        return 1 - torch.max(probs, dim=-1)[0]

    def margin(self, logits: torch.Tensor) -> torch.Tensor:
        """
        Margin Sampling - gap between top 2 predictions.
        U = 1 - (p_max - p_2nd)
        - Range: [0, 1]
        - High uncertainty when top two predictions are close
        """
        probs = F.softmax(logits, dim=-1)
        sorted_probs, _ = torch.sort(probs, descending=True, dim=-1)
        margin = sorted_probs[:, 0] - sorted_probs[:, 1]
        return 1 - margin

    def max_probability(self, logits: torch.Tensor) -> torch.Tensor:
        """
        Max Probability - confidence of top prediction.
        C = max(p)
        - Range: [0, 1]
        - Returns confidence (NOT uncertainty)
        """
        probs = F.softmax(logits, dim=-1)
        return torch.max(probs, dim=-1)[0]

    def variance(
        self, logits: torch.Tensor, samples: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        """
        Predictive Variance - std of predictions.
        Used when predictions come from MC Dropout or ensemble.
        - Approximates epistemic uncertainty
        """
        if samples is None:
            logger.warning("Variance requires multiple samples (MC Dropout)")
            return self.entropy(logits)

        # samples shape: [num_samples, batch_size, num_classes]
        probs = F.softmax(samples, dim=-1)
        variance = torch.var(probs, dim=0)  # Variance across samples
        return variance.mean(dim=-1)  # Average across classes

    def combined_uncertainty(
        self,
        logits: torch.Tensor,
        method: Literal["entropy", "least_confidence", "margin", "hybrid"] = "entropy",
        temperature: float = 1.0,
    ) -> torch.Tensor:
        """
        Combined uncertainty with temperature scaling.
        Temperature scales softmax before uncertainty calculation.
        - T > 1: softens predictions (increases uncertainty)
        - T = 1: no scaling (default)
        - T < 1: sharpens predictions (decreases uncertainty)
        """
        scaled_logits = logits / temperature if temperature != 1.0 else logits

        if method == "entropy":
            return self.entropy(scaled_logits)
        elif method == "least_confidence":
            return self.least_confidence(scaled_logits)
        elif method == "margin":
            return self.margin(scaled_logits)
        elif method == "hybrid":
            # Combine entropy + margin
            e = self.entropy(scaled_logits)
            m = self.margin(scaled_logits)
            return 0.7 * e / e.max() + 0.3 * m  # Weighted combination
        else:
            return self.entropy(scaled_logits)

    def get_top_k_uncertain(
        self,
        logits: torch.Tensor,
        k: int = 5,
        method: str = "entropy",
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get top K most uncertain predictions (for active learning).

        Args:
            logits: Model output logits
            k: Number of top uncertain samples to return
            method: Uncertainty method to use

        Returns:
            uncertainty_scores, indices
        """
        uncertainty = self.combined_uncertainty(logits, method=method)
        top_uncertain, indices = torch.topk(uncertainty, min(k, len(uncertainty)))
        return top_uncertain, indices


class ActiveLearningDecider:
    """Decide whether to trigger active learning based on uncertainty."""

    def __init__(
        self,
        confidence_threshold: float = 0.65,
        entropy_threshold: float = 0.55,
        margin_threshold: float = 0.15,
        use_hybrid: bool = True,
    ):
        """
        Initialize active learning decision maker.

        Args:
            confidence_threshold: Min confidence to avoid querying
            entropy_threshold: Max entropy to avoid querying
            margin_threshold: Min margin between top 2 to avoid querying
            use_hybrid: Use combination of thresholds
        """
        self.confidence_threshold = confidence_threshold
        self.entropy_threshold = entropy_threshold
        self.margin_threshold = margin_threshold
        self.use_hybrid = use_hybrid
        self.uq = UncertaintyQuantifier()

    def should_query_user(
        self,
        logits: torch.Tensor,
        confidence: Optional[float] = None,
        verbose: bool = False,
    ) -> Tuple[bool, Dict]:
        """
        Decide whether to query user for label.

        Args:
            logits: Model output logits
            confidence: Precomputed confidence (optional)
            verbose: Return detailed reasoning

        Returns:
            (should_query, details_dict)
        """
        # Calculate uncertainties
        entropy = self.uq.entropy(logits).item()
        least_conf = self.uq.least_confidence(logits).item()
        margin = self.uq.margin(logits).item()
        max_prob = self.uq.max_probability(logits).item()

        details = {
            "confidence": max_prob,
            "entropy": entropy,
            "least_confidence": least_conf,
            "margin": margin,
            "reasons": [],
        }

        should_query = False

        # Check thresholds
        if max_prob < self.confidence_threshold:
            should_query = True
            details["reasons"].append(f"Confidence {max_prob:.3f} < {self.confidence_threshold}")

        if entropy > self.entropy_threshold:
            should_query = True
            details["reasons"].append(f"Entropy {entropy:.3f} > {self.entropy_threshold}")

        if margin > (1 - self.margin_threshold):  # Normalize margin to [0, 1]
            should_query = True
            details["reasons"].append(
                f"Margin {margin:.3f} > {(1 - self.margin_threshold):.3f}"
            )

        if verbose:
            logger.info(f"Active Learning Decision: {should_query}, Details: {details}")

        return should_query, details


class BayesianUncertaintyQuantifier:
    """Bayesian uncertainty via Monte Carlo Dropout."""

    def __init__(self, model, n_mc_samples: int = 8):
        """
        Initialize Bayesian UQ with MC Dropout.

        Args:
            model: PyTorch model with dropout layers
            n_mc_samples: Number of forward passes with dropout enabled
        """
        self.model = model
        self.n_mc_samples = n_mc_samples
        logger.info(f"BayesianUQ initialized with {n_mc_samples} MC samples")

    def predict_with_uncertainty(
        self, inputs: Dict, tokenizer
    ) -> Dict:
        """
        Get predictions with Bayesian uncertainty estimates.

        Args:
            inputs: Tokenized text inputs
            tokenizer: Tokenizer for text encoding

        Returns:
            Dictionary with mean predictions and uncertainty
        """
        self.model.train()  # Enable dropout

        predictions = []

        with torch.no_grad():
            for _ in range(self.n_mc_samples):
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = F.softmax(logits, dim=-1)
                predictions.append(probs)

        # Stack predictions: [n_mc_samples, batch_size, num_classes]
        predictions_tensor = torch.stack(predictions)

        # Mean and variance
        mean_probs = predictions_tensor.mean(dim=0)  # [batch_size, num_classes]
        epistemic_unc = predictions_tensor.var(dim=0).mean(dim=-1)  # Epistemic uncertainty
        aleatoric_unc = (
            (1 - predictions_tensor).var(dim=0).mean(dim=-1)
        )  # Aleatoric uncertainty
        predictive_entropy = -torch.sum(
            mean_probs * torch.log(mean_probs + 1e-9), dim=-1
        )

        top_prob, top_idx = torch.max(mean_probs, dim=-1)

        return {
            "emotion_idx": top_idx.item(),
            "confidence": round(top_prob.item(), 4),
            "epistemic_uncertainty": round(epistemic_unc.item(), 4),
            "aleatoric_uncertainty": round(aleatoric_unc.item(), 4),
            "predictive_entropy": round(predictive_entropy.item(), 4),
            "n_samples": self.n_mc_samples,
            "mean_probs": mean_probs,
            "predictions_samples": predictions_tensor,
        }

    def enable_mc_dropout(self):
        """Enable dropout during inference for Bayesian approximation."""
        self.model.train()

    def disable_mc_dropout(self):
        """Disable dropout for standard inference."""
        self.model.eval()


def print_uncertainty_guide() -> str:
    """Print guide for uncertainty quantification methods."""
    return """
╔═══════════════════════════════════════════════════════════════════╗
║           Uncertainty Quantification Methods Guide                ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║ 1. ENTROPY (Shannon) - Best for Emotion Detection                ║
║    Formula: H(p) = -Σ(p·log(p))                                  ║
║    Range: [0, log(28)]                                           ║
║    Best for: Detecting ambiguous emotions                        ║
║    Threshold: > 0.55 suggests active learning                    ║
║                                                                   ║
║ 2. LEAST CONFIDENCE                                              ║
║    Formula: U = 1 - max(p)                                       ║
║    Range: [0, 1]                                                 ║
║    Best for: Overall confidence-based filtering                  ║
║    Threshold: < 0.65 suggests active learning                    ║
║                                                                   ║
║ 3. MARGIN SAMPLING                                               ║
║    Formula: U = 1 - (p₁ - p₂)                                    ║
║    Range: [0, 1]                                                 ║
║    Best for: Distinguishing close competitors                    ║
║    Threshold: > 0.15 suggests active learning                    ║
║                                                                   ║
║ 4. BAYESIAN (MC DROPOUT) - Most Robust                           ║
║    Multiple forward passes with dropout enabled                  ║
║    Estimates:                                                    ║
║    - Epistemic uncertainty (model uncertainty)                   ║
║    - Aleatoric uncertainty (data uncertainty)                    ║
║    - Predictive entropy                                          ║
║    Threshold: epistemic > 0.12 suggests active learning          ║
║                                                                   ║
║ 5. HYBRID (Recommended for Production)                           ║
║    Combine: Entropy + Least Confidence + Margin                  ║
║    Decision: Query if ANY exceeds threshold                      ║
║    Most robust against adversarial examples                      ║
║                                                                   ║
╠═══════════════════════════════════════════════════════════════════╣
║ Uncertainty × Active Learning Integration                        ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║ High Confidence (> 0.75)                                         ║
║ └─→ Return response (no query)                                   ║
║                                                                   ║
║ Medium Confidence (0.65-0.75)                                    ║
║ └─→ Check entropy/margin                                         ║
║     ├─→ Ambiguous (high entropy) → Query                         ║
║     └─→ Clear (low entropy) → Return response                    ║
║                                                                   ║
║ Low Confidence (< 0.65)                                          ║
║ └─→ Always query + add to active learning queue                  ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
