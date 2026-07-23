"""
05_write_summary.py   (new in v2.0.0)

Assembles results/ANALYSIS_SUMMARY.json from the individual analysis outputs, so
that the summary can never drift from the CSVs it claims to summarise.

Run last, after scripts 01, 02 and 04.
"""
import json
import os

import pandas as pd

RES = os.path.join(os.path.dirname(__file__), "..", "results")


def read(name):
    return pd.read_csv(os.path.join(RES, name))


inst = read("instance_level_features.csv")

summary = {
    "code_version": "2.0.0",
    "note": ("Supersedes v1.0.0. The cross-sectional contrast and Cohen's d "
             "reported in v1.0.0 were withdrawn; see CHANGELOG.md."),
    "dataset": {
        "total_instances": int(len(inst)),
        "unique_students": int(inst.student.nunique()),
        "sections": int(inst.section.nunique()),
        "exams": int(inst.exam.nunique()),
        "graded_instances": int(inst.score_pct.notna().sum()),
        "instances_with_any_blank": int((inst.blank_ratio > 0).sum()),
        "instances_substantial_disruption": int((inst.blank_ratio >= 0.50).sum()),
    },
    "analysis0_assumption_checks": read("analysis0_assumption_checks.csv").to_dict("records"),
    "analysis1_recovery": read("analysis1_recovery.csv").to_dict("records")[0],
    "analysis2_prevalence": read("analysis2_prevalence.csv").to_dict("records"),
    "analysis3_complete_disconnection": read("analysis3_complete_disconnection.csv").to_dict("records")[0],
    "analysis4_trajectory": read("analysis4_trajectory.csv").to_dict("records"),
    "analysis5_threshold_sensitivity": read("analysis5_threshold_sensitivity.csv").to_dict("records"),
    "analysis6_section_robustness": read("analysis6_section_robustness.csv").to_dict("records"),
    "analysis7_supplementary_structure": read("analysis7_supplementary_structure.csv").to_dict("records")[0],
    "analysis8_route_overlap": read("analysis8_route_overlap.csv").to_dict("records")[0],
}

out = os.path.join(RES, "ANALYSIS_SUMMARY.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1, ensure_ascii=False)

print(f"wrote {out}")
print(f"  dataset: {summary['dataset']['total_instances']} instances, "
      f"{summary['dataset']['unique_students']} students, "
      f"{summary['dataset']['sections']} sections")
print(f"  analyses included: {len([k for k in summary if k.startswith('analysis')])}")
