"""LLM client adapters for offline MEOL synthesis.

The mock adapter is the default. Real providers are only used when explicitly
enabled in config and CLI.
"""

from __future__ import annotations

import json
import os
from typing import Any, Protocol

from .config import LLMConfig
from .mock_outputs import mock_meol


class MEOLLMClient(Protocol):
    """Minimal JSON-producing interface used by the synthesis CLI."""

    def generate_meol(self, prompt: str) -> dict[str, Any]:
        """Generate a MEOL JSON object."""


class MockMEOLLMClient:
    """Deterministic mock LLM client."""

    def generate_meol(self, prompt: str) -> dict[str, Any]:
        _ = prompt
        return mock_meol()


class OpenAIMEOLLMClient:
    """OpenAI-backed client for the future real LLM path."""

    def __init__(self, config: LLMConfig) -> None:
        self._config = config

    def generate_meol(self, prompt: str) -> dict[str, Any]:
        from openai import OpenAI

        if not self._config.model:
            raise ValueError("llm.model must be set for provider=openai")
        api_key = os.environ.get(self._config.api_key_env)
        if not api_key:
            raise ValueError(f"missing API key environment variable: {self._config.api_key_env}")

        client = OpenAI(
            api_key=api_key,
            base_url=self._config.base_url,
            timeout=self._config.timeout_seconds,
        )
        response_format = (
            {"type": "json_object"}
            if self._config.response_format == "json_object"
            else None
        )
        kwargs: dict[str, Any] = {
            "model": self._config.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an offline CREST-MEO operator synthesis engine. "
                        "Return valid JSON only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": self._config.temperature,
            "max_tokens": self._config.max_output_tokens,
        }
        if response_format is not None:
            kwargs["response_format"] = response_format
        completion = client.chat.completions.create(**kwargs)
        content = completion.choices[0].message.content or ""
        return _loads_json_object(content)


def make_llm_client(config: LLMConfig, *, allow_real_llm: bool) -> MEOLLMClient:
    """Create a client from config without allowing accidental real calls."""

    provider = config.provider.lower()
    if provider == "mock":
        return MockMEOLLMClient()
    if not allow_real_llm:
        raise ValueError(
            "real LLM provider requested but allow_real_llm is false; "
            "set synthesis.allow_real_llm=true and pass --allow-real-llm"
        )
    if provider == "openai":
        return OpenAIMEOLLMClient(config)
    raise ValueError(f"unsupported LLM provider: {config.provider}")


def _loads_json_object(text: str) -> dict[str, Any]:
    """Parse a JSON object, tolerating markdown fences around the object."""

    clean = text.strip()
    if clean.startswith("```"):
        lines = [line for line in clean.splitlines() if not line.strip().startswith("```")]
        clean = "\n".join(lines).strip()
    try:
        raw = json.loads(clean)
    except json.JSONDecodeError:
        start = clean.find("{")
        end = clean.rfind("}")
        if start < 0 or end <= start:
            raise
        raw = json.loads(clean[start : end + 1])
    if not isinstance(raw, dict):
        raise ValueError("LLM response must be a JSON object")
    return raw

