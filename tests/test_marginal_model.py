"""Tests for the subject-blind marginal-sampler baseline."""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from behaviorbench.eval.main import EvaluationRunner, build_model, main, parse_args
from behaviorbench.models import MarginalSamplerModel


def _parse(monkeypatch, extra_argv):
    argv = ["behaviorbench-eval", "--task", "pers_score_pred"] + extra_argv
    monkeypatch.setattr(sys, "argv", argv)
    return parse_args()


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")


def _fake_task(data_path: Path, group_by: str | None = None):
    return SimpleNamespace(data_path=str(data_path), _group_by=group_by, name="fake")


class TestBuildModelWiring:
    def test_marginal_model_type_builds_sampler_without_model_name(self, monkeypatch):
        model = build_model(_parse(monkeypatch, ["--model-type", "marginal"]))
        assert isinstance(model, MarginalSamplerModel)
        assert model.source == "test"

    def test_marginal_seed_comes_from_cli(self, monkeypatch):
        model = build_model(_parse(monkeypatch, ["--model-type", "marginal", "--seed", "7"]))
        assert model.seed == 7

    def test_marginal_rejects_tasks_without_population(self, monkeypatch):
        monkeypatch.setattr(
            sys,
            "argv",
            ["behaviorbench-eval", "--task", "ieo_economics", "--model-type", "marginal"],
        )
        with pytest.raises(ValueError, match="no population answer distribution"):
            main()

    def test_marginal_rejects_resume(self, monkeypatch):
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "behaviorbench-eval",
                "--task",
                "pers_score_pred",
                "--model-type",
                "marginal",
                "--resume",
                "some.json",
            ],
        )
        with pytest.raises(ValueError, match="--resume is not supported"):
            main()


class TestSamplerBehavior:
    def test_unbound_sampler_raises(self):
        with pytest.raises(RuntimeError, match="bind_task"):
            MarginalSamplerModel()({"system": "", "user": ""})

    def test_draws_come_from_pool_verbatim(self, tmp_path):
        rows = [{"system": "s", "user": f"u{i}", "assistant": f"[{i}]"} for i in range(20)]
        data = tmp_path / "test.jsonl"
        _write_jsonl(data, rows)

        model = MarginalSamplerModel(seed=1)
        model.bind_task(_fake_task(data))
        pool = {f"[{i}]" for i in range(20)}
        draws = model.batch_call([{"system": "s", "user": "whatever"}] * 200)
        assert set(draws) <= pool
        assert len(set(draws)) > 1  # actually sampling, not constant

    def test_grouped_draws_stay_within_group(self, tmp_path):
        rows = []
        for i in range(30):
            item = "ItemA" if i % 2 == 0 else "ItemB"
            answer = "[1]" if item == "ItemA" else "[5]"
            rows.append(
                {
                    "system": "s",
                    "user": "q",
                    "assistant": answer,
                    "metadata": {"target_item": item},
                }
            )
        data = tmp_path / "test.jsonl"
        _write_jsonl(data, rows)

        model = MarginalSamplerModel(seed=1)
        model.bind_task(_fake_task(data, group_by="target_item"))

        prompt_a = {"system": "s", "user": "q", "metadata": {"target_item": "ItemA"}}
        prompt_b = {"system": "s", "user": "q", "metadata": {"target_item": "ItemB"}}
        assert set(model.batch_call([prompt_a] * 50)) == {"[1]"}
        assert set(model.batch_call([prompt_b] * 50)) == {"[5]"}

    def test_unknown_group_falls_back_to_task_pool(self, tmp_path):
        rows = [
            {"system": "s", "user": "q", "assistant": "[3]", "metadata": {"target_item": "ItemA"}}
        ]
        data = tmp_path / "test.jsonl"
        _write_jsonl(data, rows)

        model = MarginalSamplerModel(seed=1)
        model.bind_task(_fake_task(data, group_by="target_item"))
        prompt = {"system": "s", "user": "q", "metadata": {"target_item": "NeverSeen"}}
        assert model(prompt) == "[3]"

    def test_same_seed_reproduces_draws(self, tmp_path):
        rows = [{"system": "s", "user": "u", "assistant": f"[{i}]"} for i in range(50)]
        data = tmp_path / "test.jsonl"
        _write_jsonl(data, rows)
        prompts = [{"system": "s", "user": "u"}] * 100

        draws = []
        for _ in range(2):
            model = MarginalSamplerModel(seed=42)
            model.bind_task(_fake_task(data))
            draws.append(model.batch_call(prompts))
        assert draws[0] == draws[1]

        other = MarginalSamplerModel(seed=43)
        other.bind_task(_fake_task(data))
        assert other.batch_call(prompts) != draws[0]


@pytest.mark.skipif(
    not Path("data/big_five/pers_score_pred/test.jsonl").exists(),
    reason="data bundle not present",
)
def test_end_to_end_pers_score_pred(tmp_path):
    """Sampler runs through the real pipeline with zero parse failures."""
    runner = EvaluationRunner(output_dir=tmp_path)
    model = MarginalSamplerModel(seed=42)
    result = runner.run_task(
        "pers_score_pred",
        model,
        "data/big_five/pers_score_pred/test.jsonl",
        num_samples=25,
        seed=42,
    )
    assert any(key.startswith("MAE") for key in result.metrics)
    assert result.metadata["num_failed_parses"] == 0
