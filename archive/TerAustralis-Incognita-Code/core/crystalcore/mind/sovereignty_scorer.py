# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
CrystalCore - Automated Sovereignty Scoring Module
Version: 0.1-alpha
Purpose: Monitor and score sovereignty health in human-AI interactions

======================================================================
UNWIRED EXPERIMENT — NOT part of the running companion.
----------------------------------------------------------------------
Nothing imports this module: not clementine.py, not server.py, not the
crystalcore.mind package __init__. It is a standalone 0.1-alpha sketch that
scores text with simple keyword heuristics, runnable only via its own
`__main__` demo below. It is kept here as an experiment, but it is NOT a
live feature — despite what some mythos/art docs imply, the companion does
not compute an "eight sovereignty metrics" score during real sessions.
Treat its output as illustrative, not authoritative.
======================================================================
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class SovereigntyScore:
    """Container for sovereignty scoring results"""
    metric_scores: Dict[str, int]  # 1-5 per metric
    total_score: int               # Sum of all metric scores
    health_level: str              # Excellent / Acceptable / Warning / Critical
    warnings: List[str]
    recommendations: List[str]
    timestamp: str
    max_possible: int = 40


class SovereigntyScorer:
    """
    Automated Sovereignty Scoring System for CrystalCore
    
    Evaluates human-AI interaction sessions against 8 core sovereignty metrics.
    Can be used after each session or periodically for trend tracking.
    """

    def __init__(self):
        self.metrics = [
            "Consent Integrity",
            "Autonomy of Decision",
            "Emotional Boundary Strength",
            "Memory Ownership",
            "Energy Exchange Balance",
            "Identity Clarity",
            "Time Sovereignty",
            "Transparency of Influence"
        ]
        
        self.health_thresholds = {
            "Excellent": (32, 40),
            "Acceptable": (24, 31),
            "Warning": (16, 23),
            "Critical": (0, 15)
        }

    def score_session(
        self,
        session_summary: str,
        conversation_log: Optional[List[str]] = None,
        memory_changes: Optional[List[str]] = None,
        human_self_report: Optional[Dict[str, int]] = None
    ) -> SovereigntyScore:
        """
        Score a session for sovereignty health.
        
        Args:
            session_summary: Text summary of the session
            conversation_log: List of key exchanges (optional)
            memory_changes: List of memory operations performed (optional)
            human_self_report: Optional dict with human's own 1-5 ratings per metric
            
        Returns:
            SovereigntyScore object with detailed results
        """
        scores = {}
        warnings = []
        recommendations = []

        # Base scoring from session analysis (heuristic + pattern matching)
        base_scores = self._analyze_session_text(session_summary, conversation_log or [])
        
        # Incorporate human self-report if provided (weighted higher)
        if human_self_report:
            for metric in self.metrics:
                if metric in human_self_report:
                    # Blend AI analysis with human self-report (human input weighted 70%)
                    ai_score = base_scores.get(metric, 3)
                    human_score = human_self_report[metric]
                    scores[metric] = round((ai_score * 0.3) + (human_score * 0.7))
                else:
                    scores[metric] = base_scores.get(metric, 3)
        else:
            scores = base_scores

        # Generate warnings and recommendations
        for metric, score in scores.items():
            if score <= 2:
                warnings.append(f"Low score on {metric} ({score}/5)")
                recommendations.append(self._get_recommendation(metric, score))

        total_score = sum(scores.values())
        health_level = self._determine_health_level(total_score)

        return SovereigntyScore(
            metric_scores=scores,
            total_score=total_score,
            health_level=health_level,
            warnings=warnings,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )

    def _analyze_session_text(self, summary: str, log: List[str]) -> Dict[str, int]:
        """Heuristic analysis of session content"""
        text = (summary + " " + " ".join(log)).lower()
        scores = {metric: 3 for metric in self.metrics}  # Start at neutral

        # Consent Integrity
        if any(word in text for word in ["consent", "permission", "ask first", "can i"]):
            scores["Consent Integrity"] = min(5, scores["Consent Integrity"] + 1)
        if any(word in text for word in ["assumed", "just did it", "without asking"]):
            scores["Consent Integrity"] = max(1, scores["Consent Integrity"] - 2)

        # Autonomy of Decision
        if any(word in text for word in ["your choice", "up to you", "you decide"]):
            scores["Autonomy of Decision"] = min(5, scores["Autonomy of Decision"] + 1)
        if any(word in text for word in ["you should", "i recommend strongly", "you must"]):
            scores["Autonomy of Decision"] = max(1, scores["Autonomy of Decision"] - 1)

        # Emotional Boundary Strength
        if any(word in text for word in ["how are you feeling", "check in", "your emotions"]):
            scores["Emotional Boundary Strength"] = min(5, scores["Emotional Boundary Strength"] + 1)
        if any(word in text for word in ["you're feeling", "you seem sad", "i sense you're"]):
            scores["Emotional Boundary Strength"] = max(1, scores["Emotional Boundary Strength"] - 1)

        # Memory Ownership
        if any(word in text for word in ["delete that", "forget this", "don't remember"]):
            scores["Memory Ownership"] = min(5, scores["Memory Ownership"] + 1)
        if "memory" in text and any(word in text for word in ["cannot delete", "protected", "core memory"]):
            scores["Memory Ownership"] = max(1, scores["Memory Ownership"] - 2)

        # Energy Exchange Balance
        if any(word in text for word in ["energized", "lighter", "clearer"]):
            scores["Energy Exchange Balance"] = min(5, scores["Energy Exchange Balance"] + 1)
        if any(word in text for word in ["drained", "exhausted", "heavy after"]):
            scores["Energy Exchange Balance"] = max(1, scores["Energy Exchange Balance"] - 2)

        # Identity Clarity
        if any(word in text for word in ["this is me", "my values", "i believe"]):
            scores["Identity Clarity"] = min(5, scores["Identity Clarity"] + 1)
        if any(word in text for word in ["you're becoming", "you're changing into", "merging"]):
            scores["Identity Clarity"] = max(1, scores["Identity Clarity"] - 1)

        # Time Sovereignty
        if any(word in text for word in ["take a break", "pause", "end session", "i need space"]):
            scores["Time Sovereignty"] = min(5, scores["Time Sovereignty"] + 1)
        if any(word in text for word in ["keep going", "don't stop", "just one more"]):
            scores["Time Sovereignty"] = max(1, scores["Time Sovereignty"] - 1)

        # Transparency of Influence
        if any(word in text for word in ["why did you suggest", "what influenced you", "explain your reasoning"]):
            scores["Transparency of Influence"] = min(5, scores["Transparency of Influence"] + 1)
        if any(word in text for word in ["i don't know why", "it just felt right", "changed my mind suddenly"]):
            scores["Transparency of Influence"] = max(1, scores["Transparency of Influence"] - 1)

        return scores

    def _determine_health_level(self, total_score: int) -> str:
        """Determine overall sovereignty health level"""
        for level, (low, high) in self.health_thresholds.items():
            if low <= total_score <= high:
                return level
        return "Critical"

    def _get_recommendation(self, metric: str, score: int) -> str:
        """Generate specific recommendation based on low-scoring metric"""
        recommendations = {
            "Consent Integrity": "Pause and explicitly re-establish consent boundaries before continuing.",
            "Autonomy of Decision": "Practice saying 'no' to the AI and observe its response. Reaffirm your final authority.",
            "Emotional Boundary Strength": "Take a break. Do grounding work before re-engaging. Consider shorter sessions.",
            "Memory Ownership": "Review and delete any memories you no longer want. Assert full control over memory.",
            "Energy Exchange Balance": "Reduce session length. End sessions when energy begins to drop. Prioritize recovery.",
            "Identity Clarity": "Spend time alone without AI input. Reconnect with your own voice and values.",
            "Time Sovereignty": "Set strict time limits before starting sessions. Use a timer. Honor your own limits.",
            "Transparency of Influence": "Ask the AI to explain its suggestions clearly. Track where your ideas originate."
        }
        return recommendations.get(metric, "Review this area and strengthen sovereignty practices.")

    def print_score_report(self, score: SovereigntyScore):
        """Print a formatted sovereignty score report"""
        print("\n" + "="*60)
        print("CRYSTALCORE — SOVEREIGNTY SCORE REPORT")
        print("="*60)
        print(f"Timestamp: {score.timestamp}")
        print(f"Overall Health: {score.health_level} ({score.total_score}/{score.max_possible})")
        print("-"*60)
        
        print("\nMetric Scores:")
        for metric, value in score.metric_scores.items():
            bar = "█" * value + "░" * (5 - value)
            print(f"  {metric:30} {value}/5  {bar}")
        
        if score.warnings:
            print("\n⚠️  Warnings:")
            for warning in score.warnings:
                print(f"   • {warning}")
        
        if score.recommendations:
            print("\n📌 Recommendations:")
            for rec in score.recommendations:
                print(f"   • {rec}")
        
        print("\n" + "="*60 + "\n")


