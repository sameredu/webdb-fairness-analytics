"""
02_statistical_analysis.py  (rigorous, non-circular)
Three complementary analyses for fairness-aware disruption detection:
  ANALYSIS 1 - Within-subject recovery (PRIMARY causal evidence, Wilcoxon)
  ANALYSIS 2 - Disruption prevalence with Wilson 95% CIs (severity-graded)
  ANALYSIS 3 - Complete-disconnection behavioural signature
Plus a supporting cross-sectional contrast (corroborative, not primary).
"""
import pandas as pd, numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
import os

np.random.seed(42)
RES = os.path.join(os.path.dirname(__file__), "..", "results")
inst = pd.read_csv(os.path.join(RES, "instance_level_features.csv"))
SUBSTANTIAL = 0.50
EXAM_ORDER = ["Midterm1","Midterm2_Theory","Midterm2_Practical","Final_Theory",
              "Final_Practical","Supp_Theory","Supp_Practical"]

# ANALYSIS 1 - within-subject recovery
supp=(inst[(inst.exam=="Supp_Theory")&inst.score_pct.notna()][["student","score_pct"]]
      .rename(columns={"score_pct":"recovery_pct"}))
fdis=(inst[(inst.exam.isin(["Final_Theory","Final_Practical"]))&(inst.blank_ratio>=SUBSTANTIAL)
           &inst.score_pct.notna()][["student","score_pct"]].rename(columns={"score_pct":"disrupted_pct"}))
fdis=fdis.groupby("student",as_index=False).min()
pairs=fdis.merge(supp,on="student")
w_stat,w_p=stats.wilcoxon(pairs.recovery_pct,pairs.disrupted_pct)
a1={"n_pairs":len(pairs),"disrupted_mean_pct":round(pairs.disrupted_pct.mean(),2),
    "recovery_mean_pct":round(pairs.recovery_pct.mean(),2),
    "mean_gain_pts":round((pairs.recovery_pct-pairs.disrupted_pct).mean(),2),
    "wilcoxon_W":round(float(w_stat),2),"p_value":round(float(w_p),4)}
pd.DataFrame([a1]).to_csv(os.path.join(RES,"analysis1_recovery.csv"),index=False)
pairs.to_csv(os.path.join(RES,"analysis1_matched_pairs.csv"),index=False)
print("=== ANALYSIS 1: Within-subject recovery (PRIMARY) ===")
for k,v in a1.items(): print(f"  {k}: {v}")

# ANALYSIS 2 - prevalence with Wilson CI
rows=[]
for exam in EXAM_ORDER:
    sub=inst[inst.exam==exam]
    n_sub=int((sub.blank_ratio>=SUBSTANTIAL).sum())
    n_complete=int((sub.blank_ratio==1.0).sum())
    lo,hi=proportion_confint(n_sub,len(sub),method="wilson")
    rows.append({"exam":exam,"n_students":len(sub),"substantial_disruption":n_sub,
                 "complete_disconnection":n_complete,"rate_pct":round(100*n_sub/len(sub),1),
                 "ci95_low":round(100*lo,1),"ci95_high":round(100*hi,1)})
prev=pd.DataFrame(rows); prev.to_csv(os.path.join(RES,"analysis2_prevalence.csv"),index=False)
print("\n=== ANALYSIS 2: Disruption prevalence (substantial, Wilson CI) ===")
print(prev.to_string(index=False))

# ANALYSIS 3 - complete disconnection
cd=inst[inst.blank_ratio==1.0].copy(); cdd=cd[cd.duration_min.notna()]
a3={"complete_instances":len(cd),"unique_students":int(cd.student.nunique()),
    "exams_spanned":int(cd.exam.nunique()),
    "mean_duration_min_with_zero_answers":round(cdd.duration_min.mean(),1),
    "median_duration_min":round(cdd.duration_min.median(),1)}
pd.DataFrame([a3]).to_csv(os.path.join(RES,"analysis3_complete_disconnection.csv"),index=False)
print("\n=== ANALYSIS 3: Complete disconnection signature ===")
for k,v in a3.items(): print(f"  {k}: {v}")

# SUPPORTING cross-sectional
g=inst[inst.score_pct.notna()].copy()
non=g[g.blank_ratio==0]["score_pct"]; dis=g[g.blank_ratio>=SUBSTANTIAL]["score_pct"]
U,p=stats.mannwhitneyu(dis,non,alternative="two-sided")
n1,n2=len(dis),len(non)
psd=np.sqrt(((n1-1)*dis.std()**2+(n2-1)*non.std()**2)/(n1+n2-2))
d=(non.mean()-dis.mean())/psd
print("\n=== SUPPORTING: cross-sectional contrast (corroborative) ===")
print(f"  non n={n2} mean={non.mean():.1f}% | dis n={n1} mean={dis.mean():.1f}% | U={U:.1f} p={p:.2e} d={d:.2f}")
pd.DataFrame([{"non_n":n2,"non_mean":round(non.mean(),2),"dis_n":n1,"dis_mean":round(dis.mean(),2),
    "U":round(U,1),"p_value":f"{p:.2e}","cohens_d":round(d,2)}]).to_csv(
    os.path.join(RES,"analysis4_crosssectional.csv"),index=False)
