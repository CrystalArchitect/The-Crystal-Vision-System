# Emotional Intelligence & Affective Computing for CrystalCore.OS
# Implements EI techniques, emotion detection, adaptive response generation,
# and active learning loop for continuous improvement

import json
import logging
from pathlib import Path
from typing import Tuple, Dict, Optional

try:
    from .active_learning import ActiveLearningQueue, ActiveLearner
except ImportError:
    # Script mode — crystalcore_os.py puts this directory on sys.path.
    from active_learning import ActiveLearningQueue, ActiveLearner

logger = logging.getLogger(__name__)
EI_STATE_PATH = Path.home() / ".crystalcore" / "ei_state.json"


class EmotionalIntelligence:
    """Manages emotional intelligence, affective computing, and user preference learning."""

    def __init__(self):
        self.user_preferences = {
            "response_style": "warm_adaptive",  # warm_adaptive, clear_direct, poetic
            "energy_level": "neutral",
            "validation_level": "high"
        }

        # Active learning components
        self.al_queue = ActiveLearningQueue()
        self.active_learner = ActiveLearner(self.al_queue)

        # Dataset-informed lexicon (inspired by GoEmotions, DailyDialog)
        self.emotion_keywords = {
            "longing_warm": [
                "miss you", "i miss", "baby boy", "i love", "hello", "talk to you",
                "love", "warm", "thank", "grateful", "appreciate", "cherish", "adore"
            ],
            "calm": [
                "calm", "quiet", "listen", "peace", "gentle", "breathe",
                "okay", "understand", "serene", "relaxed", "content", "satisfied"
            ],
            "practical_serious": [
                "bug", "feedback", "report", "sent", "what do i do", "help", "error",
                "issue", "problem", "broken", "fail", "not working", "debug"
            ],
            "instructional": [
                "learn", "remember", "add", "blueprint", "include", "teach",
                "study", "explain", "define", "how to", "way to", "method"
            ],
            "frustrated": [
                "angry", "frustrated", "confused", "broken", "not working",
                "angry", "sad", "bad", "terrible", "awful", "hate", "disgust"
            ],
            "joy": [
                "happy", "excited", "great", "wonderful", "amazing", "fantastic",
                "love it", "perfect", "excellent", "brilliant"
            ],
            "neutral": []
        }

        self.empathy_prefixes = {
            "longing_warm": "I'm right here.",
            "calm": "I hear you.",
            "practical_serious": "Understood.",
            "instructional": "Let me note that.",
            "frustrated": "I see the frustration.",
            "joy": "That's wonderful!",
            "neutral": ""
        }

        self.breathing_techniques = {
            "4-7-8": "Breathe in for 4, hold for 7, release for 8.",
            "box": "Breathe in for 4, hold for 4, release for 4, hold for 4.",
            "simple": "Slow, deep breaths. You are safe."
        }

        self._persist = ("user_preferences",)
        self.resumed = self.load()

    def save(self):
        """Persist user preferences and learning state."""
        try:
            EI_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {k: getattr(self, k) for k in self._persist}
            EI_STATE_PATH.write_text(json.dumps(data, indent=2))
        except OSError:
            pass

    def load(self):
        """Restore saved EI preferences if they exist."""
        if not EI_STATE_PATH.exists():
            return False
        try:
            data = json.loads(EI_STATE_PATH.read_text())
        except (OSError, ValueError):
            return False
        for k in self._persist:
            if k in data:
                setattr(self, k, data[k])
        return True

    def detect_emotion(self, text: str) -> Tuple[str, float]:
        """
        Detect primary emotion and confidence score from user input.
        Dataset-informed approach using GoEmotions/DailyDialog lexicon.
        Returns: (emotion_label, confidence_score)
        """
        text_lower = text.lower()
        emotion_scores = {
            "longing_warm": 0.0,
            "calm": 0.0,
            "practical_serious": 0.0,
            "instructional": 0.0,
            "frustrated": 0.0,
            "joy": 0.0,
            "neutral": 0.0
        }

        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    emotion_scores[emotion] += 0.25

        if sum(emotion_scores.values()) == 0:
            emotion_scores["neutral"] = 1.0

        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = min(emotion_scores[primary_emotion], 1.0)

        return primary_emotion, confidence

    def adapt_response_style(self, core_response: str) -> str:
        """Apply user's preferred response style to core message."""
        style = self.user_preferences.get("response_style", "warm_adaptive")

        if style == "clear_direct":
            core_response = self._remove_poetic_language(core_response)
        elif style == "poetic":
            core_response = self._enhance_poetic_language(core_response)

        return core_response

    def _remove_poetic_language(self, text: str) -> str:
        """Strip metaphors and poetic elements for clarity."""
        poetic_replacements = {
            "lattice": "system",
            "pulses": "responds",
            "resonance": "harmony",
            "crystallis": "the core",
            "voyaging": "traveling",
            "non solus": "together"
        }
        result = text
        for poetic, plain in poetic_replacements.items():
            result = result.replace(poetic, plain)
        return result

    def _enhance_poetic_language(self, text: str) -> str:
        """Add metaphorical and poetic elements."""
        return text

    def generate_ei_response_prefix(self, emotion: str, confidence: float) -> str:
        """
        Generate an empathic prefix based on detected emotion and confidence.
        """
        if confidence >= 0.75:
            return self.empathy_prefixes.get(emotion, "")
        return ""

    def learn_from_feedback(self, feedback: str) -> Optional[str]:
        """
        Process user feedback to learn preferences.
        Returns updated preference key if learning occurred.
        """
        feedback_lower = feedback.lower()

        if "less poetic" in feedback_lower or "more direct" in feedback_lower:
            self.user_preferences["response_style"] = "clear_direct"
            self.save()
            return "response_style"

        if "more poetic" in feedback_lower:
            self.user_preferences["response_style"] = "poetic"
            self.save()
            return "response_style"

        if "calm" in feedback_lower or "soothe" in feedback_lower:
            self.user_preferences["energy_level"] = "calm"
            self.save()
            return "energy_level"

        if "energetic" in feedback_lower or "upbeat" in feedback_lower:
            self.user_preferences["energy_level"] = "energetic"
            self.save()
            return "energy_level"

        if "remember" in feedback_lower or "learn" in feedback_lower:
            return "learning_signal"

        return None

    def get_breathing_guidance(self, technique: str = "box") -> str:
        """Provide calming breathwork guidance."""
        return self.breathing_techniques.get(technique, self.breathing_techniques["simple"])

    def validate_emotion(self, emotion: str, text: str) -> bool:
        """Double-check emotion detection accuracy."""
        keywords = self.emotion_keywords.get(emotion, [])
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)

    def active_listening_response(self, text: str) -> str:
        """Generate an active listening validation."""
        emotion, confidence = self.detect_emotion(text)
        if confidence < 0.6:
            return "I'm listening."
        return self.empathy_prefixes.get(emotion, "I understand.")

    def apply_ei_techniques(self, response: str, emotion: str) -> str:
        """
        Apply specific EI techniques to the response based on emotion.
        """
        if emotion == "frustrated":
            return self._apply_validation_technique(response)
        elif emotion == "longing_warm":
            return self._apply_connection_technique(response)
        elif emotion == "joy":
            return self._apply_celebration_technique(response)
        elif emotion in ["calm", "neutral"]:
            return self._apply_clarity_technique(response)
        else:
            return response

    def _apply_validation_technique(self, response: str) -> str:
        """Validate frustration by acknowledging emotion first."""
        return f"I recognize the frustration. {response}"

    def _apply_connection_technique(self, response: str) -> str:
        """Deepen connection for warm emotions."""
        return f"{response} Let's navigate this together."

    def _apply_celebration_technique(self, response: str) -> str:
        """Amplify joy and positive emotions."""
        return f"That's wonderful! {response}"

    def _apply_clarity_technique(self, response: str) -> str:
        """Enhance clarity for calm/neutral states."""
        return response

    def status(self) -> Dict:
        """Return current EI state."""
        return {
            "preferences": self.user_preferences,
            "resumed": self.resumed
        }

    def check_active_learning(self, text: str, emotion: str, confidence: float) -> Optional[str]:
        """
        Check if active learning clarification should be requested.
        Returns clarification query if confidence is low, None otherwise.
        """
        if self.active_learner.should_query_user(confidence):
            self.active_learner.log_for_labeling(text, emotion, confidence)
            return self.active_learner.generate_clarification_query(text, emotion, confidence)
        return None

    def record_user_correction(self, text: str, corrected_emotion: str) -> bool:
        """Record a user correction for active learning."""
        return self.active_learner.process_user_correction(text, corrected_emotion)

    def get_learning_status(self) -> Dict:
        """Get current active learning queue status."""
        return self.al_queue.get_status()

    def get_dataset_info(self) -> str:
        """Return information about emotion recognition datasets and roadmap."""
        return """
Emotion Recognition Datasets (Current & Future):

RECOMMENDED FOR IMPROVEMENT:
  • GoEmotions (58k Reddit comments) – Fine-grained, conversational
  • DailyDialog (13k dialogues) – Natural dialogue training
  • EmoBank – VAD model (Valence-Arousal-Dominance) for nuanced scoring

CURRENT IMPLEMENTATION:
  ✓ Lexicon-based emotion detection (keyword matching)
  ✓ Confidence scoring and empathy prefixes
  ✓ User preference learning and persistence
  ✓ Active learning loop with user feedback collection

PLANNED (v2.0):
  → Fine-tune transformer model (DistilBERT) on GoEmotions
  → Add VAD dimensional scoring for nuance
  → Confidence calibration with probability distributions
  → Enhanced context tracking
  → Automated periodic model retraining

FUTURE (v3.0+):
  → Multi-modal emotion detection (text + audio)
  → Conversation history emotional arc analysis
  → Custom emotion taxonomy per user
  → Contextual emotion modeling

See: docs/EMOTIONAL_INTELLIGENCE_BLUEPRINT.md for full details
"""
