# C5 source audit

The paper source is pinned at SHA-256
`364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c`;
the experiment text is `main.tex:672-720`.

Parking details present: Central Park GHCNd, 1869–2021, 153 instances of 365
days, leave-one-out pointwise mean dual, `D_k=2^k`, `C_k=(2/f)^k`,
`alpha=.5`, and the randomized classical algorithm inside the augmented
procedure.

Missing parking details: rain threshold, leap/missing handling, whether `k`
starts at zero or one in code, interval alignment, exact deterministic and
randomized PPP policies, seeds/repetitions, and confidence-interval estimator.

Bike details present: Manhattan origins, ten equal latitude intervals mapped
to a line, one daily instance, 2023–2024 train and 2025 test, trip and
minute-mode requests, 15-minute dual averaging, `k=2..9`, WFA, and DC.

Missing bike details: Manhattan predicate and latitude endpoints, initial
server configuration, whether colocated servers are allowed, distance scale,
WFA/DC ties, dual-to-request alignment, empty-minute/day handling, seeds, and
processed input hashes. No author code or raw/processed experiment artifact is
linked from the source or publicly discoverable.
