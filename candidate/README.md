---
title: Dual Prediction Online Minimization Reproduction
emoji: 📚
colorFrom: blue
colorTo: indigo
sdk: static
app_file: index.html
pinned: false
---

# Current rigorous verification

This is the canonical entrypoint for the candidate evaluator artifact. Current
verification appears first. The judged finite-check pages are preserved later
under the exact label **Historical rejected baseline**.

- [Illustrated technical report](report.md)
- [Self-contained marimo tutorial](notebooks/dual_prediction_reproduction.py)
- [Current score forecast and visibility matrix](pages/current-summary/page.md)
- [Release and preservation audit](pages/release-audit/page.md)
- [Pinned Python environment](pyproject.toml), [exact lock](uv.lock), and
  [cumulative executable gate](repro/src/run_publication_gate.py)
- [Exact source payload](source/arxiv-2606.05380.base64.txt), verified against
  SHA-256 `364d1b1d...077c` before use
- [Historical rejected baseline](pages/overview/page.md)

## Current claims

- [Claim 1: exact laminar derivation](pages/current-claim-c1/page.md) — candidate
  verdict `VERIFIED`; symbolic charging certificate and rejection control.
- [Claim 2: exact MTS Bellman proof](pages/current-claim-c2/page.md) — candidate
  verdict `VERIFIED`; exact symbolic certificate, independent checker, and
  rejection control.
- [Claim 3: dual stability and primal instability](pages/current-claim-c3/page.md)
  — candidate verdict `VERIFIED`; parametric proof and typo rejection.
- [Claim 4: exact caching instability](pages/current-claim-c4/page.md) —
  candidate verdict `VERIFIED` for Wei's deterministic combiner; one request
  replacement, exact Belady control, and calibrated asymptotic sweep.
- [Claim 5: four-route real-data audit](pages/current-claim-c5/page.md) —
  `BLOCKED`, confidence `LOW`; exact public inputs are identifiable but author
  experiment semantics and processed artifacts are unavailable.
- [Claim 6: corrected general set-cover lower bound](pages/current-claim-c6/page.md)
  — candidate verdict `VERIFIED` in deterministic/adaptive scope; the
  manuscript's defective phase order is rejected.

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| C1 | [Current C1](pages/current-claim-c1/page.md) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |
| C2 | [Current C2](pages/current-claim-c2/page.md) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |
| C3 | [Current C3](pages/current-claim-c3/page.md) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |
| C4 | [Current C4](pages/current-claim-c4/page.md) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |
| C5 | [Current C5](pages/current-claim-c5/page.md) | Yes | Yes | Yes | Yes | Yes | Yes | BLOCKED after four routes |
| C6 | [Current C6](pages/current-claim-c6/page.md) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |

This candidate is not published and is not a new judge result.
