"""Primary fail-closed verifier for the exact Claim 2 proof certificate."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from proof_kernel import check_farkas_certificate, check_structural_obligations


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / ".openresearch" / "artifacts" / "C2"
SOURCE = ROOT / "source" / "arxiv-2606.05380.tar"
SOURCE_SHA256 = "364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c"


def main() -> None:
    contract = json.loads((ARTIFACT / "claim_contract.json").read_text())
    certificate = json.loads((ARTIFACT / "proof_certificate.json").read_text())
    expected = json.loads((ARTIFACT / "raw" / "expected_result.json").read_text())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256
    assert contract["additive_conclusion"] == "ALG <= OPT + eta"
    assert contract["ratio_conclusion"].endswith("when OPT > 0")
    assert expected["verdict"] == "VERIFIED"

    linear = check_farkas_certificate(certificate)
    structural = check_structural_obligations(certificate)
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()
    result = {
        "claim_id": "C2",
        "verdict": "VERIFIED",
        "source_sha256": SOURCE_SHA256,
        "git_sha": commit,
        "proof_kind": expected["proof_kind"],
        "linear_certificate": linear,
        "structural_certificate": structural,
        "ratio_scope": "OPT > 0",
    }
    output = ROOT / "outputs" / "claim2_proof_verification.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
