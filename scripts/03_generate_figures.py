"""
03_generate_figures.py
Publication-quality figures (no embedded titles; Springer style) for the
strengthened fairness-aware disruption analysis.

Fig 1 - Disruption prevalence by examination (substantial disruption, Wilson 95% CI)
Fig 2 - Within-subject recovery: matched disrupted-final vs supplementary scores
Fig 3 - Complete-disconnection signature: session duration vs questions answered
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

RES = os.path.join(os.path.dirname(__file__), "..", "results")
FIG = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIG, exist_ok=True)

BLUE = "#2E5FA3"
RED = "#C0392B"
GREEN = "#3B7D23"
GREY = "#7F8C8D"

inst = pd.read_csv(os.path.join(RES, "instance_level_features.csv"))
prev = pd.read_csv(os.path.join(RES, "analysis2_prevalence.csv"))
pairs = pd.read_csv(os.path.join(RES, "analysis1_matched_pairs.csv"))

LABELS = {
    "Midterm1": "Midterm 1\n(theory)", "Midterm2_Theory": "Midterm 2\n(theory)",
    "Midterm2_Practical": "Midterm 2\n(practical)", "Final_Theory": "Final\n(theory)",
    "Final_Practical": "Final\n(practical)", "Supp_Theory": "Supp.\n(theory)",
    "Supp_Practical": "Supp.\n(practical)",
}

# ---------------- Figure 1: prevalence with CI ----------------
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("white"); ax.set_facecolor("white")
x = np.arange(len(prev))
rates = prev.rate_pct.values
err_low = rates - prev.ci95_low.values
err_high = prev.ci95_high.values - rates
colors = [RED if "Practical" in e else BLUE for e in prev.exam]
ax.bar(x, rates, color=colors, edgecolor="white", zorder=3, width=0.62)
ax.errorbar(x, rates, yerr=[err_low, err_high], fmt="none",
            ecolor="#34495E", elinewidth=1.3, capsize=4, zorder=4)
for i, r in enumerate(rates):
    ax.text(i, prev.ci95_high.values[i] + 1.5, f"{r:.1f}%", ha="center",
            fontsize=9.5, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels([LABELS[e] for e in prev.exam], fontsize=9.5)
ax.set_ylabel("Substantial disruption rate (%)", fontsize=11)
ax.set_ylim(0, max(prev.ci95_high) + 8)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3, zorder=0)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label="Theory"), Patch(color=RED, label="Practical")],
          fontsize=10, loc="upper left")
plt.tight_layout()
plt.savefig(os.path.join(FIG, "Fig1_prevalence.png"), dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()

# ---------------- Figure 2: within-subject recovery ----------------
fig, ax = plt.subplots(figsize=(8, 5.5))
fig.patch.set_facecolor("white"); ax.set_facecolor("white")
for _, row in pairs.iterrows():
    ax.plot([0, 1], [row.disrupted_pct, row.recovery_pct], "-",
            color=GREY, alpha=0.55, zorder=2, linewidth=1.3)
ax.scatter(np.zeros(len(pairs)), pairs.disrupted_pct, color=RED, s=70,
           zorder=3, label="Disrupted final exam", edgecolors="white")
ax.scatter(np.ones(len(pairs)), pairs.recovery_pct, color=GREEN, s=70,
           zorder=3, label="Supplementary (stable) exam", edgecolors="white")
ax.set_xticks([0, 1])
ax.set_xticklabels(["Disrupted\nexamination", "Supplementary\nrecovery"], fontsize=11)
ax.set_ylabel("Score (%)", fontsize=11)
ax.set_ylim(-5, 108)
ax.set_xlim(-0.3, 1.3)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3)
ax.annotate(f"Mean gain +{(pairs.recovery_pct - pairs.disrupted_pct).mean():.0f} pts\n"
            f"Wilcoxon p = 0.0156",
            xy=(0.5, 50), fontsize=10.5, ha="center",
            bbox=dict(boxstyle="round,pad=0.4", fc="#FCF3CF", ec="#B7950B"))
ax.legend(fontsize=10, loc="center right")
plt.tight_layout()
plt.savefig(os.path.join(FIG, "Fig2_recovery.png"), dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()

# ---------------- Figure 3: complete disconnection ----------------
fig, ax = plt.subplots(figsize=(8.5, 5.5))
fig.patch.set_facecolor("white"); ax.set_facecolor("white")
gr = inst[inst.duration_min.notna()].copy()
gr["answered"] = gr.n_q - gr.n_unanswered
complete = gr[gr.blank_ratio == 1.0]
others = gr[gr.blank_ratio < 1.0]
ax.scatter(others.duration_min, others.answered, s=28, color=BLUE, alpha=0.45,
           edgecolors="none", label="Normal / partial sessions", zorder=2)
ax.scatter(complete.duration_min, complete.answered, s=70, color=RED, alpha=0.85,
           edgecolors="white", label="Complete disconnection (0 answered)", zorder=3)
ax.set_xlabel("Session duration (minutes)", fontsize=11)
ax.set_ylabel("Questions answered", fontsize=11)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(alpha=0.3)
ax.axhline(0, color=RED, linestyle="--", linewidth=0.9, alpha=0.6)
ax.annotate(f"{len(complete)} instances: full-length sessions,\nzero answers transmitted",
            xy=(complete.duration_min.median(), 0),
            xytext=(complete.duration_min.median(), max(gr.answered) * 0.35),
            fontsize=10, ha="center", color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, alpha=0.7))
ax.legend(fontsize=10, loc="upper right")
plt.tight_layout()
plt.savefig(os.path.join(FIG, "Fig3_complete_disconnection.png"), dpi=200,
            bbox_inches="tight", facecolor="white")
plt.close()

print("Saved Fig1_prevalence.png, Fig2_recovery.png, Fig3_complete_disconnection.png")
