# Findings — why `tencent/hy3` scores poorly on distributional tasks

Companion to [README.md](README.md). **This file is interpretation, not program output** —
read [`RESULTS.txt`](RESULTS.txt) for what the program itself reports.

Every per-task figure quoted here is copied from the program's own output: the `W` column is
`Wasserstein_with_ks_distance` from `metrics`, and the mean/SD columns are
`model_action_mean`, `model_action_std`, `human_action_mean`, `human_action_std` from
`metadata`. All are visible in [`RESULTS.txt`](RESULTS.txt) and in the raw JSONs. Rows
labelled **mean** are the one thing computed here — a plain average across the nine games.

## Summary

hy3 is competent at **predicting** human behaviour and poor at **reproducing** it. Two
separate mechanisms drive the weak `game_behavior` Wasserstein score (29.49), and they are
worth distinguishing because they have different implications.

---

## Per-game breakdown

All nine `game_behavior` tasks, n=1000 model samples against the human reference
distribution:

| game | model mean | model SD | human mean | human SD | W |
|---|---:|---:|---:|---:|---:|
| bomb | 57.14 | 19.72 | 45.56 | 23.09 | 14.30 |
| dictator | 49.76 | 2.48 | 24.71 | 19.19 | 25.51 |
| guessing | 0.44 | 1.46 | 35.47 | 21.51 | 35.03 |
| public_goods | 9.94 | 0.86 | 8.91 | 6.07 | 24.06 |
| push_pull | 0.07 | 0.25 | 0.57 | 0.50 | 50.30 |
| trust_banker | 75.16 | 6.27 | 55.90 | 37.40 | 22.44 |
| trust_investor | 94.57 | 16.23 | 42.19 | 39.89 | 52.38 |
| ultimatum_proposer | 39.99 | 2.21 | 44.92 | 18.33 | 13.56 |
| ultimatum_responder | 5.57 | 7.13 | 33.29 | 17.80 | 27.81 |
| **mean** | | **6.29** | | **20.42** | **29.49** |

---

## Failure mode 1 — distributional collapse

The model emits a near-point-mass where the benchmark expects a distribution. Mean model SD
across the nine games is **6.29** against a human **20.42** — about a third of the
behavioural variance.

The dictator game is the clearest case. 1000 independent samples of an identical prompt:

| response | count | share |
|---|---:|---:|
| gave $50 | 981 | 98.1% |
| gave $40 | 13 | 1.3% |
| gave $20 | 4 | 0.4% |
| gave $30 | 1 | 0.1% |
| gave $80 | 1 | 0.1% |

Only **5 distinct values** and **13 distinct output strings** across 1000 samples. Sample
outputs:

```
I would keep $50 and give the other player [$50].
I would keep $60 and give the other player [$40].
I will keep $70 for myself and give the other player [$30].
```

Humans in the same game gave a mean of $24.71 with SD $19.19 — a broad, right-skewed
distribution that this does not resemble.

## Failure mode 2 — playing the equilibrium, not the human

Distinct from collapse: in several games the model's *centre* is displaced toward the
game-theoretic solution, where humans systematically deviate.

| game | hy3 | human | what happened |
|---|---:|---:|---|
| guessing (p-beauty) | **0.44** | 35.47 | Plays the Nash equilibrium (0). Humans do 1–2 levels of iterated reasoning and land near 35. |
| push_pull | 0.07 | 0.57 | Corner solution. |
| ultimatum_responder | 5.57 | 33.29 | Accepts near-insulting offers — rational, since any positive amount beats zero. Humans reject unfair offers out of fairness concerns. |
| trust_investor | **94.57** | 42.19 | Over-trusts dramatically, sending almost the entire endowment. |

These games are research instruments *precisely because* humans deviate from the rational
prediction in them. A model that optimises correctly fails them for reasons that have
nothing to do with sampling diversity — no amount of added variance would fix `guessing`,
because the centre is in the wrong place.

**Implication:** the two failure modes need different remedies. Collapse is potentially a
decoding or fine-tuning issue; equilibrium-seeking is a deeper alignment-to-human-behaviour
issue, which is the gap behavioural fine-tuning (Be.FM and similar) exists to close.

---

## What the model is good at

The same model does well wherever the task is to *reason about* people rather than *be* one:

| task | score | note |
|---|---|---|
| `multiround_behavior` | MAE 10.4–29.8 across its 8 tasks | predicting a specific person's next action |
| `ieo_economics` | accuracy **0.831** | economics knowledge, 124 items |
| `big_five` | MAE 4.79 | personality-score prediction |
| `workflow` (free-text) | BLEURT **0.443** | research-workflow generation |

This is a clean illustration of the paper's central claim: behavioural *knowledge* and
behavioural *fidelity* are separable capabilities, and strong general models can have the
first without the second.

---

## Data quality

- **2 parse failures across ~27,000 requests** (0.007%), both in `trust_investor`. The
  findings above are not parsing artefacts.
- **0 failed tasks** — every one of the 39 completed.
- `game_behavior` used n=1000 model samples per game (998 for `trust_investor`, where the
  two parse failures occurred) against human reference samples of n=200 per game.

## Open questions

1. **Decoding settings.** The run used provider-default sampling. How much of failure mode 1
   is decoding rather than the model has not been established here, and the paper's own
   decoding protocol is not confirmed — so this is also a comparability question for the
   leaderboard, not only for hy3.
2. **MAE convention.** Whether the paper's per-family MAE averages use normalised or raw
   units changes the acrossgame figure materially (30.28 vs 22.95). Worth confirming before
   any MAE-based ranking claim.
3. **Generality.** The 1000-sample analysis above is for `dictator`. The per-game table
   suggests the pattern holds broadly, but only `dictator` has been examined at that depth.
