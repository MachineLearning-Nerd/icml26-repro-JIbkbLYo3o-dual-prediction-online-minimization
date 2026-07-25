# C1 source audit

Retrieved 2026-07-25 from `https://export.arxiv.org/e-print/2606.05380`
with an explicit OpenResearch browser User-Agent. SHA-256:
`364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c`.

The exact statement is `lem:lemdualboundlaminar` at `main.tex:389-395`.
The informal Theorem 1.1 consequence uses `alpha=1/(1+epsilon)`. Assumptions
are a finite laminar family, nonnegative set costs, an optimal dual, and an
`R`-competitive classical algorithm. The guarantee is in expectation only
over the subroutine/randomized rounding.

The source proof is at `main.tex:907-954`. Its nonnumeric obligations are:
maximal charged laminar sets are disjoint; an optimal integral laminar cover
can be disjointified; complementary slackness and strong LP duality apply; and
the classical subroutine is competitive on the passed subinstance.
