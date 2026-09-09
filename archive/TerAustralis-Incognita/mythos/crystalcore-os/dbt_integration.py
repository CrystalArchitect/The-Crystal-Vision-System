# CrystalCore.OS - dbt Integration Module
# Exports emotion predictions, active learning data, and uncertainty metrics to data warehouse

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class DbtDataExporter:
    """Export CrystalCore.OS data to dbt warehouse."""

    def __init__(self, export_dir: str = "~/.crystalcore/dbt_exports"):
        """
        Initialize dbt exporter.

        Args:
            export_dir: Directory for JSONL exports
        """
        self.export_dir = Path(export_dir).expanduser()
        self.export_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"DbtDataExporter initialized, export_dir={self.export_dir}")

    def export_prediction(
        self,
        text: str,
        emotion: str,
        emotion_idx: int,
        confidence: float,
        entropy: float,
        least_confidence: float,
        margin_uncertainty: float,
        modalities: List[str],
        epistemic_uncertainty: float = None,
        aleatoric_uncertainty: float = None,
        mc_samples: int = None,
        should_query: bool = False,
        query_reason: str = None,
    ) -> str:
        """
        Export a single emotion prediction to dbt.

        Args:
            text: Input text
            emotion: Predicted emotion label
            emotion_idx: Emotion index (0-27)
            confidence: Model confidence (0.0-1.0)
            entropy: Shannon entropy
            least_confidence: Least confidence metric
            margin_uncertainty: Margin uncertainty
            modalities: List of modalities used ('text', 'audio', 'vision')
            epistemic_uncertainty: Bayesian epistemic uncertainty
            aleatoric_uncertainty: Bayesian aleatoric uncertainty
            mc_samples: Number of MC dropout samples
            should_query: Whether to query user for feedback
            query_reason: Reason for active learning query

        Returns:
            Prediction ID
        """
        prediction = {
            "prediction_timestamp": datetime.utcnow().isoformat(),
            "input_text": text,
            "emotion_detected": emotion,
            "emotion_idx": emotion_idx,
            "confidence": round(confidence, 4),
            "entropy": round(entropy, 4),
            "least_confidence": round(least_confidence, 4),
            "margin_uncertainty": round(margin_uncertainty, 4),
            "modalities": ",".join(modalities) if modalities else "text",
            "epistemic_uncertainty": round(epistemic_uncertainty, 4) if epistemic_uncertainty else None,
            "aleatoric_uncertainty": round(aleatoric_uncertainty, 4) if aleatoric_uncertainty else None,
            "mc_samples": mc_samples,
            "should_query_user": should_query,
            "query_reason": query_reason,
            "label_status": "pending",
            "user_label": None,
            "label_confidence": None,
            "labeled_at": None,
        }

        # Append to predictions JSONL
        predictions_file = self.export_dir / "stg_emotion_predictions.jsonl"
        with open(predictions_file, "a") as f:
            f.write(json.dumps(prediction) + "\n")

        logger.debug(f"Exported prediction: {emotion} (confidence={confidence:.3f})")
        return prediction.get("prediction_timestamp")

    def export_active_learning_sample(
        self,
        text: str,
        predicted_emotion: str,
        predicted_emotion_idx: int,
        confidence: float,
        entropy: float,
        is_uncertain: bool,
        uncertainty_reason: str,
        model_version: str,
    ) -> str:
        """
        Export low-confidence prediction to active learning queue.

        Args:
            text: Input text
            predicted_emotion: Model's prediction
            predicted_emotion_idx: Emotion index
            confidence: Model confidence
            entropy: Prediction entropy
            is_uncertain: Whether sample is uncertain
            uncertainty_reason: Why sample triggered active learning
            model_version: Version of model that made prediction

        Returns:
            Queue ID
        """
        queue_entry = {
            "queue_timestamp": datetime.utcnow().isoformat(),
            "text_input": text,
            "predicted_emotion": predicted_emotion,
            "predicted_emotion_idx": predicted_emotion_idx,
            "confidence": round(confidence, 4),
            "entropy": round(entropy, 4),
            "is_uncertain": is_uncertain,
            "uncertainty_reason": uncertainty_reason,
            "model_version": model_version,
            "status": "unlabeled",
            "user_feedback_emotion": None,
            "user_feedback_confidence": None,
            "feedback_received_at": None,
            "used_for_retraining": False,
        }

        # Append to queue JSONL
        queue_file = self.export_dir / "stg_active_learning_queue.jsonl"
        with open(queue_file, "a") as f:
            f.write(json.dumps(queue_entry) + "\n")

        logger.info(f"Queued sample: {predicted_emotion} (entropy={entropy:.3f})")
        return queue_entry.get("queue_timestamp")

    def update_label(
        self,
        queue_timestamp: str,
        user_emotion: str,
        user_confidence: float,
    ) -> None:
        """
        Update active learning queue with user feedback.

        Args:
            queue_timestamp: Timestamp of queued sample
            user_emotion: User's labeled emotion
            user_confidence: User's confidence in label (0.0-1.0)
        """
        queue_file = self.export_dir / "stg_active_learning_queue.jsonl"

        # Read all entries
        entries = []
        if queue_file.exists():
            with open(queue_file, "r") as f:
                entries = [json.loads(line) for line in f]

        # Update matching entry
        for entry in entries:
            if entry.get("queue_timestamp") == queue_timestamp:
                entry["status"] = "labeled"
                entry["user_feedback_emotion"] = user_emotion
                entry["user_feedback_confidence"] = round(user_confidence, 4)
                entry["feedback_received_at"] = datetime.utcnow().isoformat()
                break

        # Write back
        with open(queue_file, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")

        logger.info(f"Updated label for {queue_timestamp}: {user_emotion}")

    def export_daily_metrics(
        self,
        date: str,
        emotion: str,
        prediction_count: int,
        avg_confidence: float,
        avg_entropy: float,
        queries_triggered: int,
        labeled_count: int,
    ) -> None:
        """
        Export daily emotion metrics for aggregation.

        Args:
            date: Date (YYYY-MM-DD)
            emotion: Emotion label
            prediction_count: Number of predictions that day
            avg_confidence: Average confidence
            avg_entropy: Average entropy
            queries_triggered: Active learning queries triggered
            labeled_count: Labels collected
        """
        metric = {
            "prediction_date": date,
            "emotion_label": emotion,
            "prediction_count": prediction_count,
            "avg_confidence": round(avg_confidence, 4),
            "avg_entropy": round(avg_entropy, 4),
            "queries_triggered": queries_triggered,
            "labeled_count": labeled_count,
        }

        metrics_file = self.export_dir / "agg_daily_emotion_metrics.jsonl"
        with open(metrics_file, "a") as f:
            f.write(json.dumps(metric) + "\n")

        logger.debug(f"Exported daily metrics for {emotion} on {date}")

    def get_export_status(self) -> Dict:
        """Get status of all exports."""
        status = {
            "export_dir": str(self.export_dir),
            "files": {},
            "total_predictions": 0,
            "total_queued": 0,
            "total_labeled": 0,
        }

        # Count predictions
        predictions_file = self.export_dir / "stg_emotion_predictions.jsonl"
        if predictions_file.exists():
            with open(predictions_file, "r") as f:
                predictions = [json.loads(line) for line in f]
                status["total_predictions"] = len(predictions)
                status["files"]["predictions"] = str(predictions_file)

        # Count active learning queue
        queue_file = self.export_dir / "stg_active_learning_queue.jsonl"
        if queue_file.exists():
            with open(queue_file, "r") as f:
                queue_entries = [json.loads(line) for line in f]
                status["total_queued"] = len(queue_entries)
                status["total_labeled"] = sum(
                    1 for e in queue_entries if e.get("status") == "labeled"
                )
                status["files"]["queue"] = str(queue_file)

        return status


class DbtDataIngester:
    """Ingest dbt warehouse data back into CrystalCore.OS."""

    def __init__(self, dbt_project_path: str = "./dbt/crystalcore_emotion_warehouse"):
        """
        Initialize dbt ingester.

        Args:
            dbt_project_path: Path to dbt project
        """
        self.dbt_project_path = Path(dbt_project_path)
        logger.info(f"DbtDataIngester initialized, project_path={self.dbt_project_path}")

    def get_emotion_distribution(self) -> Dict[str, int]:
        """Get emotion distribution from fact table."""
        # This would read from dbt-generated tables in data warehouse
        # Placeholder for actual implementation
        logger.info("Retrieving emotion distribution from dbt warehouse")
        return {}

    def get_low_confidence_predictions(self, limit: int = 100) -> List[Dict]:
        """Get low-confidence predictions for active learning."""
        logger.info(f"Retrieving {limit} low-confidence predictions from dbt warehouse")
        return []

    def get_model_performance_metrics(self) -> Dict:
        """Get model performance metrics from dbt aggregates."""
        logger.info("Retrieving model performance metrics from dbt warehouse")
        return {
            "total_predictions": 0,
            "avg_confidence": 0.0,
            "avg_entropy": 0.0,
            "active_learning_queries": 0,
            "labels_collected": 0,
        }


def print_dbt_integration_guide() -> str:
    """Print guide for dbt integration with CrystalCore.OS."""
    return """
╔═══════════════════════════════════════════════════════════════════╗
║           CrystalCore.OS × dbt Integration Guide                  ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║ DATA FLOW:                                                        ║
║ CrystalCore.OS → DbtDataExporter → JSONL files                   ║
║ → dbt (transform) → Data Warehouse (DuckDB/BigQuery)             ║
║ → Analytics, BI Dashboard, Model Retraining                      ║
║                                                                   ║
║ EXPORT METHODS:                                                  ║
║                                                                   ║
║ 1. Emotion Predictions                                           ║
║    exporter.export_prediction(text, emotion, confidence, ...)    ║
║    Stores: stg_emotion_predictions.jsonl                         ║
║                                                                   ║
║ 2. Active Learning Queue                                         ║
║    exporter.export_active_learning_sample(text, pred, ...)       ║
║    Stores: stg_active_learning_queue.jsonl                       ║
║                                                                   ║
║ 3. User Labels                                                   ║
║    exporter.update_label(queue_timestamp, emotion, confidence)   ║
║    Updates: stg_active_learning_queue.jsonl                      ║
║                                                                   ║
║ 4. Daily Metrics                                                 ║
║    exporter.export_daily_metrics(date, emotion, count, ...)      ║
║    Stores: agg_daily_emotion_metrics.jsonl                       ║
║                                                                   ║
║ RUNNING dbt:                                                     ║
║                                                                   ║
║  cd dbt/crystalcore_emotion_warehouse                            ║
║  dbt run       # Transform data                                  ║
║  dbt test      # Validate quality                                ║
║  dbt docs      # Generate documentation                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
