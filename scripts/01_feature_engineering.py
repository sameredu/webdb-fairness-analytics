"""
01_feature_engineering.py
Instance-level behavioral feature extraction across all seven Web Databases
examinations for fairness-aware learning-analytics analysis.

Each (student, exam) pair is one instance. Disruption is flagged from the
presence of one or more 'Unanswered' question cells in the Moodle gradebook
export. The script produces a single tidy CSV (instance_level_features.csv)
used by all downstream statistical scripts.

Input : seven anonymized .xlsx exports (Zenodo DOI 10.5281/zenodo.20366538)
Output: results/instance_level_features.csv
"""
import pandas as pd
import numpy as np
import re
import os

DATA_DIR = os.environ.get("WEBDB_DATA", "/mnt/user-data/uploads")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(OUT_DIR, exist_ok=True)

# (filename, max_score, exam_type, ordinal_position_in_semester)
EXAMS = {
    "Midterm1":           ("DataBase_WEB_Midterm1_Anonymized.xlsx",        25, "theory",    1),
    "Midterm2_Theory":    ("DataBase_WEB_Midterm2_Theory_Anonymized.xlsx", 15, "theory",    2),
    "Midterm2_Practical": ("DataBase_WEB_Midterm2_Practical_Anonymized.xlsx",10,"practical", 3),
    "Final_Theory":       ("DataBase_WEB_Final_Theory_Anonymized.xlsx",     20, "theory",    4),
    "Final_Practical":    ("DataBase_WEB_Final_Practical_Anonymized.xlsx",  10, "practical", 5),
    "Supp_Theory":        ("DataBase_WEB_Supp_Theory_Anonymized.xlsx",      10, "theory",    6),
    "Supp_Practical":     ("DataBase_WEB_Supp_Practical_Anonymized.xlsx",   10, "practical", 7),
}


def parse_duration(s):
    """Convert a Moodle duration string to minutes (float)."""
    if pd.isna(s):
        return np.nan
    s = str(s)
    total = 0.0
    h = re.search(r"(\d+)\s*hour", s)
    m = re.search(r"(\d+)\s*min", s)
    sec = re.search(r"(\d+)\s*sec", s)
    if h:
        total += int(h.group(1)) * 60
    if m:
        total += int(m.group(1))
    if sec:
        total += int(sec.group(1)) / 60.0
    return total if total > 0 else np.nan


def main():
    records = []
    for exam, (fname, mx, typ, order) in EXAMS.items():
        df = pd.read_excel(os.path.join(DATA_DIR, fname))
        qcols = [c for c in df.columns if c.startswith("Q")]
        scol = [c for c in df.columns if "Total_Score" in c][0]
        nq = len(qcols)
        for _, r in df.iterrows():
            qvals = r[qcols].astype(str)
            n_unans = qvals.str.contains("Unanswered", case=False, na=False).sum()
            n_grading = qvals.str.contains("Needs_Grading", case=False, na=False).sum()
            score = pd.to_numeric(r[scol], errors="coerce")
            dur = parse_duration(r.get("Duration"))
            records.append({
                "student": r["Student_Label"],
                "exam": exam,
                "exam_type": typ,
                "exam_order": order,
                "section": r.get("Section"),
                "n_q": nq,
                "n_unanswered": int(n_unans),
                "n_needs_grading": int(n_grading),
                "blank_ratio": n_unans / nq if nq else np.nan,
                "duration_min": dur,
                "score": score,
                "max_score": mx,
                "score_pct": 100 * score / mx if pd.notna(score) else np.nan,
                "attempt_status": r.get("Attempt_Status"),
                "disrupted": bool(n_unans > 0),
            })

    inst = pd.DataFrame(records)
    out = os.path.join(OUT_DIR, "instance_level_features.csv")
    inst.to_csv(out, index=False)
    print(f"Wrote {out}: {len(inst)} instances, "
          f"{inst.disrupted.sum()} disrupted, "
          f"{inst.score_pct.notna().sum()} graded.")
    return inst


if __name__ == "__main__":
    main()
