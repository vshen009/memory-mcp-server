from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Literal

Scope = Literal["agent-profile", "agent-projects", "episodic", "preference"]


@dataclass
class EpisodicPayload:
    memory_id: str
    type: Literal["episodic"]
    timestamp: str
    location: str
    actors: List[str]
    event: str
    emotion: Literal["happy", "sad", "angry", "calm", "afraid"]
    emotion_strength: int  # 0-5
    importance: int  # 0-10
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PreferencePayload:
    memory_id: str
    type: Literal["preference"]
    target: str
    attitude: Literal["like", "dislike", "neutral"]
    strength: int  # 0-5
    trigger_count: int
    update_time: str
    content: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def now_iso() -> str:
    return datetime.now().isoformat()
