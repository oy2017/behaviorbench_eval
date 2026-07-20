#!/usr/bin/env python3
"""Build summary.csv from the raw BehaviorBench result JSONs in tencent/hy3/.

Every number in README.md and FINDINGS.md comes from this script reading the
committed raw JSONs -- nothing is hand-entered. Re-run to verify:

    python3 outputs/openrouter/make_summary.py

Metric keys vary by task family. Files covering several sub-tasks expose
``<metric>_averaged``; single-task files expose the bare key. We prefer the
averaged form when present and fall back to the bare key.
"""
import csv
import glob
import json
import os
import re

RAW_DIR = os.path.join(os.path.dirname(__file__), "tencent", "hy3")
OUT_CSV = os.path.join(os.path.dirname(__file__), "summary.csv")

FAMILIES = [
    ("acrossgame_behavior", "acrossgame_behavior"),
    ("multiround_behavior", "multiround_behavior"),
    ("game_behavior", "game_behavior"),
    ("strategic_gameplay", "strategic_gameplay"),
    ("workflow", "workflow"),
    ("ieo_economics", "economics"),
]
# Remaining prediction tasks form the big_five / survey family.
BIG_FIVE = {
    "acrossdim_pers_score", "demo_pred_age", "missing_surv_resp",
    "pers_score_pred", "seq_surv_resp", "surv_resp_pred",
}


def family_of(task):
    for prefix, fam in FAMILIES:
        if task.startswith(prefix):
            return fam
    if task in BIG_FIVE:
        return "big_five"
    return "other"


def pick(metrics, *names):
    """Return the first present metric, preferring the _averaged variant."""
    for n in names:
        if n + "_averaged" in metrics:
            return metrics[n + "_averaged"]
        if n in metrics:
            return metrics[n]
    return None


def main():
    rows = []
    for fn in sorted(glob.glob(os.path.join(RAW_DIR, "*.json"))):
        d = json.load(open(fn))
        for task in d["tasks"]:
            name = task["task_name"]
            m = task.get("metrics") or d["metrics"].get(name, {})
            meta = task.get("metadata", {})
            rows.append({
                "family": family_of(name),
                "task": name,
                "n_model": meta.get("num_model_samples") or meta.get("num_samples") or len(task.get("predictions") or []),
                "n_human": meta.get("num_human_samples", ""),
                "parse_fails": meta.get("num_failed_parses", ""),
                # Two MAE variants exist. ``_mae`` is normalised onto a common
                # scale; ``_mae_raw`` is in each game's native units. Family
                # averages MUST use the normalised form -- games have different
                # action scales (push_pull is binary, trust_banker runs 0-100+),
                # so averaging raw values across games sums incommensurable
                # units and is dominated by whichever game has the largest ones.
                "MAE": pick(m, "MAE_with_normalization_mae", "MAE"),
                "MAE_raw": pick(m, "MAE_with_normalization_mae_raw"),
                "W": pick(m, "Wasserstein_with_ks_distance"),
                "ks_pass": pick(m, "Wasserstein_with_ks_ks_pass_test", "Wasserstein_with_ks_all_ks_pass_test"),
                "spearman": pick(m, "Spearman_with_pvalue_correlation"),
                "accuracy": pick(m, "accuracy_multi_choice", "Accuracy"),
                "win_rate": pick(m, "win_rate"),
                "BLEURT": pick(m, "BLEURT"),
                "ROUGE_1": pick(m, "ROUGE-1"),
                "model_mean": meta.get("model_action_mean", ""),
                "model_sd": meta.get("model_action_std", ""),
                "human_mean": meta.get("human_action_mean", ""),
                "human_sd": meta.get("human_action_std", ""),
                "source_file": os.path.basename(fn),
            })

    rows.sort(key=lambda r: (r["family"], r["task"]))
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT_CSV}  ({len(rows)} task rows)")

    # Family roll-up, printed so README numbers can be checked against it.
    def avg(vals):
        vals = [v for v in vals if isinstance(v, (int, float))]
        return sum(vals) / len(vals) if vals else None

    fams = {}
    for r in rows:
        fams.setdefault(r["family"], []).append(r)
    print(f"\n{'family':<22}{'tasks':>6}{'MAE(norm)':>11}{'MAE(raw)':>10}{'W':>9}{'acc':>8}{'BLEURT':>9}")
    print("-" * 76)
    for fam, rs in sorted(fams.items()):
        def fmt(v):
            return f"{v:.3f}" if isinstance(v, float) else "-"
        print(f"{fam:<22}{len(rs):>6}{fmt(avg([r['MAE'] for r in rs])):>11}"
              f"{fmt(avg([r['MAE_raw'] for r in rs])):>10}"
              f"{fmt(avg([r['W'] for r in rs])):>9}{fmt(avg([r['accuracy'] for r in rs])):>8}"
              f"{fmt(avg([r['BLEURT'] for r in rs])):>9}")
    tot = sum(r["parse_fails"] for r in rows if isinstance(r["parse_fails"], int))
    print("-" * 63)
    print(f"total parse failures across all tasks: {tot}")


if __name__ == "__main__":
    main()
