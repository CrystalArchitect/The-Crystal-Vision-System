"""
Transcript: Dialogue recording (ARCHIVE + CHRONICLE registers)

Preserves exchanges between human and Convergence Lens for later review.

Example:
  transcript = Transcript()

  transcript.add_turn(
    speaker='human',
    text="Do you think we'll have AGI by 2030?",
    role='guide'  # which Companion role was active?
  )

  transcript.add_turn(
    speaker='lens',
    text="That's a claim about the future. Let me decompose it.",
    role='recorder'
  )

  # Save as ARCHIVE + CHRONICLE record
  transcript.save_to_archive(path="~/.crystalcore/archives/agi-2030.jsonl")
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json


@dataclass
class Turn:
  """A single exchange in a dialogue."""

  speaker: str
  """'human' | 'lens' (the Convergence Lens interface)"""

  text: str
  """What was said."""

  timestamp: str
  """ISO8601 when this was spoken."""

  role: Optional[str] = None
  """Which Companion role was active: 'guide' | 'challenger' | 'recorder' | 'governance'"""

  classification: Optional[dict] = None
  """If Lens classified this statement, include the result."""

  uncertainty_map: Optional[dict] = None
  """If Lens mapped uncertainty, include the result."""

  def as_archive_entry(self) -> dict:
    """Serialize for ARCHIVE storage."""
    return {
      'speaker': self.speaker,
      'text': self.text,
      'timestamp': self.timestamp,
      'role': self.role,
      'classification': self.classification,
      'uncertainty_map': self.uncertainty_map,
    }


@dataclass
class Transcript:
  """A preserved dialogue."""

  session_id: str
  """Unique identifier for this conversation."""

  turns: List[Turn] = field(default_factory=list)
  subject: Optional[str] = None
  """What is this conversation about?"""

  def add_turn(self, speaker: str, text: str, role: Optional[str] = None,
               classification: Optional[dict] = None,
               uncertainty_map: Optional[dict] = None):
    """Record a turn in the conversation."""

    turn = Turn(
      speaker=speaker,
      text=text,
      timestamp=datetime.utcnow().isoformat() + 'Z',
      role=role,
      classification=classification,
      uncertainty_map=uncertainty_map,
    )
    self.turns.append(turn)

  def summary(self) -> str:
    """Brief overview of this transcript."""
    human_turns = len([t for t in self.turns if t.speaker == 'human'])
    lens_turns = len([t for t in self.turns if t.speaker == 'lens'])
    return (f"Session {self.session_id}: "
            f"{human_turns} human turn(s), {lens_turns} lens turn(s). "
            f"Subject: {self.subject or 'unspecified'}")

  def as_jsonl(self) -> str:
    """Serialize as JSONL (one entry per line) for CHRONICLE."""
    lines = []
    for turn in self.turns:
      entry = turn.as_archive_entry()
      entry['session_id'] = self.session_id
      entry['subject'] = self.subject
      lines.append(json.dumps(entry))
    return '\n'.join(lines)

  def save_to_archive(self, path: str):
    """
    Write transcript to ARCHIVE path.

    CHRONICLE preservation rule: this file is append-only.
    Never delete; never edit. Only add new sessions.
    """
    try:
      with open(path, 'a') as f:
        f.write(self.as_jsonl())
        f.write('\n')
      print(f"Transcript saved to {path}")
    except IOError as e:
      print(f"Failed to save transcript: {e}")

  @staticmethod
  def load_from_archive(path: str) -> List[Transcript]:
    """
    Read transcripts from ARCHIVE path.

    Returns all preserved sessions in chronological order.
    """
    transcripts = {}
    try:
      with open(path, 'r') as f:
        for line in f:
          if not line.strip():
            continue
          entry = json.loads(line)
          session_id = entry.get('session_id')
          if session_id not in transcripts:
            transcripts[session_id] = Transcript(
              session_id=session_id,
              subject=entry.get('subject'),
            )
          turn = Turn(
            speaker=entry['speaker'],
            text=entry['text'],
            timestamp=entry['timestamp'],
            role=entry.get('role'),
            classification=entry.get('classification'),
            uncertainty_map=entry.get('uncertainty_map'),
          )
          transcripts[session_id].turns.append(turn)
      return list(transcripts.values())
    except FileNotFoundError:
      return []


if __name__ == '__main__':
  # Example usage
  t = Transcript(session_id='sess_2026_07_27_001', subject='AGI timeline')

  t.add_turn(
    speaker='human',
    text='Do you think we\'ll have AGI by 2030?',
    role='guide',
  )

  t.add_turn(
    speaker='lens',
    text='That\'s a vision-layer claim. Let me decompose it.',
    role='recorder',
    classification={'category': 'vision', 'evidence_tier': 'speculative'},
  )

  t.add_turn(
    speaker='human',
    text='What would make you more confident?',
    role='challenger',
  )

  t.add_turn(
    speaker='lens',
    text='Evidence that scaling laws hold beyond current benchmarks.',
    role='guide',
  )

  print(t.summary())
  print("\nTranscript as JSONL:")
  print(t.as_jsonl())
