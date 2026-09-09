# CrystalCore.OS - Full Hugging Face Trainer Integration with Active Learning
# Complete retraining pipeline using Hugging Face Trainer and uncertainty sampling

import json
import logging
from pathlib import Path
from typing import Dict, Optional, List, Tuple

import torch
import torch.nn.functional as F

try:
    from datasets import Dataset
    from transformers import (
        AutoTokenizer,
        AutoModelForSequenceClassification,
        Trainer,
        TrainingArguments,
    )

    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

logger = logging.getLogger(__name__)

# Explicit GoEmotions Label Mapping (28 classes)
EMOTION_LABEL_MAP = {
    0: "admiration",
    1: "amusement",
    2: "anger",
    3: "annoyance",
    4: "approval",
    5: "caring",
    6: "confusion",
    7: "curiosity",
    8: "desire",
    9: "disappointment",
    10: "disapproval",
    11: "disgust",
    12: "embarrassment",
    13: "excitement",
    14: "fear",
    15: "gratitude",
    16: "grief",
    17: "joy",
    18: "love",
    19: "nervousness",
    20: "optimism",
    21: "pride",
    22: "realization",
    23: "relief",
    24: "remorse",
    25: "sadness",
    26: "surprise",
    27: "neutral",
}

# Reverse mapping for easy lookup
EMOTION_LABEL_MAP_REV = {v: k for k, v in EMOTION_LABEL_MAP.items()}


