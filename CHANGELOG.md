# Changelog

All notable changes to this repository are recorded here. Version numbers follow
[Semantic Versioning](https://semver.org/).

---

## [2.0.0] — 2026

Released alongside the major revision of the companion manuscript for
*Discover Education*. **This is a breaking release**: two results published in
v1.0.0 were withdrawn after re-examination of the underlying data. Results
produced by v1.0.0 should not be cited.

### Removed

- **Cross-sectional contrast** (`analysis4_crosssectional.csv`, formerly written
  by `02_statistical_analysis.py`). The contrast compared non-disrupted
  instances (*r* = 0; *n* = 210; mean 91.0%) with substantially disrupted
  instances (*r* ≥ 0.50; *n* = 47; mean 3.4%). On re-examination, the
  non-disrupted group was drawn **entirely** from theory examinations while the
  disrupted group was **81% practical**, and score availability in the practical
  examinations was itself determined by whether manual grading remained
  outstanding. The comparison therefore measured assessment format and the
  gradebook export mechanism rather than performance. It was described in v1.0.0
  as "partially circular"; it was in fact confounded. Replaced in function by the
  threshold-sensitivity analysis (`04_revision_analyses.py`, analysis 5).

- **Cohen's *d* = 7.66.** A standardised mean difference reported after a
  rank-based test presupposes the distributional assumptions the test was chosen
  to avoid. Replaced by matched-pairs rank-biserial correlation (*r* = 1.00).

- **Causal phrasing** in `README.md` and in the docstring of
  `02_statistical_analysis.py`. The design is retrospective and observational; it
  supports an attributional argument, not a causal one.

### Added

- `scripts/04_revision_analyses.py`, containing five new analyses:
  - **Analysis 4** — three-point trajectory (prior / disrupted / recovery),
    establishing that flagged students averaged 77.8% *before* disruption and
    exceeded that baseline by only 21.3 points on recovery.
  - **Analysis 5** — threshold sensitivity across *r* ∈ [0.30, 1.00].
  - **Analysis 6** — section-level robustness across five sections and three
    instructors, with the examination instrument held constant by design.
  - **Analysis 7** — supplementary-examination participation structure.
  - **Analysis 8** — overlap between the log signature and the institutional
    Incomplete-request route.
- **Analysis 0** in `02_statistical_analysis.py`: Shapiro–Wilk and Levene
  assumption checks, reported before test selection rather than assumed.
- Rank-biserial correlation, Hodges–Lehmann shift, bootstrap 95% confidence
  interval (10,000 replicates, seed 42), and the exact attainable *p*-value floor
  for the matched-pair analysis.
- Duration range and count of sessions exceeding 30 minutes in the
  complete-disconnection analysis, since the signature is not uniform: recorded
  durations range from 0.3 to over 90 minutes, and short zero-answer sessions are
  equally consistent with entry-and-withdrawal.
- A **Known constraints** section in `README.md`.

### Fixed

- **Cohort size**: 206 → **226** unique students. The figure 206 is the Midterm 1
  cohort; twenty students appear only in later assessments.
- **Sections**: four → **five** (101, 102, 103, 201, 202), taught by three
  instructors under a single unified course specification with identical
  examinations.
- **Prior-baseline normality test**: recomputed at full precision
  (W = 0.881, *p* = 0.314). An earlier value derived from a differently filtered
  prior-exam set has been corrected.
- Description of the supplementary examination. It is **not** gated on verified
  connectivity disruption. Two institutional routes exist — a cohort-wide second
  sitting where a failure is widespread, and an individually reviewed Incomplete
  request — and where a student sits both examinations, policy records the higher
  score. The dataset does not record which route authorised each sitting.

---

## [1.0.0] — 2026-06-15

Initial release: feature engineering, within-subject recovery, prevalence with
Wilson confidence intervals, complete-disconnection signature, and a
cross-sectional contrast. **Superseded — see 2.0.0.**
