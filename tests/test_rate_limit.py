import importlib.util
import pathlib
import tempfile
import unittest
from datetime import datetime, timedelta


def load_rate_limiter_class():
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    module_path = repo_root / "src" / "memory_mcp_server" / "rate_limit.py"
    spec = importlib.util.spec_from_file_location("rate_limit_for_test", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.MemoryRateLimiter


MemoryRateLimiter = load_rate_limiter_class()


class RateLimitTests(unittest.TestCase):
    def test_30m_limit(self):
        with tempfile.TemporaryDirectory() as d:
            limiter = MemoryRateLimiter(pathlib.Path(d) / "state.json", max_per_30m=1, max_per_day=5)
            now = datetime(2026, 3, 3, 10, 0, 0)
            ok, reason = limiter.allow("u1", now=now)
            self.assertTrue(ok)
            self.assertEqual(reason, "ok")

            ok2, reason2 = limiter.allow("u1", now=now + timedelta(minutes=5))
            self.assertFalse(ok2)
            self.assertEqual(reason2, "rate_limited_30m")

    def test_daily_limit(self):
        with tempfile.TemporaryDirectory() as d:
            limiter = MemoryRateLimiter(pathlib.Path(d) / "state.json", max_per_30m=10, max_per_day=2)
            now = datetime(2026, 3, 3, 9, 0, 0)
            self.assertTrue(limiter.allow("u1", now=now)[0])
            self.assertTrue(limiter.allow("u1", now=now + timedelta(hours=1))[0])
            ok, reason = limiter.allow("u1", now=now + timedelta(hours=2))
            self.assertFalse(ok)
            self.assertEqual(reason, "rate_limited_daily")


if __name__ == "__main__":
    unittest.main()
