from django.test import TestCase
from .scoring import urgency_score, effort_score, analyze

class ScoringTests(TestCase):

    def test_urgency_basic(self):
        """Urgency should be <= 100"""
        self.assertTrue(urgency_score("2030-01-01") <= 100)

    def test_effort_inverse(self):
        """High-effort tasks should have lower effort score."""
        self.assertTrue(effort_score(1) > effort_score(20))

    def test_analyze_output(self):
        """Analyzer should return results list."""
        tasks = [
            {"id": "T1", "title": "Test", "importance": 7},
            {"id": "T2", "title": "Test2", "importance": 3}
        ]
        result = analyze(tasks)
        self.assertEqual(len(result["results"]), 2)

    def test_strategy_variation(self):
        """Different strategies should produce different scores."""
        tasks = [{"id": "A", "title": "A", "importance": 8}]
        score_smart = analyze(tasks, "smart")["results"][0]["score"]
        score_impact = analyze(tasks, "impact")["results"][0]["score"]
        self.assertNotEqual(score_smart, score_impact)
