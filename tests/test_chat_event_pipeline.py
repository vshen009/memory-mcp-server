import pathlib
import sys
import tempfile
import unittest


repo_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root / "src"))

from memory_mcp_server.pipelines import ChatEventPipeline  # noqa: E402


class ChatEventPipelineTests(unittest.TestCase):
    def test_build_records_positive(self):
        with tempfile.TemporaryDirectory() as d:
            p = ChatEventPipeline(state_dir=pathlib.Path(d))
            out = p.build_records(
                text="你真棒，老卵",
                user_id="vincent-main",
                location="telegram",
                actors=["Vincent", "Trinity"],
            )
            self.assertTrue(out["should_store"])
            self.assertEqual(out["episodic"]["type"], "episodic")
            self.assertEqual(out["preference"]["type"], "preference")

    def test_build_records_rate_limited(self):
        with tempfile.TemporaryDirectory() as d:
            p = ChatEventPipeline(state_dir=pathlib.Path(d))
            first = p.build_records(text="你真棒", user_id="vincent-main")
            second = p.build_records(text="你也真棒", user_id="vincent-main")
            self.assertTrue(first["should_store"])
            self.assertFalse(second["should_store"])
            self.assertEqual(second["reason"], "rate_limited_30m")


if __name__ == "__main__":
    unittest.main()
