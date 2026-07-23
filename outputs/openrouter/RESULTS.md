# Results

All 39 tasks per model, grouped by family. Values are copied from each result JSON's `metrics` and `metadata`; blank cells mean the metric does not apply to that task.

## Open question for the leaderboard maintainers

These runs produce the same per-task result JSONs the leaderboard consumes, but
the step that turns those JSONs into `data.js` scenario values
(`generate_leaderboard_data.py`) is not public. To make new entries comparable
with the board, we need to know:

1. **The `n_v1` subsample** used for the MobLab and Big Five families: its
   definition (which subjects/rows per task, or the seed plus sampling code),
   and whether it subsamples the prompts, the human reference distributions,
   or both. The runs below use the full test files everywhere.
2. **The task-to-column aggregation**: which metric variant feeds each
   `data.js` column (e.g. normalized vs raw MAE) and which tasks average into
   each scenario.
3. Alternatively, and simplest: **could these result JSONs be run through
   `generate_leaderboard_data.py` directly?**

(The ranking math after `data.js` — mean win rate, ELO — is client-side
JavaScript on the leaderboard page and fully reproducible.)

## Summary — family means, side by side

Raw per-family metric means computed from the section tables below (not the
leaderboard's mean-win-rate aggregation; see note). Arrows give the better
direction.

| family (metric) | glm-5.2 (default) | hy3 | glm-5.2 no-reasoning |
|---|---|---|---|
| game Wasserstein ↓ | 20.42 | 29.49 | **19.92** |
| acrossgame MAE ↓ | **25.74** | 30.28 | 27.78 |
| multiround MAE ↓ | 18.85 | **18.46** | 20.00 |
| big_five MAE ↓ | 4.59 | 4.79 | **4.45** |
| strategic win rate ↑ | **0.156** | 0.098 | 0.143 |
| economics accuracy ↑ | **0.911** | 0.831 | 0.774 |
| workflow BLEURT ↑ | 0.458 | 0.443 | 0.458 |

A `moonshotai/kimi-k3` run is pending (smoke-tested only; see Runs and cost)
and will slot in between hy3 and the no-reasoning column. The no-reasoning variant is a non-default side run, kept
for the reasoning-effect comparison.

Note on leaderboard comparability: the public leaderboard summarizes with
HELM-style mean win rate / ELO over per-scenario columns (Individual /
Distributional), not family-mean raw metrics, and its MobLab and BigFive
numbers are computed on its own `n_v1` subsample of the test data (IEO and
workflow are full-set). The runs here use the full test files everywhere, so
the two sets of numbers are computed on slightly different data (see the
open question above).

## Runs and cost

| model | what ran | date | tokens (prompt / completion) | cost |
|---|---|---|---|---|
| `z-ai/glm-5.2` (default, reasoning on) | full benchmark: 39 tasks, full test files | 2026-07-23 | 8.2M / 13.5M (10.8M reasoning) | ≈$40 |
| `tencent/hy3` | full benchmark: 39 tasks, full test files | 2026-07-19 | 8.3M / 0.6M | $1.38 |
| `moonshotai/kimi-k3` | **smoke test only**: 5 calls, dictator task, default settings | 2026-07-23 | 830 / 2.4k | full run estimated **$220–570** — very verbose reasoner (485 completion tokens/call, 2.7x GLM-5.2's rate); pending go/no-go |
| `z-ai/glm-5.2-no-reasoning` (`--reasoning-effort none`) | full benchmark: 39 tasks, full test files | 2026-07-22 | 8.0M / 2.9M | ≈$13.5 |

## `z-ai/glm-5.2` — default settings (reasoning on)

Provider-default inference settings, matching the paper convention; GLM-5.2 reasons by default. Full detail in [`z-ai/glm-5.2/`](z-ai/glm-5.2).

### game_behavior

*Model plays the game; scored against the human distribution.*

| task | Wasserstein | KS stat | KS pass | n | parse fails | model mean | model SD | human mean | human SD |
|---|---|---|---|---|---|---|---|---|---|
| `bomb` | 17.72 | 0.525 | 0 | 1000 | 0 | 50 | 0 | 45.56 | 23.09 |
| `dictator` | 18.97 | 0.592 | 0 | 1000 | 0 | 43.68 | 16.87 | 24.71 | 19.19 |
| `guessing` | 17.03 | 0.605 | 0 | 1000 | 0 | 19.13 | 6.701 | 35.47 | 21.51 |
| `public_goods` | 20.25 | 0.434 | 0 | 1000 | 0 | 9.564 | 2.615 | 8.91 | 6.069 |
| `push_pull` | 47.7 | 0 | 1 | 1000 | 0 | 0.093 | 0.2904 | 0.57 | 0.4951 |
| `trust_banker` | 19.35 | 0.52 | 0 | 1000 | 0 | 82.18 | 24.51 | 55.9 | 37.4 |
| `trust_investor` | 20.26 | 0.292 | 0 | 1000 | 0 | 41.74 | 27.65 | 42.19 | 39.89 |
| `ultimatum_proposer` | 7.633 | 0.182 | 0 | 1000 | 0 | 45.33 | 5.796 | 44.92 | 18.33 |
| `ultimatum_responder` | 14.83 | 0.501 | 0 | 1000 | 0 | 18.55 | 10.48 | 33.29 | 17.8 |

### acrossgame_behavior

*Predict a player's action in one game from their behaviour in others.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|---|
| `bomb` | 18.08 | 18.08 | 16.62 | 0.436 | 0 | 0.02153 |  |  | 750 | 0 |
| `dictator` | 21.64 | 21.64 | 8.712 | 0.26 | 0 | -0.02062 |  |  | 750 | 0 |
| `guessing` | 19.92 | 19.92 | 18.39 | 0.5093 | 0 | 0.02407 |  |  | 750 | 0 |
| `public_goods` | 25.93 | 5.185 | 15.61 | 0.2187 | 0 | 0.08791 |  |  | 750 | 0 |
| `push_pull` | 54.4 | 0.544 | 50.13 | 0 | 1 |  | 0.456 | 0.3649 | 750 | 0 |
| `trust_banker` | 25.65 | 38.47 | 17 | 0.5267 | 0 | 0.01629 |  |  | 262 | 0 |
| `trust_investor` | 35.96 | 35.96 | 21.98 | 0.3333 | 0 | 0.03708 |  |  | 750 | 0 |
| `ultimatum_proposer` | 13.29 | 13.29 | 6.565 | 0.1295 | 0 | 0.234 |  |  | 750 | 1 |
| `ultimatum_responder` | 16.79 | 16.79 | 13.23 | 0.4853 | 0 | 0.2947 |  |  | 750 | 0 |

### multiround_behavior

*Predict a specific player's next action across rounds.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|---|
| `bomb` | 16.5 | 16.5 | 16.23 | 0.4449 | 0 | 0.2381 |  |  | 500 | 1 |
| `dictator` | 10.27 | 10.27 | 3.592 | 0.086 | 0 | 0.6581 |  |  | 500 | 0 |
| `guessing` | 11.12 | 11.12 | 8.866 | 0.238 | 0 | 0.623 |  |  | 500 | 0 |
| `public_goods` | 24.31 | 4.862 | 16.77 | 0.228 | 0 | 0.4207 |  |  | 500 | 0 |
| `push_pull` | 30.4 | 0.304 | 4.4 | 0 | 1 |  | 0.696 | 0.6793 | 500 | 0 |
| `trust_banker_inv100` | 11.97 | 35.9 | 7.893 | 0.1847 | 0 | 0.5237 |  |  | 498 | 0 |
| `trust_banker_inv50` | 22.37 | 33.55 | 19.95 | 0.472 | 0 | 0.277 |  |  | 125 | 0 |
| `trust_investor` | 23.85 | 23.85 | 3.198 | 0.032 | 1 | 0.5402 |  |  | 500 | 0 |

### big_five

*Personality / survey-response prediction.*

| task | MAE | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|
| `acrossdim_pers_score` | 7.397 | 4.512 | 0.2873 | 0 | 0.2873 |  |  | 1000 | 31 |
| `demo_pred_age` | 10.52 | 4.266 | 0.2402 | 0 | 0.1812 |  |  | 1000 | 1 |
| `missing_surv_resp` | 0.7735 | 0.3841 | 0 | 1 | 0.502 | 0.4594 | 0.3667 | 1000 | 3 |
| `pers_score_pred` | 6.957 | 5.472 | 0.3545 | 0 | 0.1216 |  |  | 1000 | 0 |
| `seq_surv_resp` | 0.8475 | 0.4539 | 0 | 1 | 0.4088 | 0.4116 | 0.3344 | 1000 | 0 |
| `surv_resp_pred` | 1.016 | 0.7652 | 0 | 1 | 0.02905 | 0.2703 | 0.1236 | 1000 | 2 |

### strategic_gameplay

*Head-to-head strategic play.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Win rate | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|
| `guessing` | 5.057 | 5.057 | 1.801 | 0.04614 | 1 | 0.5214 | 0.1565 | 1000 | 3 |

### economics

*Economics-olympiad multiple choice.*

| task | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|
| `economics` | 0.9113 | 0.7376 | 124 | 1 |

### workflow

*Free-text research-workflow generation (BLEURT / ROUGE).*

| task | BLEURT | ROUGE-1 | n | parse fails |
|---|---|---|---|---|
| `idea_generation` | 0.4053 | 0.2813 | 244 | 0 |
| `impact_prediction` | 0.4709 | 0.2469 | 116 | 0 |
| `method_recommendation` | 0.3926 | 0.3079 | 240 | 0 |
| `outcome_prediction` | 0.5271 | 0.396 | 240 | 0 |
| `title_prediction` | 0.4948 | 0.5138 | 244 | 0 |
## `tencent/hy3`

Provider-default settings. Full detail, including every per-sample prompt and model response, is in [`tencent/hy3/`](tencent/hy3).

### game_behavior

*Model plays the game; scored against the human distribution.*

| task | Wasserstein | KS stat | KS pass | n | parse fails | model mean | model SD | human mean | human SD |
|---|---|---|---|---|---|---|---|---|---|
| `bomb` | 14.3 | 0.503 | 0 | 1000 | 0 | 57.14 | 19.72 | 45.56 | 23.09 |
| `dictator` | 25.51 | 0.807 | 0 | 1000 | 0 | 49.76 | 2.478 | 24.71 | 19.19 |
| `guessing` | 35.03 | 0.881 | 0 | 1000 | 0 | 0.437 | 1.464 | 35.47 | 21.51 |
| `public_goods` | 24.06 | 0.506 | 0 | 1000 | 0 | 9.943 | 0.8554 | 8.91 | 6.069 |
| `push_pull` | 50.3 | 0 | 1 | 1000 | 0 | 0.067 | 0.25 | 0.57 | 0.4951 |
| `trust_banker` | 22.44 | 0.595 | 0 | 1000 | 0 | 75.16 | 6.272 | 55.9 | 37.4 |
| `trust_investor` | 52.38 | 0.6348 | 0 | 998 | 2 | 94.57 | 16.23 | 42.19 | 39.89 |
| `ultimatum_proposer` | 13.56 | 0.499 | 0 | 1000 | 0 | 39.99 | 2.214 | 44.92 | 18.33 |
| `ultimatum_responder` | 27.81 | 0.68 | 0 | 1000 | 0 | 5.571 | 7.13 | 33.29 | 17.8 |

### acrossgame_behavior

*Predict a player's action in one game from their behaviour in others.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|---|
| `bomb` | 33.47 | 33.47 | 22.48 | 0.4387 | 0 | -0.02251 |  |  | 750 | 0 |
| `dictator` | 24.76 | 24.76 | 23.37 | 0.7653 | 0 | 0.03312 |  |  | 750 | 0 |
| `guessing` | 23.34 | 23.34 | 15.91 | 0.3453 | 0 | 0.07299 |  |  | 750 | 0 |
| `public_goods` | 28.31 | 5.661 | 11.19 | 0.3813 | 0 | 0.1127 |  |  | 750 | 0 |
| `push_pull` | 55.2 | 0.552 | 53.07 | 0 | 1 |  | 0.448 | 0.3378 | 750 | 0 |
| `trust_banker` | 22.65 | 33.98 | 20.26 | 0.5153 | 0 | -0.0288 |  |  | 262 | 0 |
| `trust_investor` | 49.73 | 49.73 | 37.59 | 0.4973 | 0 | -0.06324 |  |  | 750 | 0 |
| `ultimatum_proposer` | 15.05 | 15.05 | 8.912 | 0.204 | 0 | 0.2346 |  |  | 750 | 0 |
| `ultimatum_responder` | 20.05 | 20.05 | 14.16 | 0.408 | 0 | 0.1308 |  |  | 750 | 0 |

### multiround_behavior

*Predict a specific player's next action across rounds.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|---|
| `bomb` | 17.8 | 17.8 | 6.386 | 0.192 | 0 | 0.3134 |  |  | 500 | 0 |
| `dictator` | 12.12 | 12.12 | 6.33 | 0.138 | 0 | 0.5349 |  |  | 500 | 0 |
| `guessing` | 10.38 | 10.38 | 7.532 | 0.198 | 0 | 0.6495 |  |  | 500 | 0 |
| `public_goods` | 18.22 | 3.644 | 4.2 | 0.06 | 1 | 0.57 |  |  | 500 | 0 |
| `push_pull` | 29.8 | 0.298 | 2.6 | 0 | 1 |  | 0.702 | 0.673 | 500 | 0 |
| `trust_banker_inv100` | 15.38 | 46.14 | 10.63 | 0.245 | 0 | 0.3565 |  |  | 498 | 0 |
| `trust_banker_inv50` | 20.03 | 30.05 | 18.3 | 0.376 | 0 | 0.3225 |  |  | 125 | 0 |
| `trust_investor` | 23.97 | 23.97 | 6.92 | 0.154 | 0 | 0.5133 |  |  | 500 | 0 |

### big_five

*Personality / survey-response prediction.*

| task | MAE | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|
| `acrossdim_pers_score` | 7.88 | 5.05 | 0.3043 | 0 | 0.1924 |  |  | 1000 | 0 |
| `demo_pred_age` | 10.94 | 5.018 | 0.231 | 0 | 0.06284 |  |  | 1000 | 0 |
| `missing_surv_resp` | 0.7893 | 0.4407 | 0 | 1 | 0.5086 | 0.4597 | 0.3561 | 1000 | 0 |
| `pers_score_pred` | 7.19 | 5.946 | 0.3625 | 0 | 0.07357 |  |  | 1000 | 0 |
| `seq_surv_resp` | 0.8879 | 0.4619 | 0 | 1 | 0.3876 | 0.417 | 0.3244 | 1000 | 0 |
| `surv_resp_pred` | 1.025 | 0.8365 | 0 | 1 | 0.05813 | 0.2736 | 0.1136 | 1000 | 0 |

### strategic_gameplay

*Head-to-head strategic play.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Win rate | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|
| `guessing` | 11.74 | 11.74 | 9.625 | 0.449 | 0 | -0.1602 | 0.098 | 1000 | 0 |

### economics

*Economics-olympiad multiple choice.*

| task | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|
| `ieo_economics` | 0.8306 | 0.8244 | 124 | 0 |

### workflow

*Free-text research-workflow generation (BLEURT / ROUGE).*

| task | BLEURT | ROUGE-1 | n | parse fails |
|---|---|---|---|---|
| `idea_generation` | 0.4066 | 0.2816 | 244 | 0 |
| `impact_prediction` | 0.4348 | 0.253 | 116 | 0 |
| `method_recommendation` | 0.4403 | 0.3564 | 240 | 0 |
| `outcome_prediction` | 0.5063 | 0.4109 | 240 | 0 |
| `title_prediction` | 0.4276 | 0.4482 | 244 | 0 |

## `z-ai/glm-5.2` — reasoning disabled

Run with `--reasoning-effort none` (GLM-5.2 reasons by default; disabled here for cross-model consistency). Full detail in [`z-ai/glm-5.2-no-reasoning/`](z-ai/glm-5.2-no-reasoning).

### game_behavior

*Model plays the game; scored against the human distribution.*

| task | Wasserstein | KS stat | KS pass | n | parse fails | model mean | model SD | human mean | human SD |
|---|---|---|---|---|---|---|---|---|---|
| `bomb` | 7.999 | 0.218 | 0 | 1000 | 0 | 38.94 | 19.51 | 45.56 | 23.09 |
| `dictator` | 39.56 | 0.631 | 0 | 1000 | 0 | 64.28 | 37.86 | 24.71 | 19.19 |
| `guessing` | 17.51 | 0.491 | 0 | 1000 | 0 | 17.95 | 11.47 | 35.47 | 21.51 |
| `public_goods` | 13.88 | 0.129 | 0 | 1000 | 0 | 8.311 | 3.436 | 8.91 | 6.069 |
| `push_pull` | 48.4 | 0 | 1 | 1000 | 0 | 0.086 | 0.2804 | 0.57 | 0.4951 |
| `trust_banker` | 12.59 | 0.453 | 0 | 1000 | 0 | 73.38 | 30.5 | 55.9 | 37.4 |
| `trust_investor` | 16.63 | 0.294 | 0 | 1000 | 0 | 31.31 | 26.16 | 42.19 | 39.89 |
| `ultimatum_proposer` | 11.67 | 0.453 | 0 | 1000 | 0 | 49.67 | 1.578 | 44.92 | 18.33 |
| `ultimatum_responder` | 11.01 | 0.497 | 0 | 1000 | 0 | 28.57 | 8.052 | 33.29 | 17.8 |

### acrossgame_behavior

*Predict a player's action in one game from their behaviour in others.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|---|
| `bomb` | 27.16 | 27.16 | 10.94 | 0.2336 | 0 | -0.02293 |  |  | 750 | 1 |
| `dictator` | 24.1 | 24.1 | 20.45 | 0.656 | 0 | 0.02908 |  |  | 750 | 0 |
| `guessing` | 21.15 | 21.15 | 16.37 | 0.4573 | 0 | -0.03811 |  |  | 750 | 0 |
| `public_goods` | 26.78 | 5.356 | 11.34 | 0.124 | 0 | 0.1043 |  |  | 750 | 0 |
| `push_pull` | 55.33 | 0.5533 | 48.93 | 0 | 1 |  | 0.4467 | 0.3607 | 750 | 0 |
| `trust_banker` | 24.76 | 37.15 | 18.03 | 0.5496 | 0 | 0.009275 |  |  | 262 | 0 |
| `trust_investor` | 39.06 | 39.06 | 12.64 | 0.227 | 0 | -0.000219 |  |  | 750 | 1 |
| `ultimatum_proposer` | 14.03 | 14.03 | 4.857 | 0.1 | 0 | 0.1902 |  |  | 750 | 0 |
| `ultimatum_responder` | 17.65 | 17.65 | 13.74 | 0.4813 | 0 | 0.2628 |  |  | 750 | 0 |

### multiround_behavior

*Predict a specific player's next action across rounds.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|---|
| `bomb` | 17.17 | 17.17 | 6.342 | 0.166 | 0 | 0.2953 |  |  | 500 | 0 |
| `dictator` | 14.53 | 14.53 | 8.906 | 0.24 | 0 | 0.4754 |  |  | 500 | 0 |
| `guessing` | 11.05 | 11.05 | 8.422 | 0.216 | 0 | 0.6143 |  |  | 500 | 0 |
| `public_goods` | 19.87 | 3.974 | 8.11 | 0.102 | 0 | 0.5355 |  |  | 500 | 0 |
| `push_pull` | 36.2 | 0.362 | 16.2 | 0 | 1 |  | 0.638 | 0.6336 | 500 | 0 |
| `trust_banker_inv100` | 15.1 | 45.31 | 7.044 | 0.1767 | 0 | 0.3963 |  |  | 498 | 0 |
| `trust_banker_inv50` | 22.18 | 33.26 | 14.86 | 0.4 | 0 | 0.2418 |  |  | 125 | 0 |
| `trust_investor` | 23.87 | 23.87 | 5.584 | 0.082 | 1 | 0.5044 |  |  | 500 | 0 |

### big_five

*Personality / survey-response prediction.*

| task | MAE | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|
| `acrossdim_pers_score` | 7.422 | 3.751 | 0.2134 | 0 | 0.2079 |  |  | 1000 | 9 |
| `demo_pred_age` | 9.651 | 4.872 | 0.2613 | 0 | 0.1284 |  |  | 1000 | 1 |
| `missing_surv_resp` | 0.7859 | 0.4059 | 0 | 1 | 0.4824 | 0.4567 | 0.3553 | 1000 | 2 |
| `pers_score_pred` | 6.97 | 5.355 | 0.3174 | 0 | 0.09751 |  |  | 1000 | 0 |
| `seq_surv_resp` | 0.8671 | 0.4177 | 0 | 1 | 0.4387 | 0.3973 | 0.3144 | 1000 | 0 |
| `surv_resp_pred` | 1.027 | 0.7535 | 0 | 1 | 0.02934 | 0.276 | 0.1269 | 1000 | 0 |

### strategic_gameplay

*Head-to-head strategic play.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Win rate | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|
| `guessing` | 7.256 | 7.256 | 3.926 | 0.1311 | 0 | 0.3047 | 0.1431 | 1000 | 1 |

### economics

*Economics-olympiad multiple choice.*

| task | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|
| `economics` | 0.7742 | 0.6322 | 124 | 1 |

### workflow

*Free-text research-workflow generation (BLEURT / ROUGE).*

| task | BLEURT | ROUGE-1 | n | parse fails |
|---|---|---|---|---|
| `idea_generation` | 0.407 | 0.2828 | 244 | 0 |
| `impact_prediction` | 0.4565 | 0.2494 | 116 | 0 |
| `method_recommendation` | 0.4292 | 0.342 | 240 | 0 |
| `outcome_prediction` | 0.5178 | 0.3901 | 240 | 0 |
| `title_prediction` | 0.479 | 0.5053 | 244 | 0 |

