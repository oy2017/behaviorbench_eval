# Results — `tencent/hy3`

All 39 tasks, grouped by family. Values are copied from each result JSON's `metrics` and `metadata`.

Blank cells mean the metric does not apply to that task. Full detail, including every per-sample prompt and model response, is in [`tencent/hy3/`](tencent/hy3).


## game_behavior

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

## acrossgame_behavior

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

## multiround_behavior

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

## big_five

*Personality / survey-response prediction.*

| task | MAE | Wasserstein | KS stat | KS pass | Spearman | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|
| `acrossdim_pers_score` | 7.88 | 5.05 | 0.3043 | 0 | 0.1924 |  |  | 1000 | 0 |
| `demo_pred_age` | 10.94 | 5.018 | 0.231 | 0 | 0.06284 |  |  | 1000 | 0 |
| `missing_surv_resp` | 0.7893 | 0.4407 | 0 | 1 | 0.5086 | 0.4597 | 0.3561 | 1000 | 0 |
| `pers_score_pred` | 7.19 | 5.946 | 0.3625 | 0 | 0.07357 |  |  | 1000 | 0 |
| `seq_surv_resp` | 0.8879 | 0.4619 | 0 | 1 | 0.3876 | 0.417 | 0.3244 | 1000 | 0 |
| `surv_resp_pred` | 1.025 | 0.8365 | 0 | 1 | 0.05813 | 0.2736 | 0.1136 | 1000 | 0 |

## strategic_gameplay

*Head-to-head strategic play.*

| task | MAE | MAE (raw) | Wasserstein | KS stat | KS pass | Spearman | Win rate | n | parse fails |
|---|---|---|---|---|---|---|---|---|---|
| `guessing` | 11.74 | 11.74 | 9.625 | 0.449 | 0 | -0.1602 | 0.098 | 1000 | 0 |

## economics

*Economics-olympiad multiple choice.*

| task | Accuracy | F1 macro | n | parse fails |
|---|---|---|---|---|
| `ieo_economics` | 0.8306 | 0.8244 | 124 | 0 |

## workflow

*Free-text research-workflow generation (BLEURT / ROUGE).*

| task | BLEURT | ROUGE-1 | n | parse fails |
|---|---|---|---|---|
| `idea_generation` | 0.4066 | 0.2816 | 244 | 0 |
| `impact_prediction` | 0.4348 | 0.253 | 116 | 0 |
| `method_recommendation` | 0.4403 | 0.3564 | 240 | 0 |
| `outcome_prediction` | 0.5063 | 0.4109 | 240 | 0 |
| `title_prediction` | 0.4276 | 0.4482 | 244 | 0 |
