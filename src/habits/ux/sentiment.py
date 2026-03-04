"""Sentiment analysis (lightweight, offline).

A small lexicon-based approach is used intentionally:
    - No heavy ML dependencies are required
    - Behavior is deterministic and testable
    - UX feedback can be demonstrated in a simple CLI
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


POSITIVE_WORDS = {
    "good", "great", "awesome", "nice", "happy", "proud", "strong",
    "progress", "improved", "better", "love", "motivated", "energized",
    "easy", "done", "win",
}

NEGATIVE_WORDS = {
    "bad", "sad", "tired", "exhausted", "hard", "stressed", "stress",
    "angry", "upset", "failed", "fail", "pain", "sick", "burned",
    "overwhelmed", "lazy", "worried",
}


@dataclass(frozen=True)
class SentimentResult:
    """Sentiment scoring output."""
    score: float
    label: str


def _tokenize(text: str) -> list[str]:
    # Minimal tokenization is applied for deterministic behavior.
    return [t.strip(".,!?;:()[]{}\"'").lower() for t in text.split() if t.strip()]


def score_sentiment(note: Optional[str]) -> SentimentResult:
    """Compute a sentiment score for a note.

    If note is empty, a neutral result is returned.
    """
    if not note or not note.strip():
        return SentimentResult(score=0.0, label="neutral")

    tokens = _tokenize(note)
    pos = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg = sum(1 for t in tokens if t in NEGATIVE_WORDS)

    if pos == 0 and neg == 0:
        return SentimentResult(score=0.0, label="neutral")

    score = (pos - neg) / float(pos + neg)

    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    return SentimentResult(score=score, label=label)


def feedback_message(sentiment: SentimentResult) -> str:
    """Convert a sentiment label into a UX-friendly feedback message."""
    if sentiment.label == "positive":
        return "Nice! Your note sounds positive — keep that momentum going."
    if sentiment.label == "negative":
        return "I hear you. Even small steps count — be kind to yourself today."
    return "Good job showing up. Consistency beats intensity."
