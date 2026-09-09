# CrystalCore.OS - Active Learning Loop & Queue Management
# Improves emotion detection accuracy through user feedback and periodic retraining

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

LOW_CONFIDENCE_THRESHOLD = 0.65
MIN_SAMPLES_FOR_RETRAIN = 10


class ActiveLearningQueue:
    """Manages the active learning queue for continuous model improvement."""

    def __init__(self, filename: Optional[str] = None):
        # Home-anchored like STATE_PATH and EI_STATE_PATH, so all three
        # saves live in ~/.crystalcore/ no matter where the terminal is
        # launched from — never in a working tree.
        if filename is None:
            self.filename = Path.home() / ".crystalcore" / "active_learning_queue.jsonl"
        else:
            self.filename = Path(filename)
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        self.queue: List[Dict] = []
        self.load_queue()

    def load_queue(self):
        """Load existing queue from disk."""
        if self.filename.exists():
            try:
                with open(self.filename, "r") as f:
                    self.queue = [json.loads(line) for line in f if line.strip()]
                logger.info(f"Loaded {len(self.queue)} entries from active learning queue")
            except Exception as e:
                logger.error(f"Failed to load queue: {e}")
                self.queue = []
        else:
            self.queue = []

    def add_sample(
        self,
        text: str,
        predicted_emotion: str,
        confidence: float,
        user_label: Optional[str] = None,
        user_id: str = "default",
    ) -> None:
        """Add a sample to the learning queue (for retraining later)."""
        entry = {
            "text": text,
            "predicted_emotion": predicted_emotion,
            "confidence": round(confidence, 4),
            "user_label": user_label,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
        }
        self.queue.append(entry)

        # Persist to disk
        try:
            with open(self.filename, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to persist queue entry: {e}")

    def get_pending(self) -> List[Dict]:
        """Get samples awaiting user labels."""
        return [item for item in self.queue if item.get("user_label") is None]

    def get_labeled(self) -> List[Dict]:
        """Get samples that have been labeled by users."""
        return [item for item in self.queue if item.get("user_label") is not None]

    def mark_labeled(self, text: str, user_label: str) -> bool:
        """Mark a sample as labeled by the user."""
        for entry in self.queue:
            if entry["text"] == text and entry.get("user_label") is None:
                entry["user_label"] = user_label
                entry["label_timestamp"] = datetime.now().isoformat()

                # Update disk
                self._rewrite_queue()
                logger.info(f"Marked '{text[:50]}...' as {user_label}")
                return True
        return False

    def _rewrite_queue(self) -> None:
        """Rewrite entire queue to disk (after updates)."""
        try:
            with open(self.filename, "w") as f:
                for entry in self.queue:
                    f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to rewrite queue: {e}")

    def get_status(self) -> Dict:
        """Get queue statistics."""
        pending = self.get_pending()
        labeled = self.get_labeled()
        return {
            "pending": len(pending),
            "labeled": len(labeled),
            "total": len(self.queue),
            "ready_for_retrain": len(labeled) >= MIN_SAMPLES_FOR_RETRAIN,
        }

    def export_for_training(self) -> List[Dict]:
        """Export labeled samples for model retraining."""
        return self.get_labeled()

    def clear_after_retrain(self) -> None:
        """Clear queue after successful retraining."""
        self.queue = []
        try:
            self.filename.unlink()
        except Exception as e:
            logger.warning(f"Failed to clear queue file: {e}")


class ActiveLearner:
    """Active learning loop - asks for clarification when uncertain."""

    def __init__(self, queue: Optional[ActiveLearningQueue] = None):
        self.queue = queue or ActiveLearningQueue()
        self.clarification_templates = {
            "longing_warm": "Just to clarify: You seem to miss someone or express warmth. Is that right?",
            "calm": "I picked up that you're feeling calm or peaceful. Did I get that right?",
            "practical_serious": "It sounds like you're focused on something practical or serious. Is that accurate?",
            "instructional": "You seem to want me to learn or remember something. Did I understand correctly?",
            "frustrated": "I sense some frustration here. Is that how you're feeling?",
            "joy": "You seem excited or joyful! Is that capturing it?",
            "neutral": "I'm not entirely sure what emotion you're expressing. Could you tell me?",
        }

    def should_query_user(self, confidence: float) -> bool:
        """Decide whether to ask for user clarification."""
        return confidence < LOW_CONFIDENCE_THRESHOLD

    def generate_clarification_query(
        self, text: str, emotion: str, confidence: float
    ) -> str:
        """Generate a natural clarification request."""
        template = self.clarification_templates.get(emotion, self.clarification_templates["neutral"])
        return f"{template}\n(Confidence: {confidence:.0%})"

    def log_for_labeling(
        self,
        text: str,
        predicted_emotion: str,
        confidence: float,
        user_id: str = "default",
    ) -> None:
        """Log a low-confidence prediction for later labeling."""
        self.queue.add_sample(text, predicted_emotion, confidence, user_id=user_id)

    def process_user_correction(self, text: str, corrected_emotion: str) -> bool:
        """Process a user correction to a prediction."""
        success = self.queue.mark_labeled(text, corrected_emotion)
        if success:
            logger.info(f"User corrected emotion for '{text[:30]}...' to {corrected_emotion}")
        return success


def show_active_learning_dashboard(queue: ActiveLearningQueue) -> None:
    """Display active learning status dashboard."""
    status = queue.get_status()
    print("\n=== CrystalCore.OS Active Learning Status ===")
    print(f"Pending labels:  {status['pending']}")
    print(f"Labeled samples: {status['labeled']}")
    print(f"Total collected: {status['total']}")
    print(f"Ready to retrain: {'✅ Yes' if status['ready_for_retrain'] else '❌ No'}")
    if not status["ready_for_retrain"] and status["total"] > 0:
        needed = MIN_SAMPLES_FOR_RETRAIN - status["labeled"]
        print(f"Samples needed:  {max(0, needed)}")
    print("==========================================\n")


def export_labeled_data_for_training(
    queue: ActiveLearningQueue, output_file: str = "labeled_data.jsonl"
) -> Tuple[int, str]:
    """Export labeled data for training/fine-tuning."""
    labeled = queue.export_for_training()
    if not labeled:
        return 0, output_file

    try:
        with open(output_file, "w") as f:
            for entry in labeled:
                f.write(json.dumps(entry) + "\n")
        logger.info(f"Exported {len(labeled)} labeled samples to {output_file}")
        return len(labeled), output_file
    except Exception as e:
        logger.error(f"Failed to export data: {e}")
        return 0, output_file
