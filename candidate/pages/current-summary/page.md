# Current reproduction summary

- Previous live judged score: `5/12`
- Conservative projected score range after the proposed change: `8/12–10/12`
- Best-supported possible new score: **`10/12` forecast, not a judge result**

The live score remains `5/12`. Five universal/theoretical claims now have
proof-level or parametric evidence; the real-data claim is `BLOCKED` after four
routes. Only the live evaluator can award points.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| C1 | 1 | 2 | HIGH | VERIFIED | Exact charging derivation and controls; randomized rounding lemma remains source-stated |
| C2 | 1 | 2 | HIGH | VERIFIED | Exact rational proof certificate and independent reconstruction |
| C3 | 1 | 2 | MEDIUM | VERIFIED | Exact proof cone and parametric primal family; appendix has an exposed alpha/beta typo |
| C4 | 1 | 2 | HIGH | VERIFIED | Exact Wei deterministic combiner, calibrated asymptotic sweep, Belady control |
| C5 | 0 | 0 | LOW | BLOCKED | Four routes complete; author code, processed inputs, initial states, ties, and seeds unavailable |
| C6 | 1 | 2 | HIGH | VERIFIED | Corrected assumption-preserving adversary; printed H_m-1 proof is rejected |

Current total score: `5/12`. Conservative projected total: `8/12–10/12`.
Best-supported possible total: `10/12`, forecast only. C1, C2, C3, C4, and C6
changed from finite toy evidence to current verification. C5 changed from an
unattempted/no-data note to a four-route `BLOCKED` audit but remains worth zero
forecast points.

## Visibility matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| C1 | [Current C1](#/current-claim-c1) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |
| C2 | [Current C2](#/current-claim-c2) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |
| C3 | [Current C3](#/current-claim-c3) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |
| C4 | [Current C4](#/current-claim-c4) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |
| C5 | [Current C5](#/current-claim-c5) | Yes | Yes | Yes | Yes | Yes | Yes | BLOCKED after four routes |
| C6 | [Current C6](#/current-claim-c6) | Yes | Yes | Yes | Yes | Yes | Yes | VERIFIED candidate |

The exact publication action, after every remaining release gate passes, is a
text-only upload to the existing Space `DineshAI/JIbkbLYo3o`, followed by a
download/hash/traversal check and a GitHub `main` mirror. No second Space will
be created.
