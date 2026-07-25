# Claim 5 — real-data experiments

**Verdict: BLOCKED after four distinct routes. Confidence: LOW.**

No author experiment code, processed input, raw metric, or seed release is
linked from the paper. Public-data availability and agreement between prose
and the paper's own figures do not constitute a rerun.

| Route | Direct result | Why it does or does not resolve the claim |
|---|---|---|
| 1. Source figures | Four embedded PNGs hashed; 1.8x/4.4x prose aligns visually | Circular; not regenerated evidence |
| 2. Full GHCN input | Official Central Park CSV, all 153 named years, raw 0/10/25 tenths-mm threshold and leap audit | Exact PPP policies and rain rule absent |
| 3. Citi Bike manifest | Official 2023–2025 object set and compressed size resolved | Initial states, geographic bounds, ties, dual alignment absent |
| 4. Falsification | No assumption-satisfying counterexample | Alternative guessed pipelines do not contradict the exact unreleased pipeline |

The promotion control deliberately tries to call figure consistency
`VERIFIED`; it is rejected because author code, processed hashes, exact initial
states, seeds, and regenerated metrics are all absent.

The corrected GHCN audit found 153/153 complete 365-day years, zero missing
precipitation cells, and respectively 18,550, 14,222, and 11,361 rainy days at
thresholds above 0, 1, and 2.5 mm. The official Citi Bike manifest contains 25
archives totaling 19,198,058,834 compressed bytes. Run
`8176b956-5948-4227-85e8-b8c42121a706`, Git
`8c8949291acf450afacf5dc4645d630af470b199`, HF `cpu-upgrade`, estimated two
cores, 64 visible logical CPUs, 2.365 seconds for the audit.

[Contract](../../evidence/C5/claim_contract.json) ·
[source audit](../../evidence/C5/source_audit.md) ·
[method](../../evidence/C5/method.md) ·
[evaluation record](../../evidence/C5/EVAL.md) ·
[raw result](../../evidence/runs/C5-real-data-audit.json) ·
[four-route verifier](../../repro/src/audit_claim5_real_data.py) ·
[independent checker](../../repro/src/check_claim5_independent.py) ·
[control](../../repro/src/run_claim5_negative_control.py)

Fixed command: `uv run --frozen python repro/src/run_publication_gate.py`.
Compute: Hugging Face `cpu-upgrade`, CPU only; actual allocation and runtime
are recorded in raw output. Seeds: none were released or inferred.

Limitation: this is a source and primary-input audit, not a rerun of the
unreleased experiment.
