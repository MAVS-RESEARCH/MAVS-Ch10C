"""Phase 2 empirical repeated-execution corpus writer."""

from __future__ import annotations

import csv
import json
import subprocess
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml

from mavs_ch10c import console
from mavs_ch10c.execution.cache import CorpusCache
from mavs_ch10c.execution.dataset_builder import build_partition_bundle
from mavs_ch10c.execution.environment import capture_environment
from mavs_ch10c.execution.repeated_training import train_specialists_for_unit
from mavs_ch10c.execution.specialist_runner import build_specialist_output_bundle
from mavs_ch10c.execution.system_runner import (
    GOVERNANCE_SYSTEMS,
    attach_run_id,
    run_system_from_bundle,
)
from mavs_ch10c.repeatability.repetition_grid import (
    build_repetition_grid,
    repetition_grid_manifest,
)
from mavs_ch10c.repeatability.seed_registry import load_seed_registry, seed_registry_hash
from mavs_ch10c.verification.hash_utils import (
    load_json_config,
    sha256_file,
    sha256_json,
    write_json,
)


PHASE2_EXECUTION_CODE_PATHS = [
    "src/mavs_ch10c/execution/dataset_builder.py",
    "src/mavs_ch10c/execution/repeated_training.py",
    "src/mavs_ch10c/execution/specialist_runner.py",
    "src/mavs_ch10c/execution/system_runner.py",
    "src/mavs_ch10c/execution/corpus_writer.py",
    "src/mavs_ch10c/execution/cache.py",
    "scripts/run_locked_repetition_corpus.py",
    "scripts/run_audit_repetition_corpus.py",
]

PHASE3_METRIC_CODE_PATHS = [
    "src/mavs_ch10c/comparison/alignment.py",
    "src/mavs_ch10c/comparison/system_outputs.py",
    "src/mavs_ch10c/comparison/variance_dataset.py",
    "src/mavs_ch10c/comparison/baseline_deltas.py",
    "scripts/build_variance_benchmark_dataset.py",
]

REPORT_TEMPLATE_PATHS = [
    "WorkPlan.md",
    "README.md",
]

LOCAL_FINAL_CONTRACT_PATHS = [
    "configs/reproducibility/seed_registry.yaml",
    "configs/reproducibility/split_schedules.yaml",
    "configs/reproducibility/init_schedules.yaml",
    "configs/reproducibility/specialist_compositions.yaml",
    "configs/reproducibility/repetition_grid.yaml",
    "configs/experiments/locked_repetition_corpus.yaml",
    "configs/experiments/audit_repetition_corpus.yaml",
    "results/run_manifests/repetition_grid.csv",
    "results/run_manifests/repetition_grid_manifest.json",
]


