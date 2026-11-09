"""Run the checked-in Serbian AI-style seed corpus in CI, not only unittest fixtures."""
import json
import unittest
from pathlib import Path

from scripts.check import review

CASES = Path(__file__).resolve().parents[1] / "evals" / "serbian_ai_style_seed.jsonl"


class SerbianAiStyleSeedEvals(unittest.TestCase):
    def test_seed_corpus(self):
        seen = set()
        for raw in CASES.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            case = json.loads(raw)
            self.assertNotIn(case["id"], seen, "duplicate case id")
            seen.add(case["id"])
            expected = set(case["expected"])
            findings = review(case["text"], experimental=True)
            actual = {f.rule_id for f in findings}
            with self.subTest(case=case["id"]):
                allowed_extra = set(case.get("allowed_extra", []))
                self.assertTrue(
                    expected <= actual,
                    f"missing expected signal(s): {sorted(expected - actual)}",
                )
                self.assertEqual(
                    actual - expected - allowed_extra, set(),
                    "unexpected extra finding(s) in seed evaluation",
                )
        self.assertGreaterEqual(len(seen), 11)


if __name__ == "__main__":
    unittest.main()
