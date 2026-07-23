"""
04_revision_analyses.py   (new in v2.0.0)

Analyses added during the Discover Education major revision. Each block
reproduces a specific figure, table, or claim in manuscript v5.

  ANALYSIS 4 - Three-point trajectory: prior / disrupted / recovery      (§4.1, Table 5)
  ANALYSIS 5 - Threshold sensitivity of the recovery result              (§4.5, Table 7)
  ANALYSIS 6 - Section-level robustness check (instructor effects)       (§4.3)
  ANALYSIS 7 - Supplementary-examination participation structure         (§3.1)
  ANALYSIS 8 - Overlap between log signature and the institutional route (§2.4, §4.3)

Run after 01_feature_engineering.py. Writes to ../results/.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

SEED = 42
np.random.seed(SEED)

RES = os.path.join(os.path.dirname(__file__), "..", "results")
inst = pd.read_csv(os.path.join(RES, "instance_level_features.csv"))

SUBSTANTIAL = 0.50
FINALS = ["Final_Theory", "Final_Practical"]
PRIOR_EXAMS = ["Midterm1", "Midterm2_Theory", "Midterm2_Practical"]


def matched_pairs(threshold):
    """Disrupted final score (worst instance per student) paired with the
    subsequent stable supplementary theory score."""
    supp = (inst[(inst.exam == "Supp_Theory") & inst.score_pct.notna()]
            [["student", "score_pct"]].rename(columns={"score_pct": "recovery_pct"}))
    fdis = (inst[inst.exam.isin(FINALS) & (inst.blank_ratio >= threshold)
                 & inst.score_pct.notna()]
            [["student", "score_pct"]].rename(columns={"score_pct": "disrupted_pct"}))
    fdis = fdis.groupby("student", as_index=False).min()
    return fdis.merge(supp, on="student")


# ----------------------------------------------------------------------
# ANALYSIS 4 - three-point trajectory  (§4.1, Table 5)
# ----------------------------------------------------------------------
pairs = matched_pairs(SUBSTANTIAL)
rows = []
for _, r in pairs.iterrows():
    prior = inst[(inst.student == r.student)
                 & inst.exam.isin(PRIOR_EXAMS)
                 & inst.score_pct.notna()
                 & (inst.blank_ratio < SUBSTANTIAL)]
    rows.append({"student": r.student,
                 "n_prior_unimpeded": len(prior),
                 "prior_pct": float(prior.score_pct.mean()) if len(prior) else np.nan,
                 "disrupted_pct": r.disrupted_pct,
                 "recovery_pct": r.recovery_pct})
traj = pd.DataFrame(rows)
have_prior = traj.dropna(subset=["prior_pct"])
traj_display = traj.copy()
traj_display["prior_pct"] = traj_display.prior_pct.round(1)

traj.to_csv(os.path.join(RES, "analysis4_trajectory.csv"), index=False)
print("=== ANALYSIS 4: Three-point trajectory (prior / disrupted / recovery) ===")
print(traj_display.to_string(index=False))
print(f"\n  students with an unimpeded prior assessment: n = {len(have_prior)}")
print(f"  PRIOR {have_prior.prior_pct.mean():.1f}%  ->  "
      f"DISRUPTED {have_prior.disrupted_pct.mean():.1f}%  ->  "
      f"RECOVERY {have_prior.recovery_pct.mean():.1f}%")
gap = have_prior.recovery_pct.mean() - have_prior.prior_pct.mean()
print(f"  recovery exceeds prior baseline by only {gap:+.1f} points "
      f"(exact: {gap:+.4f})")
print("  -> a return to a demonstrated level, not a learning gain.")
W_pb, p_pb = stats.shapiro(have_prior.prior_pct.values)
print(f"  Shapiro-Wilk on the prior baseline: n={len(have_prior)}, "
      f"W={W_pb:.4f}, p={p_pb:.4f}   (Table 4, row 1)")
print(f"  NOTE: at n = {len(have_prior)} the Wilcoxon test cannot reach p < 0.05 "
      f"(floor = {2 / 2 ** len(have_prior):.4f}); reported descriptively.")

# ----------------------------------------------------------------------
# ANALYSIS 5 - threshold sensitivity  (§4.5, Table 7)
# ----------------------------------------------------------------------
sens = []
for thr in [0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 1.00]:
    flagged = inst[inst.blank_ratio >= thr]
    mp = matched_pairs(thr)
    row = {"threshold": thr,
           "flagged_instances": len(flagged),
           "prevalence_pct": round(100 * len(flagged) / len(inst), 1),
           "n_pairs": len(mp)}
    if len(mp) >= 3:
        W, p = stats.wilcoxon(mp.recovery_pct, mp.disrupted_pct)
        row["wilcoxon_W"] = round(float(W), 1)
        row["p_value"] = round(float(p), 4)
        row["mean_gain_pts"] = round(float((mp.recovery_pct - mp.disrupted_pct).mean()), 1)
    else:
        row["wilcoxon_W"] = row["p_value"] = row["mean_gain_pts"] = np.nan
    sens.append(row)
sens = pd.DataFrame(sens)
sens.to_csv(os.path.join(RES, "analysis5_threshold_sensitivity.csv"), index=False)
print("\n=== ANALYSIS 5: Threshold sensitivity ===")
print(sens.to_string(index=False))
print("  -> the result is invariant from r >= 0.30 to r >= 0.70; the 0.50 cut-point")
print("     is a reporting convention, not a load-bearing assumption.")

# ----------------------------------------------------------------------
# ANALYSIS 6 - section-level robustness  (§4.3)
# ----------------------------------------------------------------------
inst["flagged"] = inst.blank_ratio >= SUBSTANTIAL


def section_test(df, label):
    secs = sorted(df.section.unique())
    tab = np.array([[int(((df.section == s) & df.flagged).sum()),
                     int(((df.section == s) & ~df.flagged).sum())] for s in secs])
    chi2, p, dof, _ = stats.chi2_contingency(tab)
    rates = {s: float(round(100 * r[0] / r.sum(), 1)) for s, r in zip(secs, tab)}
    return {"scope": label, "chi2": round(float(chi2), 2), "df": int(dof),
            "p_value": round(float(p), 4), "rates_pct": rates}


sec_rows = [section_test(inst, "all_exams"),
            section_test(inst[inst.exam_type == "practical"], "practical_only"),
            section_test(inst[inst.exam_type == "theory"], "theory_only")]
pd.DataFrame(sec_rows).to_csv(os.path.join(RES, "analysis6_section_robustness.csv"), index=False)
print("\n=== ANALYSIS 6: Section-level robustness (five sections, three instructors) ===")
for r in sec_rows:
    print(f"  {r['scope']:16s} chi2={r['chi2']:6.2f} df={r['df']} "
          f"p={r['p_value']:.4f}  {r['rates_pct']}")
print("  -> the examination instrument is identical across sections by design, so")
print("     this null result bears on delivery, not on assessment content.")

# ----------------------------------------------------------------------
# ANALYSIS 7 - supplementary participation structure  (§3.1)
# ----------------------------------------------------------------------
supp_students = set(inst[inst.exam.str.startswith("Supp")].student)
n_total = inst.student.nunique()
ft = set(inst[inst.exam == "Final_Theory"].student)
fp = set(inst[inst.exam == "Final_Practical"].student)

enrolled = inst.groupby("section").student.nunique()
supp_by_sec = inst[inst.student.isin(supp_students)].groupby("section").student.nunique()
tab = pd.DataFrame({"enrolled": enrolled, "supplementary": supp_by_sec}).fillna(0).astype(int)
tab["rate_pct"] = (100 * tab.supplementary / tab.enrolled).round(1)
chi2, p_sec, dof, _ = stats.chi2_contingency(
    np.array([tab.supplementary.values, (tab.enrolled - tab.supplementary).values]))

a7 = {"supplementary_students": len(supp_students),
      "total_students": n_total,
      "share_of_cohort_pct": round(100 * len(supp_students) / n_total, 1),
      "share_of_final_theory_cohort_pct": round(100 * len(ft & supp_students) / len(ft), 1),
      "share_of_final_practical_cohort_pct": round(100 * len(fp & supp_students) / len(fp), 1),
      "absent_from_both_finals": len(supp_students - ft - fp),
      "section_chi2": round(float(chi2), 2),
      "section_df": int(dof),
      "section_p_value": round(float(p_sec), 4)}
pd.DataFrame([a7]).to_csv(os.path.join(RES, "analysis7_supplementary_structure.csv"), index=False)
print("\n=== ANALYSIS 7: Supplementary participation structure ===")
for k, v in a7.items():
    print(f"  {k}: {v}")
print(tab.to_string())
print("  -> thin, even participation across all sections is consistent with")
print("     individually adjudicated Incomplete requests rather than a cohort-wide")
print("     offer. NOTE: the authorisation route is NOT recorded in the data; this")
print("     is an inference from participation structure, not an administrative record.")

# ----------------------------------------------------------------------
# ANALYSIS 8 - overlap with the institutional route  (§2.4, §4.3)
# ----------------------------------------------------------------------
ov = inst[inst.student.isin(supp_students) & inst.exam.isin(FINALS)]
a8 = {"final_instances_of_supplementary_students": len(ov),
      "with_substantial_signature": int((ov.blank_ratio >= SUBSTANTIAL).sum()),
      "with_no_signature_at_all": int((ov.blank_ratio == 0).sum())}
pd.DataFrame([a8]).to_csv(os.path.join(RES, "analysis8_route_overlap.csv"), index=False)
print("\n=== ANALYSIS 8: Overlap between log signature and institutional route ===")
for k, v in a8.items():
    print(f"  {k}: {v}")
print("  -> the two mechanisms identify partly non-overlapping populations, which")
print("     is the empirical basis for proposing the log measure as a complement")
print("     to the existing process rather than a replacement for it.")
