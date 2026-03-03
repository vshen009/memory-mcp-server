from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


class MemoryRateLimiter:
    def __init__(
        self,
        state_path: Path,
        max_per_30m: int = 1,
        max_per_day: int = 5,
    ):
        self.state_path = state_path
        self.max_per_30m = max_per_30m
        self.max_per_day = max_per_day

    def _load(self) -> Dict[str, List[str]]:
        if not self.state_path.exists():
            return {}
        try:
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save(self, state: Dict[str, List[str]]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def allow(self, user_id: str, now: datetime | None = None) -> tuple[bool, str]:
        now = now or datetime.now()
        state = self._load()
        entries = state.get(user_id, [])

        parsed = []
        for t in entries:
            try:
                parsed.append(datetime.fromisoformat(t))
            except Exception:
                continue

        parsed = sorted(parsed)
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        in_day = [t for t in parsed if t >= day_start]
        in_30m = [t for t in parsed if t >= now - timedelta(minutes=30)]

        if len(in_30m) >= self.max_per_30m:
            return False, "rate_limited_30m"
        if len(in_day) >= self.max_per_day:
            return False, "rate_limited_daily"

        in_day.append(now)
        state[user_id] = [t.isoformat() for t in in_day]
        self._save(state)
        return True, "ok"
