# Upload Instructions — webdb-fairness-analytics v2.0.0

> **Read the privacy section first.** Earlier versions of this file stated that a
> `.gitignore` blocked the private re-identification mapping. No `.gitignore`
> existed. One is now included. Verify it is present before staging anything.

---

## 0. Privacy check — run this before every commit

Git history is permanent. A file that is committed and later deleted remains
recoverable from the history; removing it requires `git-filter-repo` or
recreating the repository. Check **before** staging, not after.

```bash
# 1. Confirm the .gitignore exists
test -f .gitignore && echo "OK: .gitignore present" || echo "STOP: .gitignore missing"

# 2. Show exactly what git would upload — read this list in full
git status --porcelain
git add --dry-run .

# 3. Confirm no mapping or raw data file is staged
git status --porcelain | grep -iE "mapping|private|do_not_publish|\.xlsx" \
  && echo "STOP — sensitive file staged" \
  || echo "OK: nothing sensitive staged"
```

Never use `git add -A` or `git add .` without reading the dry-run output first.

---

## 1. What goes to GitHub and what does not

| Item | Location | Reason |
|------|----------|--------|
| Scripts, README, CHANGELOG, CITATION | **GitHub** | Version-controlled, diffable |
| `results/*.csv`, `ANALYSIS_SUMMARY.json` | **GitHub** | Small, and lets anyone reproduce analyses 0–8 without the raw files |
| `figures/*.png` | **GitHub** | Referenced by the manuscript |
| The 7 anonymized `.xlsx` files | **Zenodo only** | Zenodo is archival and DOI-bearing; GitHub is neither. One canonical copy prevents drift |
| `PRIVATE_ID_Mapping_DO_NOT_PUBLISH.xlsx` | **Nowhere** | Breaches ethics approval 2026/29 |

Because `results/instance_level_features.csv` is committed, a reviewer can clone
the repository and immediately run scripts 02, 04 and 05 to reproduce every
number in the manuscript. Only script 01 (feature engineering) requires the raw
`.xlsx` files from Zenodo.

**If you decide to bundle the raw data anyway** (some reviewers prefer it), then
also: remove the `data/*.xlsx` line from `.gitignore`, add a `LICENSE-DATA` file
containing the CC BY 4.0 text, and state in `README.md` that code is MIT while
data is CC BY 4.0. Do not do this for the mapping file under any circumstance.

---

## 2. Push version 2.0.0

The repository already exists, so this is an update rather than an initial push.

```bash
cd webdb-fairness-analytics
git pull origin main

# Copy the v2.0.0 files over the working tree, then:
git status --porcelain          # read this
git add --dry-run .             # and this

git add .gitignore CHANGELOG.md README.md CITATION.cff UPLOAD_INSTRUCTIONS.md
git add scripts/ results/ figures/ data/README.md

git commit -m "v2.0.0: withdraw confounded cross-sectional analysis and Cohen's d; add trajectory, threshold sensitivity and robustness analyses

Two results published in v1.0.0 are withdrawn following journal peer review:
the cross-sectional contrast (confounded by assessment format and by
export-driven score availability) and Cohen's d = 7.66 (a parametric effect
size reported after a rank-based test). Six analyses are added. Cohort size
corrected from 206 to 226 students across five sections. Causal phrasing
removed throughout. See CHANGELOG.md."

git push origin main
```

---

## 3. Create the release

```bash
git tag -a v2.0.0 -m "v2.0.0 — aligned with Discover Education major revision"
git push origin v2.0.0
```

Then on GitHub: **Releases → Draft a new release → v2.0.0**, and paste the
`CHANGELOG.md` 2.0.0 section as the release notes. State explicitly that v1.0.0
is superseded and that results produced by it should not be cited.

---

## 4. Zenodo

If the GitHub–Zenodo integration is enabled, publishing the release mints a new
**version DOI** automatically. The **concept DOI** stays constant and always
resolves to the latest version.

- Cite the **concept DOI** in the manuscript so that reviewers and readers reach
  the corrected code without the citation needing to change again.
- Find it on the Zenodo record page under *Cite all versions*.
- Separately, open the **dataset** record (10.5281/zenodo.20366538) and use
  *Edit metadata* to correct any description that still says "206 students". The
  data files themselves are unchanged, so no new dataset version is required.

---

## 5. Order of operations

Publish the release **before** submitting the revision. If a reviewer opens the
repository link cited in the manuscript, it should already show the corrected
code rather than the version that still computes the withdrawn analysis.
