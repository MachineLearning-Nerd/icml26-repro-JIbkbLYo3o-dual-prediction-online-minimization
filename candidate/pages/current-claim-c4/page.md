# Claim 4 — event-prediction instability in caching

**Candidate verdict: VERIFIED for Wei's deterministic combiner.**

The exact BlindOracle-plus-LRU algorithm is run on a parametric version of the
paper's construction. True and anticipated sequences differ at one request.
That replacement affects two next-arrival records—not one scalar prediction—
and leaves a stale page in BlindOracle's cache.

Stage 2 makes LRU strictly better than BlindOracle. During every Stage-3
request, the combined algorithm follows LRU and incurs at least
`q(k+1)-k` evictions; the subtraction accounts for the warm-start cache.
Exact Belady OPT and a calibrated `k=4,8,16,32,64` sweep establish linear
ratio growth, hence the claimed `Omega(log k)` collapse.

| Evidence | Result |
|---|---|
| Named algorithm | Wei Theorem 2.1 deterministic combiner |
| Request replacements | Exactly 1 |
| Affected next-arrival records | Exactly 2 |
| Expert tie policies | Both BlindOracle and LRU ties tested |
| Independent checker | No simulator import; PASS |
| Negative control | No replacement gives ratio below 3 |
| Seeds | None; deterministic construction |
| Fixed command | `uv run --frozen python repro/src/run_publication_gate.py` |

| k | Ratio, BlindOracle tie | Ratio, LRU tie | Stage-3 evictions |
|---:|---:|---:|---:|
| 4 | 3.950 | 3.925 | 156 |
| 8 | 7.833 | 7.806 | 280 |
| 16 | 15.588 | 15.559 | 528 |
| 32 | 31.091 | 31.061 | 1024 |
| 64 | 61.152 | 61.121 | 2016 |

Run `6da5d53f-ecc3-4435-9102-1c226a9f1ec5`, Git
`a9bc4eec49b5c25aa5e88f452f6c85c5ac4e58f3`, local estimated one core,
runtime 1.378 seconds. The last-three minimum ratio divided by `k` is `0.95549`.

[Contract](../../evidence/C4/claim_contract.json) ·
[source audit](../../evidence/C4/source_audit.md) ·
[method](../../evidence/C4/method.md) ·
[evaluation record](../../evidence/C4/EVAL.md) ·
[raw result](../../evidence/runs/C4-caching.json) ·
[implementation](../../repro/src/caching_instability.py) ·
[verifier](../../repro/src/verify_claim4_caching.py) ·
[independent checker](../../repro/src/check_claim4_independent.py) ·
[control](../../repro/src/run_claim4_negative_controls.py)

Limitation: the randomized combiner is not reconstructed, and the source proof's
lower-bound-transfer gap is not hidden.
