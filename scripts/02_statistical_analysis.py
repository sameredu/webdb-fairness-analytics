"""
02_statistical_analysis.py   (v2.0.0 -- aligned with manuscript revision v5)

Core analyses for fairness-aware disruption detection:
  ANALYSIS 0 - Assumption checks (Shapiro-Wilk, Levene) preceding test selection
  ANALYSIS 1 - Within-subject recovery (Wilcoxon signed-rank, rank-biserial,
               bootstrap CI, Hodges-Lehmann shift)
  ANALYSIS 2 - Disruption prevalence with Wilson 95% CIs (severity-graded)
  ANALYSIS 3 - Complete-disconnection behavioural signature

CHANGES FROM v1.0.0
  * The cross-sectional contrast formerly written to analysis4_crosssectional.csv
    has been REMOVED. The non-disrupted group (r = 0) was drawn entirely from
    theory examinations while the disrupted group (r >= 0.50) was predominantly
    practical, and score availability in practical examinations was itself
    determined by whether manual grading remained outstanding. The comparison was
    therefore confounded by assessment format and by the export mechanism rather
    than being merely partially circular. See scripts/04_revision_analyses.py for
    the threshold-sensitivity analysis that replaces it.
  * Cohen's d has been REMOVED. A standardised mean difference presupposes the
    distributional assumptions that the rank-based tests were chosen to avoid.
    Effect size is now reported as matched-pairs rank-biserial correlation.
  * Causal phrasing has been removed throughout. The design is observational and
    supports an attributional argument, not a causal one.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportion_confint

SEED = 42
rng = np.random.default_rng(SEED)
np.random.seed(SEED)

RES = os.path.join(os.path.dirname(__file__), "..", "results")
inst = pd.read_csv(os.path.join(RES, "instance_level_features.csv"))

SUBSTANTIAL = 0.50
EXAM_ORDER = ["Midterm1", "Midterm2_Theory", "Midterm2_Practical", "Final_Theory",
              "Final_Practical", "Supp_Theory", "Supp_Practical"]

# ----------------------------------------------------------------------
# Build the matched pairs first (needed by the assumption checks)
# ----------------------------------------------------------------------
supp = (inst[(inst.exam == "Supp_Theory") & inst.score_pct.notna()]
        [["student", "score_pct"]].rename(columns={"score_pct": "recovery_pct"}))
fdis = (inst[(inst.exam.isin(["Final_Theory", "Final_Practical"]))
             & (inst.blank_ratio >= SUBSTANTIAL) & inst.score_pct.notna()]
        [["student", "score_pct"]].rename(columns={"score_pct": "disrupted_pct"}))
fdis = fdis.groupby("student", as_index=False).min()
pairs = fdis.merge(supp, on="student")

# ----------------------------------------------------------------------
# ANALYSIS 0 - assumption checks
# ----------------------------------------------------------------------
graded = inst[inst.score_pct.notna()]
non_d = graded[graded.blank_ratio == 0]["score_pct"]
dis_d = graded[graded.blank_ratio >= SUBSTANTIAL]["score_pct"]

norm_rows = []
for label, x in [("disrupted_scores", pairs.disrupted_pct.values),
                 ("recovery_scores", pairs.recovery_pct.values),
                 ("paired_differences", (pairs.recovery_pct - pairs.disrupted_pct).values),
                 ("non_disrupted_instances", non_d.values),
                 ("disrupted_instances", dis_d.values)]:
    W, p = stats.shapiro(x)
    norm_rows.append({"distribution": label, "n": len(x),
                      "shapiro_W": round(float(W), 4),
                      "p_value": f"{p:.3g}",
                      "normality_rejected": bool(p < 0.05)})
lev_W, lev_p = stats.levene(non_d, dis_d)
norm = pd.DataFrame(norm_rows)
norm.to_csv(os.path.join(RES, "analysis0_assumption_checks.csv"), index=False)

print("=== ANALYSIS 0: Assumption checks (justify non-parametric choice) ===")
print(norm.to_string(index=False))
print(f"  Levene (equal variance, non-disrupted vs disrupted): "
      f"W={lev_W:.3f}, p={lev_p:.4g}")

# ----------------------------------------------------------------------
# ANALYSIS 1 - within-subject recovery
# ----------------------------------------------------------------------
a = pairs.disrupted_pct.values
b = pairs.recovery_pct.values
diff = b - a
n = len(pairs)

w_stat, w_p = stats.wilcoxon(b, a)
# matched-pairs rank-biserial correlation
rank_biserial = 1 - (2 * float(w_stat)) / (n * (n + 1) / 2)
# smallest attainable two-sided p at this n (exact sign-change enumeration)
p_floor = 2 / (2 ** n)
# Hodges-Lehmann: median of Walsh averages of the paired differences
walsh = [(diff[i] + diff[j]) / 2 for i in range(n) for j in range(i, n)]
hodges_lehmann = float(np.median(walsh))
# bootstrap CI for the mean gain
boot = [float(np.mean(rng.choice(diff, n, replace=True))) for _ in range(10000)]
ci_lo, ci_hi = np.percentile(boot, [2.5, 97.5])

a1 = {"n_pairs": n,
      "disrupted_mean_pct": round(float(a.mean()), 2),
      "disrupted_median_pct": round(float(np.median(a)), 2),
      "recovery_mean_pct": round(float(b.mean()), 2),
      "recovery_median_pct": round(float(np.median(b)), 2),
      "mean_gain_pts": round(float(diff.mean()), 2),
      "wilcoxon_W": round(float(w_stat), 2),
      "p_value": round(float(w_p), 4),
      "p_value_floor_at_this_n": round(p_floor, 4),
      "rank_biserial_r": round(rank_biserial, 3),
      "hodges_lehmann_shift_pts": round(hodges_lehmann, 1),
      "boot_ci95_low_pts": round(float(ci_lo), 1),
      "boot_ci95_high_pts": round(float(ci_hi), 1),
      "bootstrap_replicates": 10000,
      "seed": SEED}
pd.DataFrame([a1]).to_csv(os.path.join(RES, "analysis1_recovery.csv"), index=False)
pairs.to_csv(os.path.join(RES, "analysis1_matched_pairs.csv"), index=False)

print("\n=== ANALYSIS 1: Within-subject recovery (primary) ===")
for k, v in a1.items():
    print(f"  {k}: {v}")
print("  NOTE: the observed p equals the floor attainable at this sample size;")
print("        evidential weight rests on consistency and magnitude, not on p.")

# ----------------------------------------------------------------------
# ANALYSIS 2 - prevalence with Wilson CIs
# ----------------------------------------------------------------------
rows = []
for exam in EXAM_ORDER:
    sub = inst[inst.exam == exam]
    n_sub = int((sub.blank_ratio >= SUBSTANTIAL).sum())
    n_complete = int((sub.blank_ratio == 1.0).sum())
    lo, hi = proportion_confint(n_sub, len(sub), method="wilson")
    rows.append({"exam": exam, "n_students": len(sub),
                 "substantial_disruption": n_sub,
                 "complete_disconnection": n_complete,
                 "rate_pct": round(100 * n_sub / len(sub), 1),
                 "ci95_low": round(100 * lo, 1),
                 "ci95_high": round(100 * hi, 1)})
prev = pd.DataFrame(rows)
prev.to_csv(os.path.join(RES, "analysis2_prevalence.csv"), index=False)
print("\n=== ANALYSIS 2: Disruption prevalence (substantial, Wilson CI) ===")
print(prev.to_string(index=False))

# ----------------------------------------------------------------------
# ANALYSIS 3 - complete-disconnection signature
# ----------------------------------------------------------------------
cd = inst[inst.blank_ratio == 1.0].copy()
cdd = cd[cd.duration_min.notna()]
a3 = {"complete_instances": len(cd),
      "unique_students": int(cd.student.nunique()),
      "exams_spanned": int(cd.exam.nunique()),
      "mean_duration_min_with_zero_answers": round(float(cdd.duration_min.mean()), 1),
      "median_duration_min": round(float(cdd.duration_min.median()), 1),
      "min_duration_min": round(float(cdd.duration_min.min()), 1),
      "max_duration_min": round(float(cdd.duration_min.max()), 1),
      "instances_over_30_min": int((cdd.duration_min > 30).sum())}
pd.DataFrame([a3]).to_csv(os.path.join(RES, "analysis3_complete_disconnection.csv"), index=False)
print("\n=== ANALYSIS 3: Complete-disconnection signature ===")
for k, v in a3.items():
    print(f"  {k}: {v}")
print("  NOTE: duration is not uniform across these instances. Short zero-answer")
print("        sessions are equally consistent with entry-and-withdrawal; the")
print("        behavioural argument applies to the sustained cases only.")
