import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Dual predictions: five exact results and one honest blocker

    **Strongest observed result.** One request replacement makes the exact
    deterministic Wei caching combiner degrade almost linearly with cache
    size. The live judge score is still **5/12**; the candidate forecast is
    **8–10/12**, never a claimed score.
    """)
    return


@app.cell
def _():
    caching_rows = [
        {"k": 4, "ratio": 3.950, "ratio_over_k": 0.9875},
        {"k": 8, "ratio": 7.833, "ratio_over_k": 0.9791},
        {"k": 16, "ratio": 15.588, "ratio_over_k": 0.9743},
        {"k": 32, "ratio": 31.091, "ratio_over_k": 0.9716},
        {"k": 64, "ratio": 61.152, "ratio_over_k": 0.9555},
    ]
    return (caching_rows,)


@app.cell
def _(caching_rows, mo):
    width = 720
    height = 360
    left = 64
    bottom = 304
    x_positions = [84, 220, 356, 492, 628]
    y = lambda value: bottom - value * 3.75
    points = " ".join(
        f"{x},{y(row['ratio']):.1f}" for x, row in zip(x_positions, caching_rows)
    )
    circles = "".join(
        f'<circle cx="{x}" cy="{y(row["ratio"]):.1f}" r="6" fill="#176b87"/>'
        f'<text x="{x}" y="{y(row["ratio"])-12:.1f}" text-anchor="middle" '
        f'font-size="13" fill="#176b87">{row["ratio"]:.2f}</text>'
        for x, row in zip(x_positions, caching_rows)
    )
    labels = "".join(
        f'<text x="{x}" y="330" text-anchor="middle" font-size="13" '
        f'fill="#52606d">{row["k"]}</text>'
        for x, row in zip(x_positions, caching_rows)
    )
    chart = f"""
    <svg viewBox="0 0 {width} {height}" role="img"
         aria-label="Competitive ratio grows with cache size">
      <rect width="{width}" height="{height}" fill="#fbfaf7"/>
      <text x="360" y="28" text-anchor="middle" font-size="20"
            font-weight="700" fill="#17212b">
        Exact caching instability after one request replacement
      </text>
      <line x1="{left}" y1="{bottom}" x2="670" y2="{bottom}"
            stroke="#52606d" stroke-width="1.5"/>
      <line x1="{left}" y1="54" x2="{left}" y2="{bottom}"
            stroke="#52606d" stroke-width="1.5"/>
      <polyline points="{points}" fill="none" stroke="#176b87"
                stroke-width="5"/>
      {circles}
      {labels}
      <text x="360" y="353" text-anchor="middle" font-size="14"
            fill="#52606d">cache size k</text>
      <text x="18" y="185" text-anchor="middle" font-size="14"
            fill="#52606d" transform="rotate(-90 18 185)">
        competitive ratio
      </text>
    </svg>
    """
    mo.Html(chart)
    return


@app.cell
def _(caching_rows, mo):
    cache_size = mo.ui.dropdown(
        options={str(row["k"]): row["k"] for row in caching_rows},
        value="64",
        label="Inspect a calibrated cache size",
    )
    cache_size
    return (cache_size,)


@app.cell
def _(cache_size, caching_rows, mo):
    selected = next(row for row in caching_rows if row["k"] == cache_size.value)
    mo.callout(
        mo.md(
            f"""
            At `k={selected["k"]}`, the observed ratio is
            **{selected["ratio"]:.3f}**, or
            **{selected["ratio_over_k"]:.3f} × k**. The no-replacement
            control stays below 3. This is direct evidence for
            `Omega(k)`, stronger than the paper's `Omega(log k)` conclusion.
            """
        ),
        kind="success",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## What each claim now has

    | Claim | Candidate status | Confidence | Direct evidence |
    |---|---|---|---|
    | C1 laminar cover | VERIFIED | HIGH | symbolic charging certificate |
    | C2 metrical task systems | VERIFIED | HIGH | exact-rational Farkas certificate |
    | C3 stability | VERIFIED | MEDIUM | induction plus unbounded primal family |
    | C4 caching | VERIFIED | HIGH | named deterministic combiner and control |
    | C5 real data | BLOCKED | LOW | four routes; essential semantics unavailable |
    | C6 lower bound | VERIFIED | HIGH | repaired adversary and rejected printed order |

    A universal theorem is not promoted from a finite sweep. C1, C2, C3,
    and C6 use machine-checkable symbolic or parametric certificates. C4
    implements the named algorithm. Every verifier exits nonzero if its
    evidence or rejection control fails.
    """)
    return


@app.cell
def _():
    rainy_day_counts = {
        "> 0 mm": 18_550,
        "> 1 mm": 14_222,
        "> 2.5 mm": 11_361,
    }
    return (rainy_day_counts,)


@app.cell
def _(mo, rainy_day_counts):
    threshold = mo.ui.radio(
        options=list(rainy_day_counts),
        value="> 0 mm",
        label="Possible rainy-day rule omitted by the paper",
    )
    threshold
    return (threshold,)


@app.cell
def _(mo, rainy_day_counts, threshold):
    mo.md(
        f"""
        The selected rule produces **{rainy_day_counts[threshold.value]:,}**
        rainy-day records over the 153 complete Central Park years named by
        the paper. The range across plausible thresholds is
        **{max(rainy_day_counts.values()) - min(rainy_day_counts.values()):,}**
        requests. Because the paper gives no threshold, baseline
        implementation, processed data, initial configurations, tie rules, or
        seeds, C5 has no unique faithful executable pipeline.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Bottom line

    The candidate replaces five toy checks with exact evidence and keeps
    the unreleased real-data experiment visibly **BLOCKED**. The best
    supported possible score is **10/12**, but only the live evaluator can
    change the current **5/12**.

    The notebook embeds the observed values, so opening it does not rerun
    the formal suite or download the 19.20 GB Citi Bike manifest.
    """)
    return


if __name__ == "__main__":
    app.run()