class CrystalCoreEI:
    """Full Emotional Intelligence system with Hugging Face Transformers."""

    def __init__(self, model_dir: str = "./crystalcore_emotion_model"):
        if not HAS_TRANSFORMERS:
            raise ImportError("Please install transformers: pip install transformers torch")

        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)

        try:
            self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            self.model = AutoModelForSequenceClassification.from_pretrained(
                str(self.model_dir), num_labels=28
            )
        except Exception as e:
            logger.warning(f"Model not found. Using fresh DistilBERT: {e}")
            self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            self.model = AutoModelForSequenceClassification.from_pretrained(
                "distilbert-base-uncased", num_labels=28
            )

        self.queue_file = Path.home() / ".crystalcore" / "active_learning_queue.jsonl"
        self.queue_file.parent.mkdir(parents=True, exist_ok=True)

    def detect_emotion(self, text: str) -> Dict:
        """
        Detect emotion from text using transformer model.
        Returns emotion label, confidence, and logits.
        """
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128,
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = F.softmax(logits, dim=1)

        top_prob, top_idx = torch.max(probs, dim=1)
        confidence = top_prob.item()
        emotion_idx = top_idx.item()
        emotion_label = EMOTION_LABEL_MAP.get(emotion_idx, "neutral")

        return {
            "emotion": emotion_label,
            "emotion_idx": emotion_idx,
            "confidence": round(confidence, 4),
            "logits": logits,
            "probs": probs,
        }

    def uncertainty_score(
        self, logits: torch.Tensor, strategy: str = "entropy"
    ) -> torch.Tensor:
        """
        Calculate uncertainty score for active learning.
        Strategies: least_confidence, entropy, margin
        """
        probs = F.softmax(logits, dim=1)

        if strategy == "least_confidence":
            return 1 - torch.max(probs, dim=1)[0]

        elif strategy == "entropy":
            # Shannon entropy: -sum(p * log(p))
            entropy = -torch.sum(probs * torch.log(probs + 1e-9), dim=1)
            return entropy

        elif strategy == "margin":
            # Margin between top 2 predictions
            top_2_probs, _ = torch.topk(probs, 2, dim=1)
            return 1 - (top_2_probs[:, 0] - top_2_probs[:, 1])

        else:
            return 1 - torch.max(probs, dim=1)[0]

    def should_query_user(
        self,
        confidence: float,
        uncertainty: float,
        confidence_threshold: float = 0.65,
        uncertainty_threshold: float = 0.55,
    ) -> bool:
        """Hybrid uncertainty sampling: trigger if either threshold exceeded."""
        return confidence < confidence_threshold or uncertainty > uncertainty_threshold

    def add_to_queue(self, text: str, emotion: str, confidence: float) -> None:
        """Add low-confidence prediction to active learning queue."""
        entry = {
            "text": text,
            "predicted_emotion": emotion,
            "confidence": confidence,
            "user_label": None,
            "timestamp": __import__("datetime").datetime.now().isoformat(),
        }
        try:
            with open(self.queue_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
            logger.info(f"Added to queue: '{text[:30]}...' ({emotion}, {confidence:.2%})")
        except Exception as e:
            logger.error(f"Failed to add to queue: {e}")

    def load_queue(self) -> List[Dict]:
        """Load active learning queue from disk."""
        if not self.queue_file.exists():
            return []
        try:
            with open(self.queue_file, "r") as f:
                return [json.loads(line) for line in f if line.strip()]
        except Exception as e:
            logger.error(f"Failed to load queue: {e}")
            return []

    def get_labeled_samples(self) -> List[Dict]:
        """Get samples that have been labeled by users."""
        queue = self.load_queue()
        return [item for item in queue if item.get("user_label") is not None]

    def prepare_training_data(self, min_samples: int = 8):
        """
        Prepare labeled data for retraining.
        Returns tokenized Dataset if enough labeled samples exist, else None.
        """
        labeled = self.get_labeled_samples()

        if len(labeled) < min_samples:
            logger.warning(
                f"Only {len(labeled)} labeled samples. Need at least {min_samples} for retraining."
            )
            return None

        texts = [item["text"] for item in labeled]
        labels = [
            EMOTION_LABEL_MAP_REV.get(item["user_label"], 27) for item in labeled
        ]

        dataset = Dataset.from_dict({"text": texts, "label": labels})

        def tokenize_fn(examples):
            return self.tokenizer(
                examples["text"],
                padding="max_length",
                truncation=True,
                max_length=128,
            )

        tokenized = dataset.map(tokenize_fn, batched=True)
        tokenized.set_format("torch", columns=["input_ids", "attention_mask", "label"])

        logger.info(f"Prepared {len(labeled)} labeled samples for training")
        return tokenized

    def retrain(self, min_samples: int = 8, epochs: int = 2) -> bool:
        """
        Fine-tune model on labeled data using Hugging Face Trainer.
        Returns True if retraining succeeded, False otherwise.
        """
        if not HAS_TRANSFORMERS:
            logger.error("Transformers not installed. Cannot retrain.")
            return False

        train_dataset = self.prepare_training_data(min_samples=min_samples)
        if train_dataset is None:
            return False

        retrained_dir = self.model_dir / "retrained"
        retrained_dir.mkdir(parents=True, exist_ok=True)

        training_args = TrainingArguments(
            output_dir=str(retrained_dir),
            num_train_epochs=epochs,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            evaluation_strategy="no",
            save_strategy="epoch",
            learning_rate=3e-5,
            weight_decay=0.01,
            report_to="none",
            logging_steps=10,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
        )

        logger.info("🚀 Starting model retraining on user-labeled data...")
        try:
            trainer.train()

            # Save updated model
            self.model.save_pretrained(str(self.model_dir))
            self.tokenizer.save_pretrained(str(self.model_dir))

            logger.info(f"✅ Retraining complete. Model saved to {self.model_dir}")
            return True

        except Exception as e:
            logger.error(f"Retraining failed: {e}")
            return False


def process_message_with_active_learning(
    text: str, ei_system: CrystalCoreEI
) -> Tuple[str, bool]:
    """
    Process user message with emotion detection and active learning.
    Returns: (response, triggered_active_learning)
    """
    result = ei_system.detect_emotion(text)

    # Calculate uncertainty (hybrid strategy)
    uncertainty = ei_system.uncertainty_score(result["logits"], strategy="entropy")
    uncertainty_val = uncertainty.mean().item()

    # Check if we should query user
    should_query = ei_system.should_query_user(
        result["confidence"], uncertainty_val, confidence_threshold=0.65, uncertainty_threshold=0.55
    )

    base_response = f"Detected emotion: {result['emotion']} ({result['confidence']:.0%})"

    if should_query:
        ei_system.add_to_queue(text, result["emotion"], result["confidence"])
        clarification = (
            f"To help me learn better: You seem {result['emotion']}. "
            f"Is that accurate, or how would you describe it?"
        )
        return base_response + "\n\n" + clarification, True

    return base_response, False
