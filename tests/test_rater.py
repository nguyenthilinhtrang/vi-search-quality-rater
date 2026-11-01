import os
import unittest

from rater.agreement import cohen_kappa, needs_met_report, pairwise_report
from rater.checks import load, validate

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


class TestKappa(unittest.TestCase):
    def test_perfect(self):
        self.assertAlmostEqual(cohen_kappa(["a", "b", "a"], ["a", "b", "a"]), 1.0)

    def test_chance(self):
        self.assertAlmostEqual(cohen_kappa(["a", "a", "b", "b"], ["a", "b", "a", "b"]), 0.0)

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            cohen_kappa(["a"], ["a", "b"])


class TestValidate(unittest.TestCase):
    def base(self, **kw):
        row = {"task_id": "X", "rater": "r", "query": "q", "query_type": "know",
               "topic": "food", "result": "page", "needs_met": "HM",
               "page_quality": "Medium", "rationale": "clear recipe most users can follow"}
        row.update(kw)
        return row

    def test_clean_row(self):
        self.assertEqual(validate([self.base()]), [])

    def test_fullym_on_broad_query(self):
        issues = validate([self.base(needs_met="FullyM")])
        self.assertTrue(any("FullyM" in i[3] for i in issues))

    def test_ymyl_low_quality_high_rating(self):
        issues = validate([self.base(topic="health", page_quality="Low")])
        self.assertTrue(any("YMYL" in i[3] for i in issues))

    def test_unknown_label(self):
        issues = validate([self.base(needs_met="Great")])
        self.assertEqual(issues[0][2], "error")


class TestSampleData(unittest.TestCase):
    def test_sample_ratings_have_no_errors(self):
        issues = validate(load(os.path.join(DATA, "sample_ratings.csv")))
        self.assertFalse([i for i in issues if i[2] == "error"])

    def test_agreement_report(self):
        r = needs_met_report(load(os.path.join(DATA, "sample_ratings.csv")))
        self.assertEqual(r["tasks"], 8)
        self.assertTrue(0 < r["kappa"] < 1)

    def test_pairwise_report(self):
        r = pairwise_report(load(os.path.join(DATA, "sample_pairwise.csv")))
        self.assertEqual(r["judgements"], 12)
        self.assertFalse(r["position_bias_flag"])


if __name__ == "__main__":
    unittest.main()
