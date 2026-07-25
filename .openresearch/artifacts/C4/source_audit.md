# C4 source audit

The target lemma is `main.tex:792-805`, source SHA
`364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c`.
It replaces the final Stage-1 request `1` by `2`, then uses long stages over
nearby page sets.

The named algorithm was audited against Alexander Wei's official LIPIcs paper,
downloaded 2026-07-25 with an explicit User-Agent. PDF SHA-256:
`1fe5b1c188d73a9c34ea744b9d5e55482437a3549429c4aedd2dde8d1b39a5c2`.
Wei defines BlindOracle as evicting the cached request with furthest predicted
next arrival, and describes the deterministic Theorem 2.1 combiner as
simulating both experts and evicting a page absent from the currently
better-performing expert's cache.

The manuscript's prose alone has a gap: Wei's combiner theorem is an upper
bound relative to the better expert; it does not automatically transfer an
expert's lower bound to the combiner. The current evidence closes that gap by
executing the combiner itself and proving it remains on LRU throughout Stage 3.

One request replacement affects two next-arrival prediction records (the old
page-1 request and the earlier page-2 request). The candidate page says this
explicitly; “one incorrect scalar prediction” would be false for this family.
