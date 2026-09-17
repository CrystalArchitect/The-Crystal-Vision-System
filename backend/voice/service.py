"""
Voice Processing Pipeline: Speech-to-Text → LLM → Text-to-Speech
Integrates Whisper STT, Llama 3 8B routing, and Piper TTS for voice approval workflows
"""

import io
import json
import logging
import asyncio
from typing import Optional, Tuple
from uuid import UUID
import httpx
import numpy as np

logger = logging.getLogger(__name__)


class VoiceProcessor:
    """Process voice approval requests end-to-end"""

    def __init__(
        self,
        whisper_url: str = "http://localhost:8001",
        llm_url: str = "http://localhost:11434",
        tts_url: str = "http://localhost:8002",
        portal_url: str = "http://localhost:8000"
    ):
        self.whisper_url = whisper_url
        self.llm_url = llm_url
        self.tts_url = tts_url
        self.portal_url = portal_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def transcribe_audio(self, audio_data: bytes, language: str = "en") -> Optional[str]:
        """
        Convert audio to text using Whisper API.

        Args:
            audio_data: Raw audio bytes (WAV/MP3)
            language: ISO language code (default 'en')

        Returns:
            Transcribed text or None if transcription fails
        """
        try:
            files = {"file": ("audio.wav", io.BytesIO(audio_data), "audio/wav")}
            response = await self.client.post(
                f"{self.whisper_url}/asr",
                files=files,
                params={"language": language}
            )
            response.raise_for_status()
            result = response.json()
            return result.get("text", "").strip()
        except httpx.HTTPError as e:
            logger.error(f"Whisper transcription failed: {e}")
            return None

    async def route_through_llm(
        self,
        transcribed_text: str,
        decision_code: str,
        decision_context: dict
    ) -> Tuple[str, bool]:
        """
        Process transcribed text through Llama 3 8B to understand approval intent.

        Args:
            transcribed_text: User's spoken approval request
            decision_code: The decision being approved (e.g., 'ADM-001')
            decision_context: Decision metadata from Portal

        Returns:
            Tuple of (response_text, approval_confirmed) where approval_confirmed is True if
            the steward clearly approved the decision
        """
        try:
            # Build prompt for LLM decision routing
            prompt = self._build_decision_routing_prompt(
                transcribed_text,
                decision_code,
                decision_context
            )

            response = await self.client.post(
                f"{self.llm_url}/api/generate",
                json={
                    "model": "llama2:7b",  # TODO: Switch to llama2:13b or llama3:8b when available
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3,  # Lower temp for deterministic routing
                    "num_predict": 200
                }
            )
            response.raise_for_status()
            result = response.json()
            llm_response = result.get("response", "").strip()

            # Parse LLM response to extract approval intent
            approval_confirmed = self._parse_approval_intent(llm_response, decision_code)
            return llm_response, approval_confirmed

        except httpx.HTTPError as e:
            logger.error(f"LLM routing failed: {e}")
            return "I couldn't process your voice request. Please try again.", False

    async def synthesize_speech(
        self,
        text: str,
        speaker_id: str = "default",
        language: str = "en"
    ) -> Optional[bytes]:
        """
        Convert text response to audio using Piper TTS.

        Args:
            text: Text to synthesize
            speaker_id: Voice identifier (e.g., 'default', 'steward-formal')
            language: ISO language code

        Returns:
            Audio bytes (WAV format) or None if synthesis fails
        """
        try:
            response = await self.client.post(
                f"{self.tts_url}/synthesize",
                json={
                    "text": text,
                    "speaker_id": speaker_id,
                    "language": language
                }
            )
            response.raise_for_status()
            return response.content
        except httpx.HTTPError as e:
            logger.error(f"Piper TTS synthesis failed: {e}")
            return None

    async def process_voice_approval(
        self,
        audio_data: bytes,
        decision_code: str,
        decision_context: dict,
        steward_id: UUID
    ) -> dict:
        """
        End-to-end voice approval workflow:
        1. Transcribe audio → text
        2. Route through LLM for intent understanding
        3. Synthesize spoken response

        Args:
            audio_data: Raw audio bytes from device
            decision_code: Decision being approved (e.g., 'ADM-001')
            decision_context: Decision metadata
            steward_id: Steward ID for audit trail

        Returns:
            Response dict with:
            - transcript: Original transcribed text
            - llm_response: LLM's understanding
            - approval_confirmed: Whether approval was granted
            - audio_response: Base64-encoded TTS audio
            - approval_hash: Voice signature hash (SHA-256 of audio)
        """
        try:
            # Step 1: Transcribe
            transcript = await self.transcribe_audio(audio_data)
            if not transcript:
                return {
                    "error": "Failed to transcribe audio",
                    "transcript": None,
                    "approval_confirmed": False
                }

            logger.info(f"Transcribed: {transcript} (decision: {decision_code})")

            # Step 2: Route through LLM
            llm_response, approval_confirmed = await self.route_through_llm(
                transcript,
                decision_code,
                decision_context
            )

            # Step 3: Synthesize spoken response
            response_text = self._format_approval_response(
                approval_confirmed,
                decision_code,
                decision_context
            )
            audio_response = await self.synthesize_speech(response_text)

            # Compute voice signature hash
            import hashlib
            voice_hash = hashlib.sha256(audio_data).hexdigest() if audio_response else None

            return {
                "transcript": transcript,
                "llm_response": llm_response,
                "approval_confirmed": approval_confirmed,
                "audio_response": audio_response,
                "voice_signature_hash": voice_hash,
                "steward_id": str(steward_id),
                "decision_code": decision_code
            }

        except Exception as e:
            logger.error(f"Voice approval processing failed: {e}")
            return {
                "error": str(e),
                "approval_confirmed": False
            }

    def _build_decision_routing_prompt(
        self,
        user_speech: str,
        decision_code: str,
        decision_context: dict
    ) -> str:
        """Build prompt for LLM to understand approval intent"""
        decision_type = decision_context.get("decision_type", "policy")
        decision_title = decision_context.get("title", "Administrative Decision")

        return f"""You are a governance assistant helping stewards approve administrative decisions.

Decision Code: {decision_code}
Decision Title: {decision_title}
Decision Type: {decision_type}

The steward just said: "{user_speech}"

Your task: Determine if the steward is approving, denying, or asking clarification questions about this decision.

Respond with:
1. A brief (1-2 sentence) confirmation of what you understood
2. Your assessment: "APPROVAL", "DENIAL", or "CLARIFICATION_NEEDED"

For example:
- If steward says "Yes, approve the linting standards", respond: "You want to approve the linting standards update. APPROVAL"
- If steward says "Hold on, what about the exceptions?", respond: "You need clarification about edge cases. CLARIFICATION_NEEDED"
- If steward says "No, this breaks too much", respond: "You're denying this change. DENIAL"

Be strict about APPROVAL: only mark as APPROVAL if the steward explicitly says yes/approve/confirm.
"""

    def _parse_approval_intent(self, llm_response: str, decision_code: str) -> bool:
        """Extract approval intent from LLM response"""
        response_upper = llm_response.upper()

        # Look for explicit approval markers
        if "APPROVAL" in response_upper:
            logger.info(f"Decision {decision_code}: Approval confirmed via voice")
            return True
        elif "DENIAL" in response_upper:
            logger.info(f"Decision {decision_code}: Denial via voice")
            return False
        elif "CLARIFICATION" in response_upper or "QUESTION" in response_upper:
            logger.info(f"Decision {decision_code}: Clarification needed")
            return False

        # Fallback: check for approval-like phrases
        approval_phrases = ["yes", "approve", "confirm", "i agree", "go ahead", "accepted"]
        for phrase in approval_phrases:
            if phrase in response_upper:
                logger.info(f"Decision {decision_code}: Approval inferred from '{phrase}'")
                return True

        return False

    def _format_approval_response(
        self,
        approved: bool,
        decision_code: str,
        decision_context: dict
    ) -> str:
        """Format spoken response to steward"""
        decision_title = decision_context.get("title", f"Decision {decision_code}")

        if approved:
            return f"Thank you. {decision_title} has been approved and canonicalized to the governance vault."
        else:
            return f"Understood. {decision_title} was not approved. No changes were made."

    async def close(self):
        """Clean up HTTP client"""
        await self.client.aclose()


# Singleton instance
_voice_processor: Optional[VoiceProcessor] = None


async def get_voice_processor(
    whisper_url: str = "http://localhost:8001",
    llm_url: str = "http://localhost:11434",
    tts_url: str = "http://localhost:8002",
    portal_url: str = "http://localhost:8000"
) -> VoiceProcessor:
    """Get or create VoiceProcessor singleton"""
    global _voice_processor
    if _voice_processor is None:
        _voice_processor = VoiceProcessor(whisper_url, llm_url, tts_url, portal_url)
    return _voice_processor
