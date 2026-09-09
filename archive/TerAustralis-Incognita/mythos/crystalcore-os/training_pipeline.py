# CrystalCore.OS - Emotion Recognition Training Pipeline
# Uses Hugging Face + GoEmotions dataset for fine-tuning transformer models

import json
import logging
from pathlib import Path
from typing import Dict, Optional

try:
    import torch
    from transformers import (
        AutoTokenizer,
        AutoModelForSequenceClassification,
        Trainer,
        TrainingArguments,
    )
    from datasets import load_dataset

    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    logging.warning(
        "Transformers/PyTorch not installed. Install with: pip install transformers torch datasets"
    )

logger = logging.getLogger(__name__)

GOEMOTIONS_EMOTIONS = [
    "admiration",
    "amusement",
    "anger",
    "annoyance",
    "approval",
    "caring",
    "confusion",
    "curiosity",
    "desire",
    "disappointment",
    "disapproval",
    "disgust",
    "embarrassment",
    "excitement",
    "fear",
    "gratitude",
    "grief",
    "joy",
    "love",
    "nervousness",
    "neutral",
    "optimism",
    "pride",
    "realization",
    "relief",
    "remorse",
    "sadness",
    "surprise",
]


class EmotionModelTrainer:
    """Train emotion recognition models using GoEmotions dataset."""

    def __init__(
        self,
        model_name: str = "distilbert-base-uncased",
        output_dir: str = "./crystalcore_emotion_model",
    ):
        if not HAS_TRANSFORMERS:
            raise ImportError("Please install transformers: pip install transformers torch")

        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=len(GOEMOTIONS_EMOTIONS)
        )

    def load_dataset(self, dataset_name: str = "go_emotions", split: str = "simplified"):
        """Load GoEmotions dataset from Hugging Face."""
        logger.info(f"Loading {dataset_name} dataset ({split} split)...")
        return load_dataset(dataset_name, split)

    def tokenize_function(self, examples):
        """Tokenize text for transformer input."""
        return self.tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=128,
        )

    def train(
        self,
        train_dataset,
        eval_dataset,
        epochs: int = 3,
        batch_size: int = 16,
        learning_rate: float = 2e-5,
    ):
        """Train the emotion recognition model."""
        logger.info("Tokenizing datasets...")
        tokenized_train = train_dataset.map(self.tokenize_function, batched=True)
        tokenized_eval = eval_dataset.map(self.tokenize_function, batched=True)

        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            evaluation_strategy="epoch",
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=epochs,
            weight_decay=0.01,
            save_strategy="epoch",
            load_best_model_at_end=True,
            report_to="none",
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_train,
            eval_dataset=tokenized_eval,
        )

        logger.info("Starting training...")
        trainer.train()

        self.save_model()
        logger.info(f"Training complete. Model saved to {self.output_dir}")

    def save_model(self):
        """Save trained model and tokenizer."""
        self.model.save_pretrained(str(self.output_dir))
        self.tokenizer.save_pretrained(str(self.output_dir))


def train_crystalcore_emotion_model():
    """Complete training pipeline for CrystalCore.OS."""
    if not HAS_TRANSFORMERS:
        print("⚠️  Transformers not installed. Skipping model training.")
        print("Install with: pip install transformers torch datasets")
        return False

    try:
        trainer = EmotionModelTrainer()
        dataset = trainer.load_dataset()

        # Split dataset
        split_data = dataset["train"].train_test_split(test_size=0.2)
        train_dataset = split_data["train"]
        eval_dataset = split_data["test"]

        trainer.train(
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            epochs=3,
            batch_size=16,
        )

        print("✅ Training complete. Model ready for CrystalCore.OS")
        return True

    except Exception as e:
        logger.error(f"Training failed: {e}")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train_crystalcore_emotion_model()
