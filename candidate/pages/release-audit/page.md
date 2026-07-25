# Release audit

Current candidate is **not yet published**.

| Item | Status |
|---|---|
| Judged Space revision | `ca024e6adeaf755dd21a0b28b642d5a85d6df733` |
| Judge revision | `ca024e6adeaf755dd21a0b28b642d5a85d6df733` |
| Historical file count | 22 |
| Historical paths present in candidate | PASS, 22/22 |
| Protected historical hashes unchanged | PASS, 19/19; only README/logbook/index navigation changed |
| Fixed command | `uv run --frozen python repro/src/run_publication_gate.py` |
| Pinned environment | Python 3.12, `uv.lock`, one repository `.venv` |
| Current verdicts | C1–C4/C6 VERIFIED; C5 BLOCKED |
| Candidate logbook validation | PASS |
| Canonical traversal | PASS, 62 reachable files, zero broken links |
| Evaluator-blind red team | PASS after one repair round and a clean second pass |
| Text upload allowlist and SHA manifest | PASS, 88 text files |
| Secret scan | PASS, zero hits |
| Source payload | PASS, SHA-256 `364d1b1d...077c` |

The experiment tree and exact run identifiers are downloadable in
[`experiment-tree.json`](../../evidence/runs/experiment-tree.json). The two
blind reviews are [pass 1](../../evidence/red-team/pass-1.md) and
[pass 2](../../evidence/red-team/pass-2.md). The exact release inputs are the
[upload allowlist](../../release/upload-allowlist.txt) and
[SHA-256 manifest](../../release/sha256-manifest.json).
