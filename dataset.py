"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    # --- New posts added (Part 1) ---
    "I absolutely love sitting in traffic for two hours 🙂",   # sarcasm
    "lowkey sad but no cap the sunset was fire today",          # slang + mixed
    "just got an A on my exam!! 😂💀 I can't believe it",       # positive (excited)
    "not gonna lie this food is mid at best",                   # slang + negative
    "I hate Mondays but at least there's coffee ☕",            # mixed
    "bro this is so unfair I'm done 😤",                        # negative
    "feeling blessed and grateful today, life is good 🙏",      # positive
    "honestly don't know how I feel about it",                  # neutral/ambiguous
]

TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    # --- New labels (must match new posts above) ---
    "negative",  # sarcasm — actually negative, but model may read "love" as positive
    "mixed",     # slang with both sad and positive elements
    "positive",  # excited about exam result
    "negative",  # "mid" = mediocre/bad; model likely won't know this slang
    "mixed",     # hate + positive offset
    "negative",  # angry/frustrated
    "positive",  # clearly positive
    "neutral",   # ambiguous — genuinely hard to label
]

# Quick sanity check — will raise an error if lengths don't match
assert len(SAMPLE_POSTS) == len(TRUE_LABELS), (
    f"Mismatch: {len(SAMPLE_POSTS)} posts but {len(TRUE_LABELS)} labels"
)