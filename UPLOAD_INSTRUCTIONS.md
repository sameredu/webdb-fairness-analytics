# Upload Instructions — webdb-fairness-analytics

## Create the repository on GitHub
1. Create a new EMPTY repo named: webdb-fairness-analytics (no README/license)
2. From this folder:

```bash
cd webdb-fairness-analytics
git init
git add -A
git commit -m "Initial release: strengthened fairness-aware disruption analysis"
git branch -M main
git remote add origin https://github.com/sameredu/webdb-fairness-analytics.git
git push -u origin main
```

## IMPORTANT — privacy
- The private re-identification file (PRIVATE_ID_Mapping_DO_NOT_PUBLISH.xlsx)
  must NEVER be added. It is already blocked by .gitignore.
- The 7 dataset .xlsx files are NOT included here; users download them from
  Zenodo (DOI 10.5281/zenodo.20366538). See data/README.md.

## Optional — mint a software DOI
After pushing, create a GitHub Release (e.g. v1.0.0) and link the repo to Zenodo
to mint a citable software DOI for the paper.
