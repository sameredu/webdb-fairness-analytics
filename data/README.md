# Data Directory

The seven anonymized Web Databases examination files are **not** bundled in this
repository. Download them from the Zenodo deposit (CC BY 4.0):

**Dataset DOI:** https://doi.org/10.5281/zenodo.20366538

Place the seven `.xlsx` files in this `data/` directory, then set the
environment variable before running the scripts:

```bash
export WEBDB_DATA="$(pwd)/data"
python scripts/01_feature_engineering.py
```

Expected files:
- DataBase_WEB_Midterm1_Anonymized.xlsx
- DataBase_WEB_Midterm2_Theory_Anonymized.xlsx
- DataBase_WEB_Midterm2_Practical_Anonymized.xlsx
- DataBase_WEB_Final_Theory_Anonymized.xlsx
- DataBase_WEB_Final_Practical_Anonymized.xlsx
- DataBase_WEB_Supp_Theory_Anonymized.xlsx
- DataBase_WEB_Supp_Practical_Anonymized.xlsx

> The private re-identification mapping file is **never** released and must not
> be committed (see `.gitignore`).
