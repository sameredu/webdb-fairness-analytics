# webdb-fairness-analytics

## Detecting Infrastructure-Induced Examination Inequality from Moodle Logs

Reproducible analysis code for a fairness-aware learning-analytics study that
distinguishes **infrastructure-induced examination failure** from genuine
academic underperformance, using real Moodle examination logs from a
connectivity-constrained higher-education setting.

[![License: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](LICENSE)
[![Dataset: CC BY 4.0](https://img.shields.io/badge/Dataset-CC%20BY%204.0-orange.svg)](https://doi.org/10.5281/zenodo.20366538)
[![Dataset DOI](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.20366538-blue)](https://doi.org/10.5281/zenodo.20366538)

> **Version 2.0.0** supersedes v1.0.0. Two analyses present in v1.0.0 were
> withdrawn and six were added, following journal peer review. See
> [CHANGELOG.md](CHANGELOG.md) for the full record. **Do not cite results
> produced by v1.0.0.**

---

## Motivation

Online examinations through Learning Management Systems (LMS) such as Moodle
assume stable connectivity. In **developing countries** and
**infrastructure-constrained educational settings** — where power outages,
bandwidth throttling, conflict, blockade, and chronic maintenance deficits
disrupt connectivity — this assumption fails. A student who loses connectivity
mid-examination can be graded identically to one who did not study, because the
LMS records both as low-scoring or blank submissions.

This project provides a transparent, reproducible pipeline that detects
infrastructure-induced disruption signatures in standard Moodle gradebook
exports and validates them against each student's own unimpeded performance.

---

## Key analyses

All analyses use a **severity-graded** disruption definition
(`blank_ratio = unanswered / n_questions`), where *substantial* disruption is
`blank_ratio >= 0.50`. This conservative threshold separates infrastructure-
induced failure from incidental single-question omissions.

| # | Analysis | Design | What it shows |
|---|----------|--------|---------------|
| 0 | **Assumption checks** | Shapiro–Wilk, Levene | Every analysed distribution departs from normality; variances are heterogeneous. Justifies the rank-based tests |
| 1 | **Within-subject recovery** | Wilcoxon signed-rank | Disrupted students recover from a mean of 10.0% to 98.6% (gain +88.6 pts; rank-biserial *r* = 1.00; bootstrap 95% CI [78.0, 97.1]) |
| 2 | **Prevalence** | Wilson 95% CIs per exam | Practical exams show markedly higher disruption (≈34%) than theory exams (≈1.5–4.4%) |
| 3 | **Complete disconnection** | Behavioural signature | 39 instances across 35 students and 4 exams with **zero** answers transmitted |
| 4 | **Three-point trajectory** | Prior / disrupted / recovery | Students averaged 77.8% *before* disruption, 10.0% under it, 99.0% after — a return to a demonstrated level, not a learning gain |
| 5 | **Threshold sensitivity** | *r* from 0.30 to 1.00 | The recovery result is invariant from *r* ≥ 0.30 to *r* ≥ 0.70; the cut-point is not load-bearing |
| 6 | **Section robustness** | χ² across five sections | No significant differences (χ² = 3.36, df = 4, *p* = 0.499). The examination is identical across sections, so this bears on delivery, not content |
| 7 | **Supplementary structure** | Participation pattern | 33 of 226 students; thin and even across sections (*p* = 0.224) |
| 8 | **Route overlap** | Log signature vs. institutional route | 6 of 18 final-exam instances of supplementary students carry **no** signature — the two mechanisms capture partly non-overlapping populations |

### On interpretation

The within-subject design removes between-subject confounding by ability,
preparation, section, and instructor. It does **not** establish causation: the
study is retrospective and observational, and disruption is inferred from
behavioural log signatures rather than from network telemetry. The three-point
trajectory (analysis 4) is what distinguishes conditional failure from academic
underperformance and from post-hoc learning gain; it is reported descriptively,
since at *n* = 5 the Wilcoxon test cannot reach conventional significance.

With *n* = 7 matched pairs, the smallest attainable two-sided *p* is
2/2⁷ = 0.0156, and the observed *p* equals this floor. Evidential weight rests
on consistency (7/7 pairs improved) and magnitude, not on the *p*-value.

---

## Repository structure

```
webdb-fairness-analytics/
├── scripts/
│   ├── 01_feature_engineering.py    # 7 exams -> instance_level_features.csv (675 instances)
│   ├── 02_statistical_analysis.py   # assumption checks, recovery, prevalence, disconnection
│   ├── 03_generate_figures.py       # publication-quality figures (no embedded titles)
│   ├── 04_revision_analyses.py      # trajectory, threshold sensitivity, robustness, overlap
│   └── 05_write_summary.py          # assembles ANALYSIS_SUMMARY.json from the CSVs
├── results/
│   ├── instance_level_features.csv
│   ├── analysis0_assumption_checks.csv
│   ├── analysis1_recovery.csv / analysis1_matched_pairs.csv
│   ├── analysis2_prevalence.csv
│   ├── analysis3_complete_disconnection.csv
│   ├── analysis4_trajectory.csv
│   ├── analysis5_threshold_sensitivity.csv
│   ├── analysis6_section_robustness.csv
│   ├── analysis7_supplementary_structure.csv
│   ├── analysis8_route_overlap.csv
│   └── ANALYSIS_SUMMARY.json
├── figures/
│   ├── Fig1_prevalence.png
│   ├── Fig2_recovery.png
│   └── Fig3_complete_disconnection.png
├── data/                            # (download dataset from Zenodo — see data/README.md)
├── CHANGELOG.md
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Reproducing the analysis

```bash
git clone https://github.com/sameredu/webdb-fairness-analytics.git
cd webdb-fairness-analytics
pip install -r requirements.txt

# Download the 7 anonymized .xlsx files from Zenodo into ./data
#   https://doi.org/10.5281/zenodo.20366538
export WEBDB_DATA="$(pwd)/data"

python scripts/01_feature_engineering.py     # builds results/instance_level_features.csv
python scripts/02_statistical_analysis.py    # assumption checks + analyses 1-3
python scripts/04_revision_analyses.py       # analyses 4-8
python scripts/03_generate_figures.py        # writes figures/*.png
python scripts/05_write_summary.py           # assembles results/ANALYSIS_SUMMARY.json
```

All stochastic steps use a fixed seed (`42`), including the 10,000-replicate
bootstrap in analysis 1.

---

## Known constraints

These are stated in the manuscript and repeated here so that anyone reusing the
data reaches them before, not after, running the pipeline.

- **Manual grading affects score availability.** Practical examinations contain
  manually graded items; instances still awaiting grading carry no exported
  score, which is why only 301 of 675 instances have a numeric grade. The
  missingness is **not random** with respect to disruption: an instance with no
  submitted answers needs no manual grading and receives an exported zero,
  whereas an instance with submitted answers may remain ungraded. Any comparison
  of scores between disrupted and non-disrupted instances across formats is
  therefore confounded by the export mechanism. This is why the cross-sectional
  contrast present in v1.0.0 was withdrawn.
- **Single-question assessment.** `Midterm2_Practical` has `n_q = 1`, so
  `blank_ratio` there can only be 0 or 1 and the four-tier severity scale
  collapses to a binary distinction for that examination.
- **Small matched sample.** The recovery analysis rests on 7 pairs, of which 3
  compare a disrupted *practical* examination with a supplementary *theory*
  examination; format is not held constant within those pairs.
- **Ceiling effect.** `Supp_Theory` has a median of 100% (19 of 29 candidates
  scored exactly 100%), so it discriminates poorly at the upper end.
- **Authorisation route not recorded.** The dataset does not record which
  institutional route authorised each supplementary sitting. Analysis 7 infers
  this from participation structure; it is not an administrative record.

---

## Dataset

The seven anonymized Moodle examination files (226 students across five sections,
Web Databases course, 7 assessments, 675 examination instances) are openly
available on Zenodo under CC BY 4.0:

**DOI:** [10.5281/zenodo.20366538](https://doi.org/10.5281/zenodo.20366538)

Anonymization: sequential student labels, SHA-256 pseudonymized IDs, emails
removed, k-anonymity k ≥ 5. The private re-identification mapping is **not**
released and is excluded via `.gitignore`.

---

## Citation

If you use this code or dataset, please cite the dataset and the companion
article (journal reference will be updated upon publication):

```bibtex
@dataset{yaghi_2026_webdb,
  author    = {Yaghi, Samer and AbuSamra, Aiman Ahmed},
  title     = {{Web Databases — Anonymized Moodle Examination Dataset
               for Fairness-Aware Learning Analytics}},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20366538},
  url       = {https://doi.org/10.5281/zenodo.20366538}
}
```

---

## Authors

- **Samer Yaghi** — University College of Applied Sciences (UCAS) / Islamic University of Gaza (IUG) · [ORCID 0009-0001-0268-7163](https://orcid.org/0009-0001-0268-7163) · syaghi@ucas.edu.ps
- **Prof. Aiman Ahmed AbuSamra** — Islamic University of Gaza (IUG) · [ORCID 0000-0003-4652-3993](https://orcid.org/0000-0003-4652-3993)

## License

Code: **MIT** (see `LICENSE`). Dataset: **CC BY 4.0** (via Zenodo).
