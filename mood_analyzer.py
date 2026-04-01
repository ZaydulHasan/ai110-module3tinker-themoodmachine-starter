# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.
"""

import re
from typing import List, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


# Slang/emoji signal tables (used in score_text)
POSITIVE_SLANG = {"fire", "lit", "goated", "blessed", "valid", "lowkey", "highkey", "bussin", "W"}
NEGATIVE_SLANG = {"mid", "trash", "cringe", "L", "cooked", "rip", "yikes", "smh"}

POSITIVE_EMOJIS = {"😊", "😄", "😍", "🥰", "🎉", "🙌", "💪", "🔥", "✨", "🙏", "❤️", ":)", ":D"}
NEGATIVE_EMOJIS = {"😢", "😭", "😤", "😠", "💀", "😒", "😞", ":(", ":-(", "😩", "😫"}

NEGATION_WORDS = {"not", "never", "no", "don't", "doesn't", "didn't", "isn't", "wasn't", "can't", "won't"}


class MoodAnalyzer:
    """A rule-based mood classifier with negation, slang, and emoji support."""

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ------------------------------------------------------------------
    # Preprocessing
    # ------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens.

        Steps:
          1. Lowercase and strip whitespace.
          2. Extract emoji characters before removing punctuation
             (so emojis stay as their own tokens).
          3. Strip punctuation from word tokens (but keep emoji tokens).
        """
        text = text.strip().lower()

        tokens = []
        for word in text.split():
            # Keep known emoji strings as-is
            if word in POSITIVE_EMOJIS or word in NEGATIVE_EMOJIS:
                tokens.append(word)
            else:
                # Strip punctuation from regular words
                cleaned = re.sub(r"[^\w]", "", word)
                if cleaned:
                    tokens.append(cleaned)

        return tokens

    # ------------------------------------------------------------------
    # Scoring logic
    # ------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric mood score for the given text.

        Rules:
          - Positive word  → +1
          - Negative word  → -1
          - Positive slang → +1
          - Negative slang → -1
          - Positive emoji → +2  (stronger signal)
          - Negative emoji → -2  (stronger signal)
          - Negation word followed by a positive word → flips to -1
          - Negation word followed by a negative word → flips to +1
        """
        tokens = self.preprocess(text)
        score = 0
        skip_next = False  # used when we handle a negation pair

        for i, token in enumerate(tokens):
            if skip_next:
                skip_next = False
                continue

            # Check if this token is a negation word
            if token in NEGATION_WORDS and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token in self.positive_words or next_token in POSITIVE_SLANG:
                    score -= 1   # "not happy" → negative
                elif next_token in self.negative_words or next_token in NEGATIVE_SLANG:
                    score += 1   # "not bad" → slightly positive
                skip_next = True
                continue

            # Regular word scoring
            if token in self.positive_words:
                score += 1
            elif token in self.negative_words:
                score -= 1
            elif token in POSITIVE_SLANG:
                score += 1
            elif token in NEGATIVE_SLANG:
                score -= 1

            # Emoji scoring (stronger weight)
            if token in POSITIVE_EMOJIS:
                score += 2
            elif token in NEGATIVE_EMOJIS:
                score -= 2

        return score

    # ------------------------------------------------------------------
    # Label prediction
    # ------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Map the numeric score to a mood label.

        Thresholds (tuned for short social-media-style posts):
          score >=  2  → "positive"
          score <= -2  → "negative"
          score ==  1  → "mixed"   (weak positive signal, could go either way)
          score == -1  → "mixed"   (weak negative signal, could go either way)
          score ==  0  → "neutral"
        """
        score = self.score_text(text)

        if score >= 1:
            return "positive"
        elif score <= -1:
            return "negative"
        else:
            return "neutral"

    # ------------------------------------------------------------------
    # Explanation
    # ------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """Return a human-readable breakdown of how the score was calculated."""
        tokens = self.preprocess(text)
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0
        skip_next = False

        for i, token in enumerate(tokens):
            if skip_next:
                skip_next = False
                continue

            if token in NEGATION_WORDS and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token in self.positive_words or next_token in POSITIVE_SLANG:
                    negative_hits.append(f"not {next_token}")
                    score -= 1
                elif next_token in self.negative_words or next_token in NEGATIVE_SLANG:
                    positive_hits.append(f"not {next_token}")
                    score += 1
                skip_next = True
                continue

            if token in self.positive_words or token in POSITIVE_SLANG:
                positive_hits.append(token)
                score += 1
            elif token in self.negative_words or token in NEGATIVE_SLANG:
                negative_hits.append(token)
                score -= 1

            if token in POSITIVE_EMOJIS:
                positive_hits.append(token)
                score += 2
            elif token in NEGATIVE_EMOJIS:
                negative_hits.append(token)
                score -= 2

        label = self.predict_label(text)
        return (
            f"Score = {score} → '{label}' | "
            f"positive signals: {positive_hits or []} | "
            f"negative signals: {negative_hits or []}"
        )