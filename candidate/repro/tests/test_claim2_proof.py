from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "repro" / "src"))

from proof_kernel import CertificateError, check_farkas_certificate, check_structural_obligations


class Claim2ProofTest(unittest.TestCase):
    def setUp(self):
        path = ROOT / ".openresearch" / "artifacts" / "C2" / "proof_certificate.json"
        if not path.exists():
            path = ROOT / "evidence" / "C2" / "proof_certificate.json"
        self.certificate = json.loads(path.read_text())

    def test_exact_certificate(self):
        result = check_farkas_certificate(self.certificate)
        self.assertEqual(result["exact_goal"], "ALG - OPT - ETA <= 0")
        self.assertEqual(check_structural_obligations(self.certificate)["induction_step"], "T -> T+1")

    def test_mutated_goal_is_rejected(self):
        mutated = copy.deepcopy(self.certificate)
        mutated["goal"]["coefficients"]["ETA"] = "-1/2"
        with self.assertRaises(CertificateError):
            check_farkas_certificate(mutated)


if __name__ == "__main__":
    unittest.main()
