from __future__ import annotations

from typing import Dict

from .emotion_lexicon_zh import INTENSIFIERS, NEGATIVE_WORDS, POSITIVE_WORDS


def score_emotion(text: str) -> Dict[str, int | str | bool]:
    t = (text or "").strip()
    pos = sum(weight for word, weight in POSITIVE_WORDS.items() if word in t)
    neg = sum(weight for word, weight in NEGATIVE_WORDS.items() if word in t)
    boost = sum(weight for word, weight in INTENSIFIERS.items() if word in t)

    if pos == 0 and neg == 0:
        return {
            "matched": False,
            "emotion": "calm",
            "emotion_strength": 1,
            "importance": 2,
            "sentiment": 0,
        }

    sentiment = pos - neg
    base = max(pos, neg)
    strength = min(5, max(1, base + boost))
    importance = min(10, max(3, strength * 2))

    if sentiment > 0:
        emotion = "happy"
    elif sentiment < 0:
        emotion = "angry"
    else:
        emotion = "calm"

    return {
        "matched": True,
        "emotion": emotion,
        "emotion_strength": int(strength),
        "importance": int(importance),
        "sentiment": int(sentiment),
    }
