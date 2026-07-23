# Reference baselines: how well can these tasks be scored without knowing the person?

*One page — 2026-07-22. Full per-task results (every prompt, answer, and metric) are in
[`marginal-sampler-test/`](marginal-sampler-test/).*

## The idea

Models on BehaviorBench do two things at once: they match what people **in general** do (the
distributional level, scored by Wasserstein distance), and they predict what **one specific
person** will do (the individual level, scored by MAE and accuracy). Today the
individual-level scores are only compared model against model. This note adds two reference
numbers per task, both computed with **no information about the person**, from the human
answer pools (per survey item, per Big Five dimension, per game — the same grouping the
metrics already use):

- **Constant** — always give the pool's most common answer (the median for number answers).
  This is provably the best score any person-blind strategy can reach. **A model above it must
  be using something about the person.** A model below it hasn't shown that — the score is
  reachable without knowing anyone.
- **Sampler** — answer each question with a random draw from real people's answers, run
  through the released pipeline unchanged (`--model-type marginal`, seed 42, full test files).
  This is what pure population-matching scores. A model near it is behaving like random draws
  from the crowd; a model below it is not even reproducing what the crowd answers.

**Is the constant a fair ceiling?** Two checks. First, it only bounds *demonstrated* signal
under these metrics: a model that samples its answers (arguably the right behavior for
simulation) can hold person-level knowledge in its distribution yet score below the constant —
likelihood-based or argmax scoring would separate that. Second, the ceiling depends on the
grouping: a person-blind strategy could also use non-person context such as the round number.
Checked for multi-round: refining the constant to per-(game, round) medians moves the bar only
from 21.1 to 20.3, so Be.FM-1.5's 16.2 clears even the finer ceiling — its edge really comes
from the person's history. For the five columns no model beats, finer grouping can only raise
the ceiling, so those findings are conservative.

**Caveats.** (1) Ideally the answer pools should come from the *training* population. I did not
have the training data, so the pools come from the released test files, assuming the training
and test populations are close (they come from the same sources, split at random). Happy to
redo this with training-side pools. (2) My runs use the full test files; the leaderboard uses
its n_v1 sampling. Small differences should be read as ties. (3) Push/Pull columns are left
out, following the paper's held-out treatment.

## Results: nine individual-level columns

Leaderboard values from the public site (2026-05-07). Be.FM-1.5-70B = 5-run mean.

| task (metric)                  | constant | sampler | Be.FM-1.5-70B | best on leaderboard | vs the constant |
|--------------------------------|:-----:|:-----:|:-------------:|:-------------------:|---|
| Multi-Round Pred. (MAE ↓)      | 21.1 | 28.8 | **16.2** | GPT 4.1 — **16.1** | **clearly better** |
| Masked Resp. (acc ↑)           | 0.386 | 0.302 | **0.449** | Gemini 3.1 Pro — **0.485** | **clearly better** |
| Strategic play (win rate ↑)    | — | 0.079 (a random human's guess) | **0.501** | Be.FM-1.5-70B | **6× the human rate** |
| Seq. Resp. (acc ↑)             | 0.397 | 0.314 | 0.404 | Gemini 3.1 Pro — **0.425** | at the constant; top models better |
| Across-Ctx Pred. (MAE ↓)       | 20.0 | 28.0 | 25.0 | Claude Sonnet 4.6 — 21.6 | no model better |
| Demo. To Resp. (acc ↑)         | 0.394 | 0.279 | 0.286 | Gemini 3.1 Pro — 0.305 | no model better |
| Demo. To Pers. (MAE ↓)         | 6.33 | 9.18 | 7.17 | Gemini 3.1 Pro — 6.40 | no model better (best ties it) |
| Across-Dim Pers. (MAE ↓)       | 6.21 | 8.92 | 6.77 | Claude Opus 4.6 — 6.73 | no model better |
| Pers. To Demo. age (MAE ↓)     | 8.48 | 12.34 | 9.38 | Llama3.3-70B — 9.29 | no model better |

The split is clean, and it follows **what the prompt gives the model**:

- **When the prompt shows the person's own earlier behavior** (past game rounds, their other
  questionnaire answers), models clearly beat the constant. This is real individual-level
  prediction, and it is the benchmark's strongest demonstrated result.
- **When the prompt gives only indirect information** (demographics, scores from other
  dimensions, play in *other* games), no model on the leaderboard beats the constant — a
  simple person-blind lookup table — on any of the five columns.

**Demo. To Resp. in one line.** Guessing 1–5 at random scores 0.20. A random draw from real
answers scores 0.279. Always giving the most common answer scores 0.394. All 24 models land
between 0.24 and 0.31 — between the two random strategies, below the lookup table. This may
say more about the data than the models: demographics are known to be weak predictors of
single answers. Either way, this column today mostly rewards knowing the population, not
knowing the person.

## One useful thing the distributional (Wasserstein) scores add

By itself the sampler's Wasserstein distance proves nothing — it draws from the real answers,
so its distance is only sampling noise (0.2–1.3 across tasks; call this the noise floor). But
read next to the individual scores, Wasserstein distance shows **how** a model is being
person-blind:

- **Wasserstein near the floor + accuracy near the sampler** → the model behaves like the
  sampler: it has learned what people answer, and draws from it. Be.FM-1.5 on Demo. To Resp.
  is the clearest case (acc 0.286 vs sampler's 0.279, and the lowest Wasserstein distance of
  any model on that task).
- **Good MAE + high Wasserstein distance** → the model is hedging toward the average (most
  general-purpose models on the MAE columns).
- **Better than the constant + Wasserstein near the floor** → the model knows individuals
  *and* keeps a realistic answer distribution. Be.FM-1.5 on multi-round (MAE 16.2, Wasserstein
  ~2.7× the floor) is the only case of this on the leaderboard — arguably a stronger statement
  of its contribution than either score alone.

## Reproduce

```bash
uv run behaviorbench-eval --task <tasks...> --model-type marginal \
  --model-name marginal-sampler-test --output-dir outputs/marginal
```

Same seed → same results. The sampler replays real answer strings word-for-word, so no answers
fail to parse (0 failures across all 33 tasks). The constant reference is a two-line
calculation per task on the same pools. Comparison script and parsed leaderboard data
available on request.
