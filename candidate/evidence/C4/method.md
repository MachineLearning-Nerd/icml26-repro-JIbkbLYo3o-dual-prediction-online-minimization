# C4 method

The implementation follows Wei's deterministic algorithm exactly: BlindOracle
and LRU are simulated, costs are measured as evictions, and the combined cache
evicts a page outside the lower-cost expert's cache. Both expert tie choices
are tested.

For cache size `k` and `q` Stage-3 cycles, Stage 2 contains `kq` cycles. The
single replacement leaves page 1 in BlindOracle with a next-arrival time in
the past. Stage 2 creates enough BlindOracle cost debt that LRU is strictly
the lower-cost expert for every Stage-3 request. After at most `k` warm-start
hits, the combined cache follows LRU and incurs at least `q(k+1)-k` evictions.
Belady's exact offline
algorithm computes OPT. A calibrated sweep at `k=4,8,16,32,64` tests growth
without selecting horizons from the claimed ratio formula.

The independent checker imports no simulator and validates raw trace
invariants and normalized scaling. The negative control makes anticipated and
true sequences identical; the stale page and collapse must disappear.

Fixed command: `uv run --frozen python repro/src/run_publication_gate.py`.
Seeds: none. Expected compute: one core, under five minutes.
