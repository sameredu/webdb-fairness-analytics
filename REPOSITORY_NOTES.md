# Repository Notes — what is published where, and the privacy check

These notes record the publication boundaries of this repository and the check that
protects them. They are maintenance notes, not instructions for reproducing the study —
for that, see [README.md](README.md).

The study and its data release are covered by ethics approval 2026/29 (Ethical Research
Committee, Islamic University of Gaza, 30 June 2026), which covers de-identified log data
only.

---

## 1. What belongs in this repository, and what does not

| Item | Location | Reason |
|------|----------|--------|
| Scripts, README, CHANGELOG, CITATION.cff | **GitHub** | Version-controlled and diffable |
| `results/*.csv`, `ANALYSIS_SUMMARY.json` | **GitHub** | Small, and they let anyone reproduce analyses 0–8 without the raw files |
| `figures/*.png` | **GitHub** | Referenced by the article |
| The seven anonymized `.xlsx` files | **Zenodo only** | Zenodo is archival and DOI-bearing; GitHub is neither. One canonical copy prevents drift |
| The private re-identification mapping | **Neither** | Releasing it would breach the ethics approval |

Because `results/instance_level_features.csv` is committed, a reader can clone the
repository and run scripts 02, 04 and 05 immediately. Only script 01 (feature
engineering) needs the raw `.xlsx` files, which are downloaded from Zenodo:
<https://doi.org/10.5281/zenodo.23643942>

---

## 2. Privacy check — run before every commit

Git history is permanent. A file that is committed and later deleted remains recoverable
from the history; removing it properly requires `git-filter-repo` or recreating the
repository. So the check belongs **before** staging, never after.

```bash
# 1. Confirm .gitignore is present
test -f .gitignore && echo "OK: .gitignore present" || echo "STOP: .gitignore missing"

# 2. Show exactly what git would upload — read this list in full
git status --porcelain
git add --dry-run .

# 3. Confirm no mapping file or raw data file is staged
git status --porcelain | grep -iE "mapping|private|do_not_publish|\.xlsx" \
  && echo "STOP — sensitive file staged" \
  || echo "OK: nothing sensitive staged"
```

Never run `git add -A` or `git add .` without reading the dry-run output first.

---

## 3. Releases and archiving

The article cites a fixed release of this code, so **do not create a new release for
documentation changes**. Publishing a GitHub release mints a new Zenodo version DOI,
and the article's citation would then point at a superseded record.

| Change | What to do |
|--------|-----------|
| README, notes, metadata, typos | Commit to `main`. No tag, no release |
| A fix that changes any published number | Discuss first: it affects the article, not only the repository |
| Genuinely new analysis work | New release and new version DOI, with the article's release left intact |

Current fixed points:

- Article: <https://doi.org/10.1007/s44217-026-02182-6>
- Software release v2.0.0: <https://doi.org/10.5281/zenodo.21505628>
- Dataset v1.1.0: <https://doi.org/10.5281/zenodo.23643942>
