"""Subject-blind marginal-sampler baseline."""

import random
from typing import Any

from behaviorbench.eval.base import extract_group
from behaviorbench.eval.utils import load_jsonl


class MarginalSamplerModel:
    """Draw each answer at random from the task population's answer pool.

    The sampler replays raw ``assistant`` strings verbatim, so every draw
    parses under the task's output parser by construction. It is blind to
    the subject (demographics, personal history) but conditions on the task
    definition: the whole data file for game tasks, and the task's metric
    group (survey item, BigFive dimension) when the task defines one.

    With pools built from the evaluation split itself (``source="test"``)
    this is an oracle marginal: it scores what a model achieves by knowing
    the population distribution exactly while knowing nothing about the
    individual subject.

    ``bind_task`` must be called before sampling; ``EvaluationRunner.run_task``
    does this automatically for any model that defines it.
    """

    def __init__(self, seed: int = 42, source: str = "test"):
        self.seed = seed
        self.source = source
        self._rng: random.Random | None = None
        self._group_by: str | None = None
        self._pool_all: list[str] = []
        self._pools: dict[str, list[str]] = {}

    def bind_task(self, task: Any) -> None:
        """Build answer pools from the full data file behind ``task``.

        Pools always come from the complete file, not the ``--num-samples``
        subset, so the population estimate does not shrink with smoke tests.
        """
        rows = load_jsonl(task.data_path)
        self._group_by = getattr(task, "_group_by", None)
        self._pool_all = [str(row["assistant"]) for row in rows if "assistant" in row]
        if not self._pool_all:
            raise ValueError(
                f"No 'assistant' answers in {task.data_path}; cannot build a marginal pool."
            )
        self._pools = {}
        if self._group_by:
            for row in rows:
                if "assistant" not in row:
                    continue
                prompt = {"system": row.get("system", ""), "user": row.get("user", "")}
                if "metadata" in row:
                    prompt["metadata"] = row["metadata"]
                group = extract_group(prompt, self._group_by)
                self._pools.setdefault(group, []).append(str(row["assistant"]))
        # Fresh RNG per task so draws don't depend on task order within a run.
        self._rng = random.Random(self.seed)

    def __call__(self, prompt: str | dict[str, str], **kwargs) -> str:
        if self._rng is None:
            raise RuntimeError(
                "MarginalSamplerModel is not bound to a task; call bind_task() first."
            )
        pool = self._pool_all
        if self._group_by and isinstance(prompt, dict):
            group = extract_group(prompt, self._group_by)
            # Fall back to the task-level pool for unmatched groups.
            pool = self._pools.get(group) or self._pool_all
        return self._rng.choice(pool)

    def batch_call(self, prompts: list[str | dict[str, str]], **kwargs) -> list[str]:
        """Process all prompts."""
        return [self(p) for p in prompts]
