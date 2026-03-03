import pathlib
import sys
import unittest

repo_root = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root / "src"))

from memory_mcp_server.emotion_scoring import score_emotion


class EmotionScoringTests(unittest.TestCase):
    def test_positive_phrase(self):
        result = score_emotion("你真棒，老卵")
        self.assertTrue(result["matched"])
        self.assertEqual(result["emotion"], "happy")
        self.assertGreaterEqual(result["emotion_strength"], 3)

    def test_negative_phrase(self):
        result = score_emotion("我很失望，太离谱了")
        self.assertTrue(result["matched"])
        self.assertEqual(result["emotion"], "angry")
        self.assertGreaterEqual(result["importance"], 6)


if __name__ == "__main__":
    unittest.main()
