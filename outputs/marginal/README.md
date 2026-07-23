# A sampler baseline: how well can these tasks be scored without knowing the person?

*One page — 2026-07-22. Full per-task results (every prompt, answer, and metric) are in
[`marginal-sampler-test/`](marginal-sampler-test/).*

## The idea

Models on BehaviorBench do two things at once: they match what people **in general** do (the
distributional level, scored by Wasserstein distance), and they predict what **one specific
person** will do (the individual level, scored by MAE and accuracy). Today the
individual-level scores are only compared model against model. This note adds a null
baseline — the score of knowing the population but not the person:

- **Marginal sampler** — a pseudo-model that answers each question with a random draw from
  real people's answers to that task (per survey item, per Big Five dimension, per game — the
  same grouping the metrics already use). It runs through the released pipeline unchanged
  (`--model-type marginal`, seed 42, full test files). It knows the population perfectly and
  knows nothing about the person.

How to read it: a model scoring **near the sampler** is doing what the sampler does —
population knowledge, no person knowledge. A model scoring **below** it is not even
reproducing what people answer. A model scoring **well above** it is using more than random
population draws.

**Caveats.** (1) Ideally the answer pool should come from the *training* population. I did not
have the training data, so the pool comes from the released test files, assuming the training
and test populations are close (they come from the same sources, split at random). Happy to
redo this with training-side pools. (2) Push/Pull columns are left out, following the paper's
held-out treatment.

## Results: nine individual-level columns

Leaderboard values from the public site (2026-05-07). Be.FM-1.5-70B = 5-run mean.

| task (metric)                  | sampler | Be.FM-1.5-70B | best on leaderboard | margin over sampler |
|--------------------------------|:-----:|:-------------:|:-------------------:|---|
| Multi-Round Pred. (MAE ↓)      | 28.8 | **16.2** | GPT 4.1 — **16.1** | large |
| Masked Resp. (acc ↑)           | 0.302 | **0.449** | Gemini 3.1 Pro — **0.485** | large |
| Strategic play (win rate ↑)    | 0.079 (a random human's guess) | **0.501** | Be.FM-1.5-70B | large (6× the human rate) |
| Seq. Resp. (acc ↑)             | 0.314 | 0.404 | Gemini 3.1 Pro — 0.425 | moderate |
| Demo. To Pers. (MAE ↓)         | 9.18 | 7.17 | Gemini 3.1 Pro — 6.40 | moderate |
| Across-Dim Pers. (MAE ↓)       | 8.92 | 6.77 | Claude Opus 4.6 — 6.73 | moderate |
| Pers. To Demo. age (MAE ↓)     | 12.34 | 9.38 | Llama3.3-70B — 9.29 | moderate |
| Across-Ctx Pred. (MAE ↓)       | 28.0 | 25.0 | Claude Sonnet 4.6 — 21.6 | small |
| Demo. To Resp. (acc ↑)         | 0.279 | 0.286 | Gemini 3.1 Pro — 0.305 | **none — models ≈ sampler** |

Two patterns stand out:

- **The large margins all occur where the prompt shows the person's own earlier behavior** —
  past rounds of the same game, the person's other questionnaire answers. This is the
  benchmark's strongest demonstrated result: real individual-level prediction.
- **Where the prompt gives only indirect information (e.g. demographics), margins shrink —
  and on Demo. To Resp. they vanish:**
  all 24 models score 0.24–0.31, clustered around the sampler's 0.279 (random 1–5 guessing
  would score 0.20). Every model on that column behaves, in effect, like the sampler:
  knowing the population, not the person. This may say more about the data than the models —
  demographics are known to be weak predictors of single answers.

The "moderate" MAE margins in the middle of the table are consistent with answering near the
population average and do not by themselves demonstrate person-level knowledge.

## Reproduce

```bash
uv run behaviorbench-eval --task <tasks...> --model-type marginal \
  --model-name marginal-sampler-test --output-dir outputs/marginal
```

Same seed → same results. The sampler replays real answer strings word-for-word, so no answers
fail to parse (0 failures across all 33 tasks). Comparison script and parsed leaderboard data
available on request.
