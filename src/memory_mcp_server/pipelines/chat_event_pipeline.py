from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from ..emotion_scoring import score_emotion
from ..rate_limit import MemoryRateLimiter
from ..schemas import EpisodicPayload, PreferencePayload


class ChatEventPipeline:
    def __init__(self, state_dir: Optional[Path] = None):
        base = state_dir or (Path.home() / ".openclaw" / "workspace" / "generated" / "tmp")
        self.limiter = MemoryRateLimiter(base / "memory-chat-rate-limit.json")

    def build_records(
        self,
        text: str,
        user_id: str,
        location: str = "chat",
        actors: Optional[list[str]] = None,
    ) -> Dict[str, Any]:
        scored = score_emotion(text)
        if not scored["matched"]:
            return {"should_store": False, "reason": "no_strong_emotion"}

        ok, reason = self.limiter.allow(user_id=user_id)
        if not ok:
            return {"should_store": False, "reason": reason}

        now = datetime.now().isoformat()
        actors = actors or ["user", "assistant"]
        eid = f"epi-{uuid4().hex[:12]}"

        episodic = EpisodicPayload(
            memory_id=eid,
            type="episodic",
            timestamp=now,
            location=location,
            actors=actors,
            event=text,
            emotion=scored["emotion"],
            emotion_strength=int(scored["emotion_strength"]),
            importance=int(scored["importance"]),
            summary=text[:140],
        )

        attitude = "like" if scored["sentiment"] > 0 else "dislike"
        preference = PreferencePayload(
            memory_id=f"pref-{uuid4().hex[:12]}",
            type="preference",
            target="沟通方式",
            attitude=attitude,
            strength=min(5, int(scored["emotion_strength"])),
            trigger_count=1,
            update_time=now,
            content=text[:200],
        )

        return {
            "should_store": True,
            "episodic": episodic.to_dict(),
            "preference": preference.to_dict(),
        }

    @staticmethod
    def to_text(payload: Dict[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False)
