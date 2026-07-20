# BehaviorBench evaluation — `tencent/hy3`

Full-sample run of the BehaviorBench suite against **Tencent Hunyuan 3 (`tencent/hy3`)** via
OpenRouter. Tencent is not in the paper's leaderboard, so this adds a previously
unrepresented Chinese lab.

| | |
|---|---|
| **📊 Results** | **[`RESULTS.md`](RESULTS.md)** — all 39 tasks in tables |
| **📁 Raw output** | **[`tencent/hy3/`](tencent/hy3)** — 35 result JSONs |
| What was run | [`run_full.sh`](run_full.sh) · [`run.log`](run.log) |

---

## The run

| | |
|---|---|
| **Model** | `tencent/hy3` (paid tier), via OpenRouter |
| **Tasks** | **39 / 39** — all families, none skipped |
| **Samples** | `game_behavior` **n=1000 per game**; prediction & big_five = full datasets; workflow = full |
| **Sampling** | provider defaults (`temperature`, `top_p`, `top_k`, `min_p` unset), `max_tokens=16384` |
| **Concurrency** | 4 |
| **Date** | 2026-07-19 |
| **Cost** | **$1.38** for ~27,000 requests |
| **Failures** | 0 failed tasks; **2 parse failures** across ~27k requests (0.007%) |
| **Code** | commit `690c1b6` |

The tool runs one task per invocation:

```bash
uv run behaviorbench-eval \
  --task game_behavior_dictator \
  --model-type openai \
  --model-name tencent/hy3 \
  --api-base https://openrouter.ai/api/v1 \
  --concurrency 4 \
  --output-dir outputs/openrouter
```

[`run_full.sh`](run_full.sh) is that command looped over all 39 task names, with retry-on-429
and logging so it could run unattended (~4h, ~$1.40).

> `--model-type openai` was broken before commit `690c1b6` — it built an Azure client pointed
> at localhost and failed every call. That fix
> ([PR #1](https://github.com/umich-foreseer/behaviorbench_eval/pull/1)) is what made this run
> possible; earlier code cannot reproduce it.

---

## What's in a result JSON

Per the repo's *Outputs* section, each run writes a timestamped JSON under
`<output-dir>/<model-name>/`. Each contains, per sample:

```json
{
  "prompt":            {"system": "...", "user": "You are paired with another player..."},
  "raw_output":        "I would keep $50 and give the other player [$50].",
  "parsed_prediction": 50.0,
  "expected":          null
}
```

plus `metrics`, `metadata` (sample counts, parse failures, model/human means and SDs),
`inference_settings`, and `token_usage`.

---

## Observations

hy3 does better at **predicting** human behaviour than at **reproducing** it. Prediction
tasks land in a normal range (`ieo_economics` accuracy 0.831, `big_five` MAE ~0.8–11), while
the `game_behavior` family — where the model plays the game itself — fits the human
distribution poorly.

Two things drive it.

**1. Very low behavioural variance.** Mean model SD across the nine games is **6.29** against
a human **20.42**. In the dictator game, across 1000 independent samples of an identical
prompt, the model gave **$50 in 98.1% of cases** — 5 distinct values, 13 distinct output
strings. Humans averaged $24.71 (SD 19.19).

**2. It plays the game-theoretic solution.** Separately, the model's centre often sits at the
rational equilibrium, where humans systematically deviate — `guessing` 0.44 vs 35.47 (Nash is
0), `ultimatum_responder` 5.57 vs 33.29 (accepting tiny offers is rational; humans reject
them), `trust_investor` 94.57 vs 42.19. These games are research instruments precisely
*because* humans deviate, so more sampling diversity would not close these gaps — the centre
is in the wrong place.

The per-game means and SDs behind this are in [`RESULTS.md`](RESULTS.md#game_behavior).

Caveats: the run used provider-default sampling, so how much of point 1 is decoding rather
than the model is untested. Family-level averages are not published — the program reports
metrics per task, and the raw JSONs carry two MAE variants (`MAE_with_normalization_mae`
normalised, `..._mae_raw` in native units) whose family averages differ materially, since
games have different action scales. Aggregate as the paper does.
