from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class CertificateTest(unittest.TestCase):
    def test_all_five_anchors(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "certificate.json"
            subprocess.run([sys.executable, "repro/src/verify_dual_predictions.py", "--output", str(output)], cwd=ROOT, check=True)
            result = json.loads(output.read_text())
        self.assertEqual(result["verified_claims"], 5)
        self.assertEqual(set(result["claims"]), {"C1", "C2", "C3", "C4", "C6"})


if __name__ == "__main__":
    unittest.main()
