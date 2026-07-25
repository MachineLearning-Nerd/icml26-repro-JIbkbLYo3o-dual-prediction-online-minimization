# Tests and gate


---
<!-- trackio-cell
{"type": "code", "id": "cell_a7a9dfdfccdc", "created_at": "2026-07-22T12:53:30+00:00", "title": "Run publication gate", "command": [".venv/bin/python", "repro/src/run_publication_gate.py"], "exit_code": 0, "duration_s": 0.21}
-->
````bash
$ .venv/bin/python repro/src/run_publication_gate.py
````

exit 0 · 0.2s


````python title=run_publication_gate.py
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
subprocess.run([sys.executable, "repro/src/verify_dual_predictions.py", "--output", "outputs/verification.json"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"], cwd=ROOT, check=True)
v = json.loads((ROOT / "outputs/verification.json").read_text())
assert v["verified_claims"] == 5 and v["falsified_claims"] == 0
gate = {"paper": "JIbkbLYo3o", "gate": "passed", "tests_passed": True, "publication_gate_passed": True, "verified_claims": 5, "scope": v["scope"]}
(ROOT / "outputs/publication_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
print(json.dumps(gate, indent=2))

````


````output
{
  "paper": "JIbkbLYo3o",
  "source_sha256": "364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c",
  "scope": "Source-pinned theorem contract plus finite exact MTS, laminar-dual, instability, and harmonic certificates; not a new proof or a rerun of unreleased real-data experiments.",
  "claims": {
    "C1": {
      "status": "verified",
      "explicit_bound_cells": 36
    },
    "C2": {
      "status": "verified",
      "cells": 80,
      "max_nonnegative_slack": 9.55685492370337
    },
    "C3": {
      "status": "verified",
      "stability_cells": 102,
      "beta": 1
    },
    "C4": {
      "status": "verified",
      "primal_instability_sizes": 20,
      "largest_ratio": 24.0,
      "stale_page_control_rejected": true
    },
    "C6": {
      "status": "verified",
      "harmonic_cells": 31,
      "h_32": 4.05849519543652
    }
  },
  "verified_claims": 5,
  "falsified_claims": 0
}
test_all_five_anchors (test_certificate.CertificateTest.test_all_five_anchors) ... {
  "paper": "JIbkbLYo3o",
  "source_sha256": "364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c",
  "scope": "Source-pinned theorem contract plus finite exact MTS, laminar-dual, instability, and harmonic certificates; not a new proof or a rerun of unreleased real-data experiments.",
  "claims": {
    "C1": {
      "status": "verified",
      "explicit_bound_cells": 36
    },
    "C2": {
      "status": "verified",
      "cells": 80,
      "max_nonnegative_slack": 9.55685492370337
    },
    "C3": {
      "status": "verified",
      "stability_cells": 102,
      "beta": 1
    },
    "C4": {
      "status": "verified",
      "primal_instability_sizes": 20,
      "largest_ratio": 24.0,
      "stale_page_control_rejected": true
    },
    "C6": {
      "status": "verified",
      "harmonic_cells": 31,
      "h_32": 4.05849519543652
    }
  },
  "verified_claims": 5,
  "falsified_claims": 0
}
ok

----------------------------------------------------------------------
Ran 1 test in 0.057s

OK
{
  "paper": "JIbkbLYo3o",
  "gate": "passed",
  "tests_passed": true,
  "publication_gate_passed": true,
  "verified_claims": 5,
  "scope": "Source-pinned theorem contract plus finite exact MTS, laminar-dual, instability, and harmonic certificates; not a new proof or a rerun of unreleased real-data experiments."
}

````
