# BehaviorBench results — `tencent/hy3`

Produced by `behaviorbench-eval` via OpenRouter. Raw per-task JSONs (the proof) are in the folders below.

## Full-sample run (paid `tencent/hy3`) — leaderboard-grade

- All 39 tasks, **2 parse failures** across ~27k requests, cost ~$1.38.
- Samples: game_behavior **n=1000**, prediction/big_five = **full datasets**, workflow full.

| family | tasks | mean MAE | mean W | other |
|---|---|---|---|---|
| game_behavior | 9 | — | 29.49 |  |
| acrossgame_behavior | 9 | 22.95 | 22.99 |  |
| multiround_behavior | 8 | 18.05 | 7.86 |  |
| big_five | 6 | 4.79 | 2.96 |  |
| strategic_gameplay | 1 | 11.74 | 9.63 | win_rate=0.10 |
| economics | 1 | — | — | accuracy=0.831 |
| workflow (free-text) | 5 | — | — | mean BLEURT=0.443 |

## How it compares (paper arXiv 2606.24162)
- **Game Wasserstein 29.5** → high/worst end (paper 7.0–31.4; specialized Be.FM lead ~7) — weak distributional fit, as expected for a general model.
- **Multiround MAE 18.0** → ties the paper's best (Be.FM-1.5-70B ≈ 18.0) — strong individual prediction.
- **Economics accuracy 0.831** → above Be.FM-70B (0.73), below top proprietary (0.956).
- **Workflow BLEURT 0.443** → within the strong-model band (0.43–0.47).
- Profile matches the paper's thesis: general-purpose models are strong on knowledge/individual tasks, weaker on distributional alignment.

## Raw output (proof)
- [`tencent/hy3/`](https://github.com/oy2017/behaviorbench_eval/tree/results/hy3-free/outputs/openrouter/tencent/hy3) — full-sample paid run (35 JSONs: metrics + metadata + per-sample predictions)
- [`tencent/hy3:free/`](https://github.com/oy2017/behaviorbench_eval/tree/results/hy3-free/outputs/openrouter/tencent/hy3:free) — earlier free-tier coverage run (n=25–100)
- Run logs: `paid_full.log`, `free_spread.log`, `deepen.log`

Open any JSON to verify the numbers above against per-sample `raw_output` / `parsed_prediction`.
