# Claim 5 — real-data experiments

**Verdict: BLOCKED after four distinct routes. Confidence: LOW.**

No author experiment code, processed input, raw metric, or seed release is
linked from the paper. Public-data availability and agreement between prose
and the paper's own figures do not constitute a rerun.

| Route | Direct result | Why it does or does not resolve the claim |
|---|---|---|
| 1. Source figures | Four embedded PNGs hashed; 1.8x/4.4x prose aligns visually | Circular; not regenerated evidence |
| 2. Full GHCN input | Official Central Park CSV, all 153 named years, threshold/leap audit | Exact PPP policies and rain rule absent |
| 3. Citi Bike manifest | Official 2023–2025 object set and compressed size resolved | Initial states, geographic bounds, ties, dual alignment absent |
| 4. Falsification | No assumption-satisfying counterexample | Alternative guessed pipelines do not contradict the exact unreleased pipeline |

The promotion control deliberately tries to call figure consistency
`VERIFIED`; it is rejected because author code, processed hashes, exact initial
states, seeds, and regenerated metrics are all absent.

[Contract](../../.openresearch/artifacts/C5/claim_contract.json) ·
[source audit](../../.openresearch/artifacts/C5/source_audit.md) ·
[method](../../.openresearch/artifacts/C5/method.md) ·
[expected raw result](../../.openresearch/artifacts/C5/raw/expected_result.json) ·
[four-route verifier](../../repro/src/audit_claim5_real_data.py) ·
[independent checker](../../repro/src/check_claim5_independent.py) ·
[control](../../repro/src/run_claim5_negative_control.py)

Fixed command: `uv run --frozen python repro/src/run_publication_gate.py`.
Compute: Hugging Face `cpu-upgrade`, CPU only; actual allocation and runtime
are recorded in raw output.
