# BehaviorBench evaluation — `tencent/hy3`

A full-sample run of the BehaviorBench suite against **Tencent Hunyuan 3 (`tencent/hy3`)**,
served through OpenRouter. Tencent is not in the paper's leaderboard, so this extends
coverage to a Chinese lab that was previously unrepresented.

Everything here is reproducible from the committed files: raw per-task JSONs are in
[`tencent/hy3/`](tencent/hy3), the run script is [`run_full.sh`](run_full.sh), and every
number below is computed by [`make_summary.py`](make_summary.py) reading those JSONs.

---

## 1. What was run

| | |
|---|---|
| **Model** | `tencent/hy3` (paid tier) |
| **Provider** | OpenRouter, OpenAI-compatible endpoint |
| **Tasks** | **39 / 39** — all families, no task skipped |
| **Samples** | `game_behavior` **n=1000 per game**; prediction & big_five = **full datasets**; workflow = full |
| **Sampling** | provider defaults (`temperature`, `top_p`, `top_k`, `min_p` all unset), `max_tokens=16384` |
| **Concurrency** | 4 |
| **Date** | 2026-07-19 |
| **Cost** | **$1.38** for ~27,000 requests |
| **Failures** | 0 failed tasks; **2 parse failures** across ~27k requests (0.007%) |
| **Code version** | commit `690c1b6` (includes the `--model-type openai` endpoint fix, PR #1) |

Reproduce with:

```bash
bash outputs/openrouter/run_full.sh           # ~4h, ~$1.40
python3 outputs/openrouter/make_summary.py    # regenerates summary.csv from the raw JSONs
```

> **Note on the code version.** `--model-type openai` was broken before commit `690c1b6`
> — it built an Azure client pointed at localhost and failed every call. That fix
> ([PR #1](https://github.com/umich-foreseer/behaviorbench_eval/pull/1)) is what made this
> run possible; earlier code cannot reproduce it.

---

## 2. Headline results

| family | tasks | MAE (normalised) | Wasserstein | accuracy | BLEURT |
|---|---:|---:|---:|---:|---:|
| game_behavior | 9 | — | **29.49** | — | — |
| acrossgame_behavior | 9 | 30.28 | 22.99 | 0.448 | — |
| multiround_behavior | 8 | 18.46 | 7.86 | 0.702 | — |
| big_five | 6 | 4.79 | 2.96 | 0.383 | — |
| strategic_gameplay | 1 | 11.75 | 9.63 | — | — |
| economics (ieo) | 1 | — | — | **0.831** | — |
| workflow (free-text) | 5 | — | — | — | **0.443** |

Per-task numbers, including model-vs-human means and standard deviations, are in
[`summary.csv`](summary.csv).

> **Which MAE?** Two variants appear in the raw JSONs: `MAE_with_normalization_mae`
> (normalised to a common scale) and `..._mae_raw` (each game's native units). Family
> averages here use the **normalised** form, because games have different action scales
> — `push_pull` is effectively binary while `trust_banker` runs 0–100+ — so averaging raw
> values across games sums incommensurable units. Both columns are in `summary.csv` so
> either convention can be checked. The raw-unit averages, for reference, are
> acrossgame **22.95** and multiround **18.05**.

---

## 3. Main finding: hy3 predicts human behaviour well, but does not reproduce it

The split across task types is stark:

- **Predicting** what a person will do — `multiround` MAE 18.5, `economics` accuracy 0.831,
  `big_five` MAE 4.79 — is solid.
- **Behaving** like a population of people — `game_behavior` Wasserstein **29.49** — sits at
  the weak end of the paper's reported range (7.0–31.4).

The cause is visible in the raw output. Averaged across all nine games:

| | model SD | human SD |
|---|---:|---:|
| mean across 9 games | **6.29** | **20.42** |

hy3 produces roughly **a third** of human behavioural variance, and its central tendency is
often far off. In the dictator game, 1000 independent samples of the identical prompt gave
**$50 in 98.1% of cases** — 5 distinct values and 13 distinct output strings across 1000
samples — against a human mean of $24.71 (SD 19.19).

Full analysis, including the per-game breakdown and the two distinct failure modes
(distributional collapse, and playing game-theoretic equilibria where humans do not), is in
**[FINDINGS.md](FINDINGS.md)**.

---

## 4. How this compares to the paper (arXiv 2606.24162)

Directional only — see the caveat below.

- **game_behavior W 29.49** → high/weak end of the paper's 7.0–31.4 range; specialised
  behavioural models (Be.FM) lead at ~7.
- **economics accuracy 0.831** → above Be.FM-70B (0.73), below the strongest proprietary
  models (0.956).
- **workflow BLEURT 0.443** → inside the strong-model band (0.43–0.47).
- Overall shape matches the paper's thesis: general-purpose models do well on knowledge and
  individual-level prediction, and poorly on distributional alignment.

> **Caveat on comparability.** The paper's per-family MAE convention (normalised vs raw) and
> its decoding settings have not been confirmed against this run. The Wasserstein, accuracy
> and BLEURT comparisons rest on firmer ground than the MAE ones. Treat all cross-paper
> comparisons as indicative until the paper's exact protocol is verified.

---

## 5. Files

| path | what it is |
|---|---|
| [`tencent/hy3/`](tencent/hy3) | **35 raw result JSONs** — metrics, metadata, and every per-sample prompt / `raw_output` / `parsed_prediction` |
| [`summary.csv`](summary.csv) | per-task table (39 rows) generated from the raw JSONs |
| [`run.log`](run.log) | full run log, task by task |
| [`run_full.sh`](run_full.sh) | the exact script that produced the JSONs |
| [`make_summary.py`](make_summary.py) | builds `summary.csv`; re-run to verify every number above |
| [`FINDINGS.md`](FINDINGS.md) | behavioural analysis of *why* the distributional scores are weak |

Open any JSON in `tencent/hy3/` to check a headline number against the underlying
per-sample model outputs.
