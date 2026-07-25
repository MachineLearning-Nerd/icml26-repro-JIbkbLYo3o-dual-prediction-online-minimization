# Claim 4 — event-prediction instability in caching

**Candidate verdict: VERIFIED for Wei's deterministic combiner.**

The exact BlindOracle-plus-LRU algorithm is run on a parametric version of the
paper's construction. True and anticipated sequences differ at one request.
That replacement affects two next-arrival records—not one scalar prediction—
and leaves a stale page in BlindOracle's cache.

Stage 2 makes LRU strictly better than BlindOracle. During every Stage-3
request, the combined algorithm follows LRU and misses on all `q(k+1)`
requests. Exact Belady OPT and a calibrated `k=4,8,16,32,64` sweep establish
linear ratio growth, hence the claimed `Omega(log k)` collapse.

| Evidence | Result |
|---|---|
| Named algorithm | Wei Theorem 2.1 deterministic combiner |
| Request replacements | Exactly 1 |
| Affected next-arrival records | Exactly 2 |
| Expert tie policies | Both BlindOracle and LRU ties tested |
| Independent checker | No simulator import; PASS |
| Negative control | No replacement gives ratio below 3 |
| Fixed command | `uv run --frozen python repro/src/run_publication_gate.py` |

[Contract](../../.openresearch/artifacts/C4/claim_contract.json) ·
[source audit](../../.openresearch/artifacts/C4/source_audit.md) ·
[method](../../.openresearch/artifacts/C4/method.md) ·
[expected raw result](../../.openresearch/artifacts/C4/raw/expected_result.json) ·
[implementation](../../repro/src/caching_instability.py) ·
[verifier](../../repro/src/verify_claim4_caching.py) ·
[independent checker](../../repro/src/check_claim4_independent.py) ·
[control](../../repro/src/run_claim4_negative_controls.py)

The randomized combiner is not reconstructed, and the source proof's
lower-bound-transfer gap is not hidden.
