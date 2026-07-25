# C1 method

The primary checker validates the exact coefficient substitution and exposes
all five structural obligations. The derivation reconstructs both charging
arguments from the algorithm: maximal Type-1 purchases are pairwise disjoint,
while redundant nested sets can be deleted from an integral optimal cover
before Type-2 charging. Exact positive-part and strong-duality identities then
give the detailed bound.

The independent checker imports no primary code and evaluates the two rational
identities at five exact rational epsilon values. The negative control deletes
the `1/(1-alpha)` miss amplification and must be rejected.

Command: `uv run --frozen python repro/src/run_publication_gate.py`.
Seeds: none. Expected compute: one CPU core, under five minutes.