def run_repetition_corpus(
    repo_root: Path,
    config_path: Path,
    execution_mode: str,
    command_line: list[str],
) -> dict[str, Any]:
    """Generate a locked or audit empirical repeated-execution corpus."""

    # console.log: phase2 empirical corpus run begins.
    console.log(
        f"phase2.corpus.run.start config={config_path} execution_mode={execution_mode}"
    )
    config = load_json_config(config_path)
    ensure_no_tuning(config)
    foundation = load_json_config(
        repo_root / "results" / "foundation_import" / "ch10a_import_manifest.json"
    )
    ensure_imported_hash_contract(foundation)
    if execution_mode == "final":
        ensure_final_mode_allowed(repo_root, config)
    if config["execution_backend"] != "empirical_sklearn_repeated_training":
        raise ValueError(f"Phase 2 empirical backend required, got {config['execution_backend']}")
    run_mode = str(config["run_mode"])
    output_dir = repo_root / str(config["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    if run_mode == "audit":
        ensure_audit_freeze_gate(repo_root)
    contract = _corpus_run_contract(repo_root, config_path, foundation)
    existing_manifest = _load_existing_manifest_if_valid(
        output_dir,
        config,
        expected_rows=int(config["expected_rows"]),
        contract=contract,
    )
    if existing_manifest is not None:
        if run_mode == "locked":
            ensure_locked_freeze_manifest(repo_root, existing_manifest)
        # console.log: phase2 empirical corpus cache hit.
        console.log(
            "phase2.corpus.run.cache_hit "
            f"mode={run_mode} rows={existing_manifest['row_count']} hash={existing_manifest['corpus_manifest_hash']}"
        )
        return existing_manifest
    ch10a_root = Path(foundation["source_path"])
    system_configs = _load_system_configs(ch10a_root)
    governance_config = _load_yaml(ch10a_root / "configs" / "systems" / "governance_defaults.yaml")
    grid_rows = _read_grid_rows(repo_root / str(config["source_grid_path"]), run_mode)
    expected_rows = int(config["expected_rows"])
    if len(grid_rows) != expected_rows:
        raise ValueError(
            f"{run_mode} grid row count mismatch: actual={len(grid_rows)}, expected={expected_rows}"
        )

    cache = CorpusCache(output_dir / "completed_run_ids.cache")
    corpus_rows: list[dict[str, Any]] = []
    prediction_rows: list[dict[str, Any]] = []
    trace_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    frozen_manifest_rows: list[dict[str, Any]] = []
    fit_rows: dict[str, dict[str, Any]] = {}
    bundle_cache: dict[tuple[Any, ...], Any] = {}
    for unit in grid_rows:
        bundle_key = _bundle_key(unit)
        if bundle_key not in bundle_cache:
            partition = build_partition_bundle(
                str(unit["dataset_id"]),
                run_mode,
                str(unit["split_schedule_id"]),
                int(unit["split_seed"]),
                int(config["partition_row_count"]),
                ch10a_root=ch10a_root,
                class_balance_strategy=str(config["class_balance_strategy"]),
            )
            fitted = train_specialists_for_unit(
                unit, partition, ch10a_root, foundation["specialist_config_hashes"]
            )
            for fit in fitted:
                fit_rows[fit.record.fit_id] = asdict(fit.record)
            bundle_cache[bundle_key] = build_specialist_output_bundle(
                run_mode=run_mode,
                execution_seed=int(unit["execution_seed"]),
                initialization_schedule_id=str(unit["initialization_schedule_id"]),
                specialist_composition_id=str(unit["specialist_composition_id"]),
                partition_bundle=partition,
                fitted_specialists=fitted,
            )
        result = run_system_from_bundle(
            unit,
            bundle_cache[bundle_key],
            foundation["system_config_hashes"],
            system_configs,
            governance_config,
        )
        record_row = asdict(result.record)
        corpus_rows.append(record_row)
        prediction_rows.extend(attach_run_id(result.prediction_rows, result.record.run_id))
        trace_rows.extend(
            {
                **row,
                "run_id": result.record.run_id,
                "repetition_id": result.record.repetition_id,
            }
            for row in result.trace_rows
        )
        frozen_manifest_rows.append(result.frozen_run_manifest)
        manifest_rows.append(result.run_manifest)
        cache.add(result.record.run_id)

    corpus_index_path = output_dir / "corpus_index.csv"
    prediction_path = output_dir / "predictions_index.csv"
    trace_path = output_dir / "trace_index.csv"
    fit_path = output_dir / "specialist_metadata.csv"
    frozen_run_manifest_path = output_dir / "frozen_run_manifests.jsonl"
    run_manifest_path = output_dir / "run_manifests.jsonl"
    _write_csv(corpus_index_path, corpus_rows)
    _write_csv(prediction_path, prediction_rows)
    _write_csv(trace_path, trace_rows)
    _write_csv(fit_path, list(fit_rows.values()))
    _write_jsonl(frozen_run_manifest_path, frozen_manifest_rows)
    _write_jsonl(run_manifest_path, manifest_rows)
    cache.write()

    artifact_hashes = {
        "corpus_index": sha256_file(corpus_index_path),
        "predictions_index": sha256_file(prediction_path),
        "trace_index": sha256_file(trace_path),
        "specialist_metadata": sha256_file(fit_path),
        "frozen_run_manifests": sha256_file(frozen_run_manifest_path),
        "run_manifests": sha256_file(run_manifest_path),
    }
    manifest = {
        "status": "pass",
        "phase": "phase2_repetition_corpus",
        "run_mode": run_mode,
        "execution_mode": execution_mode,
        "execution_backend": config["execution_backend"],
        "empirical_prediction_available": True,
        "row_count": len(corpus_rows),
        "prediction_row_count": len(prediction_rows),
        "expected_rows": expected_rows,
        "unique_specialist_output_bundles": len(bundle_cache),
        "model_fit_count": len(fit_rows),
        "governance_trace_count": len(trace_rows),
        "pre_execution_run_manifest_count": len(frozen_manifest_rows),
        "run_manifest_count": len(manifest_rows),
        "artifact_hashes": artifact_hashes,
        "grid_hash": sha256_file(repo_root / str(config["source_grid_path"])),
        "experiment_config_hash": contract["experiment_config_hash"],
        "execution_code_hashes": contract["execution_code_hashes"],
        "foundation_source_hash_contract": contract["foundation_source_hash_contract"],
        "repetition_grid_manifest_hash": contract["repetition_grid_manifest_hash"],
        "seed_registry_hash": contract["seed_registry_hash"],
        "environment": capture_environment(repo_root, command_line),
        "final_claims_from_training_diagnostics": False,
        "tuning_performed": False,
        "class_balance_strategy": config["class_balance_strategy"],
        "partition_row_count": int(config["partition_row_count"]),
        "benchmark_rows_per_run_min": min(int(row["row_count"]) for row in corpus_rows),
        "benchmark_rows_per_run_max": max(int(row["row_count"]) for row in corpus_rows),
        "governance_systems": sorted(GOVERNANCE_SYSTEMS),
    }
    manifest_hash = write_json(output_dir / "corpus_manifest.json", manifest)
    manifest["corpus_manifest_hash"] = manifest_hash
    write_json(output_dir / "corpus_manifest.json", manifest)
    if run_mode == "locked":
        ensure_locked_freeze_manifest(repo_root, manifest)
    # console.log: phase2 empirical corpus run completed.
    console.log(
        "phase2.corpus.run.complete "
        f"mode={run_mode} rows={len(corpus_rows)} prediction_rows={len(prediction_rows)} "
        f"hash={manifest['corpus_manifest_hash']}"
    )
    return manifest


def _load_existing_manifest_if_valid(
    output_dir: Path,
    config: dict[str, Any],
    expected_rows: int,
    contract: dict[str, Any],
) -> dict[str, Any] | None:
    manifest_path = output_dir / "corpus_manifest.json"
    if not manifest_path.exists():
        return None
    try:
        manifest = load_json_config(manifest_path)
    except Exception:
        return None
    required_files = [
        output_dir / "corpus_index.csv",
        output_dir / "predictions_index.csv",
        output_dir / "trace_index.csv",
        output_dir / "specialist_metadata.csv",
        output_dir / "frozen_run_manifests.jsonl",
        output_dir / "run_manifests.jsonl",
    ]
    if not all(path.exists() for path in required_files):
        return None
    if manifest.get("status") != "pass":
        return None
    if manifest.get("execution_backend") != config.get("execution_backend"):
        return None
    if manifest.get("run_mode") != config.get("run_mode"):
        return None
    if int(manifest.get("row_count", -1)) != expected_rows:
        return None
    if int(manifest.get("partition_row_count", -1)) != int(config["partition_row_count"]):
        return None
    if manifest.get("class_balance_strategy") != config.get("class_balance_strategy"):
        return None
    if manifest.get("empirical_prediction_available") is not True:
        return None
    if int(manifest.get("pre_execution_run_manifest_count", -1)) != expected_rows:
        return None
    if int(manifest.get("run_manifest_count", -1)) != expected_rows:
        return None
    artifact_hashes = manifest.get("artifact_hashes", {})
    expected_artifacts = {
        "corpus_index": output_dir / "corpus_index.csv",
        "predictions_index": output_dir / "predictions_index.csv",
        "trace_index": output_dir / "trace_index.csv",
        "specialist_metadata": output_dir / "specialist_metadata.csv",
        "frozen_run_manifests": output_dir / "frozen_run_manifests.jsonl",
        "run_manifests": output_dir / "run_manifests.jsonl",
    }
    if set(artifact_hashes) != set(expected_artifacts):
        return None
    for label, path in expected_artifacts.items():
        if artifact_hashes.get(label) != sha256_file(path):
            return None
    for key, value in contract.items():
        if manifest.get(key) != value:
            return None
    return manifest


def ensure_no_tuning(config: dict[str, Any]) -> None:
    """Fail if a Phase 2 corpus config permits tuning or model-family changes."""

    # console.log: phase2 no-tuning guard begins.
    console.log("phase2.corpus.no_tuning_guard.start")
    forbidden_true_keys = [
        "allow_hyperparameter_search",
        "allow_governance_tuning",
        "allow_model_family_changes",
        "allow_phase2_final_claims_from_training_diagnostics",
    ]
    enabled = [key for key in forbidden_true_keys if config.get(key) is True]
    if enabled:
        raise ValueError(f"Phase 2 tuning guard failed: {enabled}")
    # console.log: phase2 no-tuning guard completed.
    console.log("phase2.corpus.no_tuning_guard.complete")


def ensure_final_mode_allowed(repo_root: Path, config: dict[str, Any]) -> None:
    """Refuse final mode if frozen inputs are dirty or hash-mismatched."""

    # console.log: phase2 final-mode guard begins.
    console.log("phase2.corpus.final_guard.start")
    ensure_final_hash_contracts(repo_root, config)
    if config.get("final_mode_requires_clean_git", True):
        _assert_clean_git_paths(repo_root, LOCAL_FINAL_CONTRACT_PATHS, "Chapter 10C final inputs")
        _assert_clean_git_paths(
            Path(load_json_config(
                repo_root / "results" / "foundation_import" / "ch10a_import_manifest.json"
            )["source_path"]),
            _imported_contract_paths(
                load_json_config(
                    repo_root / "results" / "foundation_import" / "ch10a_import_manifest.json"
                )
            ),
            "Chapter 10A imported final inputs",
        )
    if config.get("run_mode") == "audit":
        ensure_audit_freeze_gate(repo_root)
    # console.log: phase2 final-mode guard completed.
    console.log("phase2.corpus.final_guard.complete")


def ensure_final_hash_contracts(repo_root: Path, config: dict[str, Any]) -> None:
    """Verify that final runs match frozen seeds and imported upstream hashes."""

    # console.log: phase2 final hash-contract guard begins.
    console.log("phase2.corpus.final_hash_contract.start")
    foundation = load_json_config(
        repo_root / "results" / "foundation_import" / "ch10a_import_manifest.json"
    )
    ensure_imported_hash_contract(foundation)
    seed_registry = load_seed_registry(repo_root / "configs" / "reproducibility" / "seed_registry.yaml")
    recorded_grid_manifest = load_json_config(
        repo_root / "results" / "run_manifests" / "repetition_grid_manifest.json"
    )
    computed_grid_manifest = repetition_grid_manifest(
        repo_root, build_repetition_grid(repo_root, "all")
    )
    expected_seed_hash = seed_registry_hash(seed_registry)
    if recorded_grid_manifest.get("seed_registry_hash") != expected_seed_hash:
        raise RuntimeError("Final corpus mode seed registry hash mismatch")
    if computed_grid_manifest.get("seed_registry_hash") != expected_seed_hash:
        raise RuntimeError("Final corpus mode computed seed registry hash mismatch")
    if recorded_grid_manifest.get("grid_hash") != computed_grid_manifest.get("grid_hash"):
        raise RuntimeError("Final corpus mode repetition grid hash mismatch")
    source_grid_path = repo_root / str(config["source_grid_path"])
    if not source_grid_path.exists():
        raise RuntimeError(f"Final corpus mode source grid missing: {source_grid_path}")
    # console.log: phase2 final hash-contract guard completed.
    console.log("phase2.corpus.final_hash_contract.complete")


def ensure_imported_hash_contract(foundation: dict[str, Any]) -> None:
    """Verify current Chapter 10A source files match the imported manifest hashes."""

    # console.log: phase2 imported hash-contract guard begins.
    console.log("phase2.corpus.imported_hash_contract.start")
    ch10a_root = Path(foundation["source_path"])
    for section in [
        "specialist_config_hashes",
        "system_config_hashes",
        "governance_hashes",
        "protocol_hashes",
        "dataset_config_hashes",
    ]:
        for relative_path, expected_hash in foundation.get(section, {}).items():
            actual_hash = sha256_file(ch10a_root / relative_path)
            if actual_hash != expected_hash:
                raise RuntimeError(
                    f"Imported Chapter 10A hash mismatch: section={section} path={relative_path}"
                )
    # console.log: phase2 imported hash-contract guard completed.
    console.log("phase2.corpus.imported_hash_contract.complete")


def ensure_locked_freeze_manifest(repo_root: Path, locked_manifest: dict[str, Any]) -> dict[str, Any]:
    """Write or refresh the locked pipeline freeze manifest used to gate audit runs."""

    # console.log: phase2 locked freeze manifest write begins.
    console.log("phase2.corpus.locked_freeze_manifest.start")
    if locked_manifest.get("run_mode") != "locked":
        raise RuntimeError("Locked freeze manifest requires a locked corpus manifest")
    output_path = repo_root / "results" / "execution_corpus" / "locked" / "audit_freeze_manifest.json"
    manifest = {
        "status": "pass",
        "phase": "phase2_audit_release_gate",
        "locked_pipeline_frozen": True,
        "metric_code_frozen": True,
        "report_templates_frozen": True,
        "locked_corpus_manifest_hash": locked_manifest["corpus_manifest_hash"],
        "locked_pipeline_code_hashes": _hash_existing_files(repo_root, PHASE2_EXECUTION_CODE_PATHS),
        "metric_code_hashes": _hash_existing_files(repo_root, PHASE3_METRIC_CODE_PATHS),
        "report_template_hashes": _hash_existing_files(repo_root, REPORT_TEMPLATE_PATHS),
        "experiment_config_hashes": {
            "locked": sha256_file(
                repo_root / "configs" / "experiments" / "locked_repetition_corpus.yaml"
            ),
            "audit": sha256_file(
                repo_root / "configs" / "experiments" / "audit_repetition_corpus.yaml"
            ),
        },
    }
    freeze_hash = write_json(output_path, manifest)
    manifest["audit_freeze_manifest_hash"] = freeze_hash
    write_json(output_path, manifest)
    # console.log: phase2 locked freeze manifest write completed.
    console.log(
        "phase2.corpus.locked_freeze_manifest.complete "
        f"hash={manifest['audit_freeze_manifest_hash']}"
    )
    return manifest


def ensure_audit_freeze_gate(repo_root: Path) -> dict[str, Any]:
    """Refuse audit corpus execution unless the locked pipeline is frozen."""

    # console.log: phase2 audit freeze gate begins.
    console.log("phase2.corpus.audit_freeze_gate.start")
    locked_manifest = load_json_config(
        repo_root / "results" / "execution_corpus" / "locked" / "corpus_manifest.json"
    )
    freeze_manifest = load_json_config(
        repo_root / "results" / "execution_corpus" / "locked" / "audit_freeze_manifest.json"
    )
    if locked_manifest.get("status") != "pass":
        raise RuntimeError("Audit corpus requires a passing locked corpus manifest")
    if freeze_manifest.get("status") != "pass":
        raise RuntimeError("Audit corpus requires a passing audit freeze manifest")
    for key in ["locked_pipeline_frozen", "metric_code_frozen", "report_templates_frozen"]:
        if freeze_manifest.get(key) is not True:
            raise RuntimeError(f"Audit corpus freeze gate failed: {key}")
    if freeze_manifest.get("locked_corpus_manifest_hash") != locked_manifest.get("corpus_manifest_hash"):
        raise RuntimeError("Audit corpus freeze gate locked corpus hash mismatch")
    expected = {
        "locked_pipeline_code_hashes": _hash_existing_files(repo_root, PHASE2_EXECUTION_CODE_PATHS),
        "metric_code_hashes": _hash_existing_files(repo_root, PHASE3_METRIC_CODE_PATHS),
        "report_template_hashes": _hash_existing_files(repo_root, REPORT_TEMPLATE_PATHS),
        "experiment_config_hashes": {
            "locked": sha256_file(
                repo_root / "configs" / "experiments" / "locked_repetition_corpus.yaml"
            ),
            "audit": sha256_file(
                repo_root / "configs" / "experiments" / "audit_repetition_corpus.yaml"
            ),
        },
    }
    for key, value in expected.items():
        if freeze_manifest.get(key) != value:
            raise RuntimeError(f"Audit corpus freeze gate hash mismatch: {key}")
    # console.log: phase2 audit freeze gate completed.
    console.log(
        "phase2.corpus.audit_freeze_gate.complete "
        f"hash={freeze_manifest['audit_freeze_manifest_hash']}"
    )
    return freeze_manifest


def _corpus_run_contract(
    repo_root: Path, config_path: Path, foundation: dict[str, Any]
) -> dict[str, Any]:
    # console.log: phase2 corpus run contract build begins.
    console.log("phase2.corpus.run_contract.start")
    seed_registry = load_seed_registry(repo_root / "configs" / "reproducibility" / "seed_registry.yaml")
    recorded_grid_manifest = load_json_config(
        repo_root / "results" / "run_manifests" / "repetition_grid_manifest.json"
    )
    contract = {
        "experiment_config_hash": sha256_file(config_path),
        "execution_code_hashes": _hash_existing_files(repo_root, PHASE2_EXECUTION_CODE_PATHS),
        "foundation_source_hash_contract": _foundation_source_hash_contract(foundation),
        "repetition_grid_manifest_hash": recorded_grid_manifest["grid_hash"],
        "seed_registry_hash": seed_registry_hash(seed_registry),
    }
    # console.log: phase2 corpus run contract build completed.
    console.log(f"phase2.corpus.run_contract.complete hash={sha256_json(contract)}")
    return contract


def _foundation_source_hash_contract(foundation: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": foundation.get("source_id"),
        "source_origin": foundation.get("source_origin"),
        "commit": foundation.get("commit"),
        "dataset_config_hashes": foundation.get("dataset_config_hashes", {}),
        "specialist_config_hashes": foundation.get("specialist_config_hashes", {}),
        "system_config_hashes": foundation.get("system_config_hashes", {}),
        "governance_hashes": foundation.get("governance_hashes", {}),
        "protocol_hashes": foundation.get("protocol_hashes", {}),
    }


def _hash_existing_files(root: Path, relative_paths: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for relative_path in relative_paths:
        path = root / relative_path
        if not path.exists():
            raise RuntimeError(f"Required contract file missing: {path}")
        hashes[relative_path] = sha256_file(path)
    return hashes


def _imported_contract_paths(foundation: dict[str, Any]) -> list[str]:
    paths: set[str] = set()
    for section in [
        "specialist_config_hashes",
        "system_config_hashes",
        "governance_hashes",
        "protocol_hashes",
        "dataset_config_hashes",
    ]:
        paths.update(str(path) for path in foundation.get(section, {}))
    return sorted(paths)


def _assert_clean_git_paths(root: Path, relative_paths: list[str], label: str) -> None:
    if not (root / ".git").exists():
        raise RuntimeError(f"Final corpus mode requires a git checkout for {label}: {root}")
    completed = subprocess.run(
        ["git", "status", "--short", "--", *relative_paths],
        cwd=str(root),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stdout.strip():
        raise RuntimeError(f"Final corpus mode requires clean git paths for {label}")


def _load_system_configs(ch10a_root: Path) -> dict[str, dict[str, Any]]:
    configs: dict[str, dict[str, Any]] = {}
    for system_id in [
        "single_model",
        "mean_ensemble",
        "static_weighted_ensemble",
        "veto_mavs",
        "pure_mavs_gc",
    ]:
        configs[system_id] = _load_yaml(ch10a_root / "configs" / "systems" / f"{system_id}.yaml")
    return configs


def _load_yaml(path: Path) -> dict[str, Any]:
    # console.log: phase2 YAML config load begins.
    console.log(f"phase2.corpus.yaml_load.start path={path}")
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"YAML config must be a mapping: {path}")
    # console.log: phase2 YAML config load completed.
    console.log(f"phase2.corpus.yaml_load.complete path={path}")
    return payload


def _bundle_key(unit: dict[str, Any]) -> tuple[Any, ...]:
    return (
        unit["run_mode"],
        unit["dataset_id"],
        unit["execution_seed"],
        unit["split_schedule_id"],
        unit["initialization_schedule_id"],
        unit["specialist_composition_id"],
    )


def _read_grid_rows(path: Path, run_mode: str) -> list[dict[str, Any]]:
    # console.log: phase2 grid read begins.
    console.log(f"phase2.corpus.grid_read.start path={path} mode={run_mode}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row["run_mode"] == run_mode
        ]
    # console.log: phase2 grid read completed.
    console.log(f"phase2.corpus.grid_read.complete rows={len(rows)}")
    return rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    # console.log: phase2 CSV artifact write begins.
    console.log(f"phase2.corpus.csv_write.start path={path} rows={len(rows)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        # console.log: phase2 CSV artifact write completed.
        console.log(f"phase2.corpus.csv_write.complete path={path}")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    # console.log: phase2 CSV artifact write completed.
    console.log(f"phase2.corpus.csv_write.complete path={path}")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    # console.log: phase2 JSONL artifact write begins.
    console.log(f"phase2.corpus.jsonl_write.start path={path} rows={len(rows)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    # console.log: phase2 JSONL artifact write completed.
    console.log(f"phase2.corpus.jsonl_write.complete path={path}")
