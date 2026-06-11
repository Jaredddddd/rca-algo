"""CLI for offline CREST-MEO MEOL synthesis.

Default behavior is deterministic mock synthesis. Real LLM calls require both
config opt-in and the --allow-real-llm CLI flag.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import yaml

from ..artifacts.telemetry_schema import summarize_parquet_folder
from ..dsl.schema import EvidenceOperatorSpec, parse_operator_spec
from ..verify.leakage_verifier import leakage_verify
from ..verify.static_verifier import static_verify
from .client import make_llm_client
from .config import DEFAULT_LLM_CONFIG_PATH, MEOLLMConfig, load_llm_config
from .mock_outputs import mock_synthesis_inputs
from .prompts import DEFAULT_MECHANISM_CATALOG, build_operator_synthesis_prompt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Synthesize a CREST-MEO MEOL JSON file.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_LLM_CONFIG_PATH,
        help="YAML config path. Defaults to the package config.yaml.",
    )
    parser.add_argument("--output", type=Path, default=None, help="Output MEOL JSON path.")
    parser.add_argument("--mock", action="store_true", help="Force deterministic mock synthesis.")
    parser.add_argument(
        "--allow-real-llm",
        action="store_true",
        help="Allow real LLM provider calls when config also opts in.",
    )
    parser.add_argument(
        "--input-folder",
        type=Path,
        default=None,
        help="Optional incident folder used to summarize telemetry schema for the prompt.",
    )
    parser.add_argument("--print-prompt", action="store_true", help="Print prompt and exit.")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    config, config_path = load_llm_config(args.config)
    if args.mock:
        config = _force_mock(config)

    context = _load_prompt_context(config, config_path, args.input_folder)
    prompt = build_operator_synthesis_prompt(
        artifact_summary=context["artifact_summary"],
        telemetry_schema=context["telemetry_schema"],
        mechanism_catalog=context["mechanism_catalog"],
        extra_context=config.prompt.extra_context,
    )
    if args.print_prompt:
        print(prompt)
        return

    allow_real = bool(config.synthesis.allow_real_llm and args.allow_real_llm)
    client = make_llm_client(config.llm, allow_real_llm=allow_real)
    meol = client.generate_meol(prompt)
    meol = _finalize_meol(meol, config, config_path)

    verifier_summary = _verify_meol(meol, config)
    meol.setdefault("generator", {})
    meol["generator"]["verifier"] = verifier_summary

    output = _output_path(args.output, config)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(meol, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"saved {output}")
    print(json.dumps(verifier_summary, sort_keys=True))


def _force_mock(config: MEOLLMConfig) -> MEOLLMConfig:
    synthesis = replace(config.synthesis, mode="mock", allow_real_llm=False)
    llm = replace(config.llm, provider="mock")
    return replace(config, synthesis=synthesis, llm=llm)


def _output_path(cli_output: Path | None, config: MEOLLMConfig) -> Path:
    if cli_output is not None:
        return cli_output
    if config.synthesis.output_path:
        return Path(config.synthesis.output_path)
    raise SystemExit("--output is required when synthesis.output_path is not set")


def _load_prompt_context(
    config: MEOLLMConfig,
    config_path: Path,
    input_folder: Path | None,
) -> dict[str, Any]:
    if config.synthesis.mode.lower() == "mock" and not input_folder:
        context = mock_synthesis_inputs()
    else:
        context = {
            "artifact_summary": {},
            "telemetry_schema": {},
            "mechanism_catalog": [],
        }

    if config.prompt.artifact_summary_path:
        context["artifact_summary"] = _load_structured_file(
            _resolve_path(config.prompt.artifact_summary_path, config_path)
        )
    if config.prompt.telemetry_schema_path:
        context["telemetry_schema"] = _load_structured_file(
            _resolve_path(config.prompt.telemetry_schema_path, config_path)
        )
    if input_folder is not None:
        context["telemetry_schema"] = summarize_parquet_folder(input_folder)
    if config.prompt.mechanism_catalog_path:
        mechanism_catalog = _load_structured_file(
            _resolve_path(config.prompt.mechanism_catalog_path, config_path)
        )
        if not isinstance(mechanism_catalog, list):
            raise ValueError("mechanism_catalog_path must contain a list")
        context["mechanism_catalog"] = mechanism_catalog
    elif config.prompt.include_default_mechanism_catalog and not context["mechanism_catalog"]:
        context["mechanism_catalog"] = DEFAULT_MECHANISM_CATALOG
    return context


def _load_structured_file(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return json.loads(text)


def _resolve_path(value: str, config_path: Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else config_path.parent / path


def _finalize_meol(meol: dict[str, Any], config: MEOLLMConfig, config_path: Path) -> dict[str, Any]:
    meol["library_name"] = str(meol.get("library_name") or config.synthesis.library_name)
    meol["dsl_version"] = str(meol.get("dsl_version") or config.synthesis.dsl_version)
    meol["roles"] = [
        "mutation",
        "propagation",
        "observability_bias",
        "topology_context",
    ]
    meol.setdefault("operators", [])
    meol["generator"] = {
        **dict(meol.get("generator", {})),
        "type": config.llm.provider,
        "mode": config.synthesis.mode,
        "prompt_version": config.prompt.version,
        "model": config.llm.model,
        "config_path": str(config_path),
        "uses_gt": False,
        "uses_case_metadata": False,
        "uses_prior_run_results": False,
        "deterministic_online_runtime": True,
    }
    return meol


def _verify_meol(meol: dict[str, Any], config: MEOLLMConfig) -> dict[str, Any]:
    operators = meol.get("operators", [])
    if not isinstance(operators, list):
        raise ValueError("MEOL operators must be a list")

    errors: dict[str, list[str]] = {}
    parsed: list[EvidenceOperatorSpec] = []
    for idx, raw in enumerate(operators):
        try:
            spec = parse_operator_spec(raw)
            parsed.append(spec)
        except Exception as exc:
            errors[f"operator[{idx}]"] = [f"parse_error:{type(exc).__name__}:{exc}"]
            continue

        operator_errors: list[str] = []
        if config.synthesis.validate_static:
            ok, static_errors = static_verify(spec)
            if not ok:
                operator_errors.extend(f"static:{error}" for error in static_errors)
        if config.synthesis.validate_leakage:
            ok, leakage_errors = leakage_verify(spec)
            if not ok:
                operator_errors.extend(f"leakage:{error}" for error in leakage_errors)
        if operator_errors:
            errors[spec.name] = operator_errors

    summary = {
        "operator_count": len(operators),
        "parsed_operator_count": len(parsed),
        "error_count": len(errors),
        "errors": errors,
    }
    if errors and config.synthesis.fail_on_verifier_error:
        raise SystemExit(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


if __name__ == "__main__":
    main()
