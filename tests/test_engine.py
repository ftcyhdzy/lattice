import os
import unittest

from engine.analyzer import scan

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMPLES = os.path.join(HERE, "..", "examples")


def _read(name):
    with open(os.path.join(EXAMPLES, name), encoding="utf-8") as fh:
        return fh.read()


class TestEngine(unittest.TestCase):
    def test_vulnerable_contract_has_findings(self):
        findings = scan(_read("vulnerable.sol"))
        ids = {f["rule"] for f in findings}
        for expected in ("LAT-001", "LAT-003", "LAT-006"):
            self.assertIn(expected, ids)
        self.assertGreaterEqual(len(findings), 5)

    def test_safe_contract_has_no_findings(self):
        findings = scan(_read("safe.sol"))
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
