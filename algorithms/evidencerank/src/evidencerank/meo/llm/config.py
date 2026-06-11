"""Configuration loading for offline CREST-MEO LLM synthesis."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


DEFAULT_LLM_CONFIG_PATH = Path(__file__).with_name("config.yaml")


@dataclass(frozen=True)
class SynthesisConfig:
    """Controls MEOL writing and verifier behavior."""

    mode: str = "mock"
    allow_real_llm: bool = False
    output_path: str | None = None
    library_name: str = "crest-meol-default-v1"
    dsl_version: str = "1.0"
    validate_static: bool = True
    validate_leakage: bool = True
    fail_on_verifier_error: bool = True


@dataclass(frozen=True)
class LLMConfig:
    """Provider settings for the optional real LLM path."""

    provider: str = "mock"
    model: str = ""
    api_key_env: str = "OPENAI_API_KEY"
    base_url: str | None = None
    temperature: float = 0.0
    max_output_tokens: int = 8192
    timeout_seconds: float = 60.0
    response_format: str = "json_object"


@dataclass(frozen=True)
class PromptConfig:
    """Prompt input paths and prompt version metadata."""

    version: str = "meo_operator_synthesis_v1"
    artifact_summary_path: str | None = None
    telemetry_schema_path: str | None = None
    mechanism_catalog_path: str | None = None
    include_default_mechanism_catalog: bool = True
    extra_context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MockConfig:
    """Mock-output selector. More variants can be added without changing CLI."""

    variant: str = "default_meol_v1"


@dataclass(frozen=True)
class MEOLLMConfig:
    """Top-level LLM synthesis configuration."""

    synthesis: SynthesisConfig = field(default_factory=SynthesisConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    prompt: PromptConfig = field(default_factory=PromptConfig)
    mock: MockConfig = field(default_factory=MockConfig)


def _section(raw: dict[str, Any], name: str) -> dict[str, Any]:
    value = raw.get(name, {})
    return value if isinstance(value, dict) else {}


def load_llm_config(path: str | Path | None = None) -> tuple[MEOLLMConfig, Path]:
    """Load a YAML config file for offline synthesis."""

    config_path = Path(path) if path is not None else DEFAULT_LLM_CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    if not isinstance(raw, dict):
        raise ValueError("LLM config root must be a YAML mapping")

    synthesis = SynthesisConfig(**_section(raw, "synthesis"))
    llm = LLMConfig(**_section(raw, "llm"))
    prompt = PromptConfig(**_section(raw, "prompt"))
    mock = MockConfig(**_section(raw, "mock"))
    return MEOLLMConfig(synthesis=synthesis, llm=llm, prompt=prompt, mock=mock), config_path

