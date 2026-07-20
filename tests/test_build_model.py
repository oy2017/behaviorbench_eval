"""Regression tests for endpoint resolution in ``build_model``.

These tests pin down which HTTP client ``--model-type openai`` builds and which
base URL it targets. They exist because ``--model-type openai`` was silently
broken: it never reached the intended API and failed on every call.

Two defects, both covered below:

1. ``OpenAIModel`` defaults to ``use_azure=True`` and the ``openai`` branch did
   not override it, so it built an ``AzureOpenAI`` client (Azure URL scheme +
   ``api-version``) instead of a plain OpenAI client.
2. ``--api-base`` defaulted to ``http://localhost:8000/v1``, so even a correct
   OpenAI client was pointed at localhost instead of ``api.openai.com``.

Together they made ``--model-type openai --model-name gpt-4.1`` (straight from
the README) build an Azure client aimed at localhost -- a hard failure for every
provider. The suite had no coverage of ``build_model``, so the bug shipped and
these tests would have passed unchanged; that gap is what this file closes.
"""

import sys

import pytest

from behaviorbench.eval.main import build_model, parse_args


def _parse(monkeypatch, extra_argv):
    """Parse a realistic CLI invocation so the argparse defaults are exercised.

    Going through ``parse_args`` (rather than hand-building a Namespace) is
    deliberate: defect #2 lives in the ``--api-base`` default, so the test must
    see the real default rather than a value we picked.
    """
    argv = [
        "behaviorbench-eval",
        "--task",
        "game_behavior_dictator",
        "--model-name",
        "gpt-4.1",
    ] + extra_argv
    monkeypatch.setattr(sys, "argv", argv)
    return parse_args()


class TestOpenAIEndpointResolution:
    """``--model-type openai`` must build a plain OpenAI client, not Azure."""

    def test_defaults_to_public_openai_endpoint(self, monkeypatch):
        """With no --api-base, the client targets api.openai.com.

        Expectation:
          * client class is ``OpenAI`` (NOT ``AzureOpenAI``)
          * base_url is the OpenAI SDK default ``https://api.openai.com/v1/``

        If the bug regresses:
          * defect #1 -> client class becomes ``AzureOpenAI`` and requests go to
            ``/openai/deployments/<model>/chat/completions?api-version=...``
          * defect #2 -> base_url becomes ``http://localhost:8000/v1/`` and gpt-4.1
            requests hit localhost, never OpenAI (connection refused).
        """
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        # A stray OPENAI_BASE_URL would mask defect #2, so clear it.
        monkeypatch.delenv("OPENAI_BASE_URL", raising=False)

        model = build_model(_parse(monkeypatch, ["--model-type", "openai"]))

        assert type(model.client).__name__ == "OpenAI"
        assert str(model.client.base_url) == "https://api.openai.com/v1/"

    def test_honors_explicit_api_base(self, monkeypatch):
        """An explicit --api-base (e.g. an OpenAI-compatible proxy) is used verbatim.

        Expectation: base_url matches the provided host and the client is still a
        plain ``OpenAI`` client.

        If the bug regresses (defect #1): an ``AzureOpenAI`` client rewrites this
        into ``https://openrouter.ai/api/v1/openai/`` with an ``api-version``
        query param, which OpenRouter answers with a 404 HTML page -> the run
        dies with "N/N API calls failed".
        """
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")

        model = build_model(
            _parse(
                monkeypatch,
                ["--model-type", "openai", "--api-base", "https://openrouter.ai/api/v1"],
            )
        )

        assert type(model.client).__name__ == "OpenAI"
        assert str(model.client.base_url) == "https://openrouter.ai/api/v1/"


class TestLocalEndpointResolution:
    """The localhost default must survive for ``--model-type local``."""

    def test_local_falls_back_to_localhost(self, monkeypatch):
        """With no --api-base, a local model still targets localhost:8000.

        Expectation: base_url is ``http://localhost:8000/v1/``.

        This guards the fix for defect #2: moving the ``--api-base`` default to
        ``None`` must NOT strand local-server users -- the ``local`` branch has to
        substitute the localhost default itself. If that fallback is dropped, a
        bare ``--model-type local`` run would send requests to api.openai.com
        instead of the user's local server.
        """
        model = build_model(_parse(monkeypatch, ["--model-type", "local"]))

        assert str(model.client.base_url) == "http://localhost:8000/v1/"


def test_openai_requires_api_key(monkeypatch):
    """``--model-type openai`` without OPENAI_API_KEY fails fast with a clear error."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        build_model(_parse(monkeypatch, ["--model-type", "openai"]))
