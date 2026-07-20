# BehaviorBench results — `tencent/hy3:free`

Produced by `behaviorbench-eval` via OpenRouter. **Summary below; the raw per-task output JSONs (the proof) are linked at the bottom and browsable in this folder.**

- **Tasks:** 39/39 · **Parse failures:** 0 · **Samples:** game_behavior n=100, others n=25
- ⚠️ Free-tier coverage run, **not** the official 1000-sample benchmark — approximate positioning only.

## Family summary  (MAE / W: lower = closer to humans)

| family | tasks | mean MAE | mean W | other |
|---|---|---|---|---|
| game_behavior | 9 | — | 29.20 |  |
| acrossgame_behavior | 9 | 21.39 | 19.95 |  |
| multiround_behavior | 8 | 16.00 | 8.63 |  |
| big_five | 6 | 5.40 | 3.66 |  |
| strategic_gameplay | 1 | 12.36 | 11.40 | win_rate=0.20 |
| economics | 1 | — | — | accuracy=0.76 |
| workflow (free-text) | 5 | — | — | mean BLEURT=0.441 |

## Per-task

| family | task | n | MAE | W | other |
|---|---|---|---|---|---|
| game_behavior | game_behavior_bomb | 100 | — | 14.91 |  |
| game_behavior | game_behavior_dictator | 100 | — | 25.61 |  |
| game_behavior | game_behavior_guessing | 100 | — | 34.18 |  |
| game_behavior | game_behavior_public_goods | 100 | — | 24.25 |  |
| game_behavior | game_behavior_push_pull | 100 | — | 51.00 |  |
| game_behavior | game_behavior_trust_banker | 100 | — | 22.90 |  |
| game_behavior | game_behavior_trust_investor | 100 | — | 57.81 |  |
| game_behavior | game_behavior_ultimatum_proposer | 100 | — | 13.39 |  |
| game_behavior | game_behavior_ultimatum_responder | 100 | — | 18.76 |  |
| acrossgame_behavior | acrossgame_behavior_bomb | 25 | 25.12 | 15.12 |  |
| acrossgame_behavior | acrossgame_behavior_dictator | 25 | 28.16 | 26.56 |  |
| acrossgame_behavior | acrossgame_behavior_guessing | 25 | 23.08 | 14.20 |  |
| acrossgame_behavior | acrossgame_behavior_public_goods | 25 | 7.12 | 8.00 |  |
| acrossgame_behavior | acrossgame_behavior_push_pull | 25 | 0.44 | 44.00 |  |
| acrossgame_behavior | acrossgame_behavior_trust_banker | 25 | 25.44 | 16.37 |  |
| acrossgame_behavior | acrossgame_behavior_trust_investor | 25 | 42.92 | 26.92 |  |
| acrossgame_behavior | acrossgame_behavior_ultimatum_proposer | 25 | 18.04 | 12.12 |  |
| acrossgame_behavior | acrossgame_behavior_ultimatum_responder | 25 | 22.20 | 16.28 |  |
| multiround_behavior | multiround_behavior_bomb | 25 | 21.52 | 11.60 |  |
| multiround_behavior | multiround_behavior_dictator | 25 | 7.44 | 6.40 |  |
| multiround_behavior | multiround_behavior_guessing | 25 | 13.68 | 10.56 |  |
| multiround_behavior | multiround_behavior_public_goods | 25 | 3.52 | 5.60 |  |
| multiround_behavior | multiround_behavior_push_pull | 25 | 0.24 | 8.00 |  |
| multiround_behavior | multiround_behavior_trust_banker_inv100 | 25 | 27.88 | 5.72 |  |
| multiround_behavior | multiround_behavior_trust_banker_inv50 | 25 | 30.16 | 16.85 |  |
| multiround_behavior | multiround_behavior_trust_investor | 25 | 23.56 | 4.28 |  |
| big_five | acrossdim_pers_score | 25 | 8.49 | 5.14 |  |
| big_five | demo_pred_age | 25 | 13.08 | 6.60 |  |
| big_five | missing_surv_resp | 25 | 0.83 | 0.83 |  |
| big_five | pers_score_pred | 25 | 8.25 | 7.67 |  |
| big_five | seq_surv_resp | 25 | 0.92 | 0.92 |  |
| big_five | surv_resp_pred | 25 | 0.82 | 0.79 |  |
| strategic_gameplay | strategic_gameplay_guessing | 25 | 12.36 | 11.40 | win=0.20 |
| economics | ieo_economics | 25 | — | — | acc=0.76 |
| workflow | workflow_idea_generation | 25 | — | — | BLEURT=0.424 ROUGE1=0.295 |
| workflow | workflow_method_recommendation | 25 | — | — | BLEURT=0.450 ROUGE1=0.369 |
| workflow | workflow_outcome_prediction | 25 | — | — | BLEURT=0.498 ROUGE1=0.406 |
| workflow | workflow_title_prediction | 25 | — | — | BLEURT=0.400 ROUGE1=0.410 |
| workflow | workflow_impact_prediction | 25 | — | — | BLEURT=0.432 ROUGE1=0.248 |

## Raw output (proof)

- [`tencent/hy3:free/`](https://github.com/oy2017/behaviorbench_eval/tree/results/hy3-free/outputs/openrouter/tencent/hy3:free) — every task's full JSON (metrics + metadata + per-sample predictions)
- [`tencent/hy3/`](https://github.com/oy2017/behaviorbench_eval/tree/results/hy3-free/outputs/openrouter/tencent/hy3) — paid smoke output
- Run logs: `free_spread.log`, `deepen.log`, `suite_run.log`, `smoke_all_families.log`
- `summary.csv` — this table as a spreadsheet

Each JSON is exactly what the evaluator wrote — open any one to verify the numbers above against per-sample `raw_output` / `parsed_prediction`.

## Comparison (paper arXiv 2606.24162)
General-purpose model profile: weak distributional game fit (W~29, like other general models; specialized Be.FM lead ~7), but competitive on knowledge/individual tasks (economics 0.76, workflow BLEURT ~0.44). Matches the paper's finding.
