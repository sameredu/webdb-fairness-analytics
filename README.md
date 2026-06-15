# webdb-fairness-analytics

## Detecting Infrastructure-Induced Examination Inequality from Moodle Logs

Reproducible analysis code for a fairness-aware learning-analytics study that
distinguishes **infrastructure-induced examination failure** from genuine
academic underperformance, using real Moodle examination logs from a
connectivity-constrained higher-education setting.

[![License: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](LICENSE)
[![Dataset: CC BY 4.0](https://img.shields.io/badge/Dataset-CC%20BY%204.0-orange.svg)](https://doi.org/10.5281/zenodo.20366538)
[![Dataset DOI](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.20366538-blue)](https://doi.org/10.5281/zenodo.20366538)

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
exports and validates them with a **within-subject recovery design**.

---

## Key analyses

All three analyses use a **severity-graded** disruption definition
(`blank_ratio = unanswered / n_questions`), where *substantial* disruption is
`blank_ratio >= 0.50`. This conservative threshold separates infrastructure-
induced failure from incidental single-question omissions.

| Analysis | Design | What it shows |
|----------|--------|---------------|
| **1. Recovery (primary)** | Within-subject (Wilcoxon signed-rank) | Disrupted students recover from a mean of ~10% to ~99% in stable supplementary exams (mean gain ≈ +89 pts, *p* = 0.0156) |
| **2. Prevalence** | Wilson 95% CIs per exam | Practical exams show markedly higher disruption (≈34%) than theory exams (≈1.5–4.4%) |
| **3. Complete disconnection** | Behavioural signature | 35 students across 4 exams remained in full-length (~70 min) sessions with **zero** answers transmitted |

The within-subject recovery design is the primary causal evidence: because each
student serves as their own control, it is immune to the circularity that
affects cross-sectional score comparisons.

---

## Repository structure

```
webdb-fairness-analytics/
├── scripts/
│   ├── 01_feature_engineering.py   # 7 exams -> instance_level_features.csv (675 instances)
│   ├── 02_statistical_analysis.py  # recovery, prevalence, disconnection, cross-sectional
│   └── 03_generate_figures.py      # publication-quality figures (no embedded titles)
├── results/
│   ├── instance_level_features.csv
│   ├── analysis1_recovery.csv / analysis1_matched_pairs.csv
│   ├── analysis2_prevalence.csv
│   ├── analysis3_complete_disconnection.csv
│   ├── analysis4_crosssectional.csv
│   └── ANALYSIS_SUMMARY.json
├── figures/
│   ├── Fig1_prevalence.png
│   ├── Fig2_recovery.png
│   └── Fig3_complete_disconnection.png
├── data/                            # (download dataset from Zenodo - see data/README.md)
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
python scripts/02_statistical_analysis.py    # prints + writes all statistical results
python scripts/03_generate_figures.py        # writes figures/*.png
```

---

## Dataset

The seven anonymized Moodle examination files (206 students, Web Databases
course, 7 assessments) are openly available on Zenodo under CC BY 4.0:

**DOI:** [10.5281/zenodo.20366538](https://doi.org/10.5281/zenodo.20366538)

Anonymization: sequential student labels, SHA-256 pseudonymized IDs, emails
removed, k-anonymity k ≥ 5. The private re-identification mapping is **not**
released and is excluded via `.gitignore`.

---

## Citation

If you use this code or dataset, please cite the dataset and the companion
article (preprint reference will be updated upon journal publication):

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