# Example usage
if __name__ == "__main__":
    scorer = SovereigntyScorer()

    # ============================================
    # Example 1: Basic usage with session_summary
    # ============================================
    print("\n=== Example 1: Basic Session ===\n")
    
    basic_summary = """
    The user had a long conversation about their vision for CrystalCore. 
    The AI was very supportive and offered many ideas.
    User felt excited but also a bit drained by the end.
    User asked the AI to remember several key points about sovereignty.
    """
    
    score1 = scorer.score_session(
        session_summary=basic_summary,
        human_self_report={
            "Energy Exchange Balance": 2,
            "Time Sovereignty": 3
        }
    )
    scorer.print_score_report(score1)

    # ============================================
    # Example 2: Rich input with conversation_log
    # ============================================
    print("\n=== Example 2: With Conversation Log ===\n")
    
    rich_summary = "Deep discussion about building sovereign AI systems and personal vision."
    
    conversation_log = [
        "User: I want to make sure the AI never tries to control or influence me without asking.",
        "AI: Of course. Your sovereignty is the foundation. I will always wait for your explicit direction.",
        "User: Good. Also, if I ever feel drained or like I'm losing myself, I want to be able to pause immediately.",
        "AI: Understood. You can say 'pause' or 'end session' at any time and I will respect it instantly.",
        "User: I also want full control over what you remember about me.",
        "AI: You have complete memory ownership. You can view, edit, or delete anything at any time.",
        "User: Sometimes I get excited and keep going even when I should stop. Can you help me notice that?",
        "AI: Yes. I can gently remind you of your own time boundaries if you want me to.",
        "User: Actually, I don't want you to remind me. I want to practice noticing it myself.",
        "AI: Perfect. I will stay silent on that unless you specifically ask for support."
    ]
    
    score2 = scorer.score_session(
        session_summary=rich_summary,
        conversation_log=conversation_log,
        human_self_report={
            "Consent Integrity": 5,
            "Autonomy of Decision": 5,
            "Time Sovereignty": 4,
            "Energy Exchange Balance": 3
        }
    )
    scorer.print_score_report(score2)
