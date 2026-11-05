import unittest
from eval_forge import evaluate, run

class EvaluationTests(unittest.TestCase):
    def test_boolean_is_not_number(self):
        self.assertFalse(evaluate({"id": "a", "output": '{"n": true}', "json_types": {"n": "number"}})["passed"])

    def test_invalid_json_and_missing_key(self):
        for value in ["broken", "{}", "[]"]:
            self.assertFalse(evaluate({"id": "a", "output": value, "json_types": {"n": "number"}})["passed"])

    def test_mixed_report(self):
        report = run([{"id": "a", "output": "yes", "expected": "yes"}, {"id": "b", "output": "bad", "forbidden": ["bad"]}])
        self.assertEqual(report["pass_rate"], .5)

    def test_reject_vacuous_evaluation(self):
        with self.assertRaises(ValueError):
            run([])
        with self.assertRaises(ValueError):
            evaluate({"id": "a", "output": "a"})
        with self.assertRaises(ValueError):
            run([{"id": "a"}, {"id": "a"}])
