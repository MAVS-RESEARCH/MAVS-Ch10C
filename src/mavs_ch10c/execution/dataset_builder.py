"""Empirical repeated dataset partitions for Phase 2 execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_openml, load_breast_cancer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from mavs_ch10c import console
from mavs_ch10c.verification.hash_utils import sha256_file, sha256_json

SPLIT_ORDER = (
    "train",
    "validation",
    "calibration",
    "locked_benchmark",
    "audit_benchmark",
)

DEFAULT_SPLIT_RATIOS = {
    "train": 0.60,
    "validation": 0.15,
    "calibration": 0.10,
    "locked_benchmark": 0.075,
    "audit_benchmark": 0.075,
}


@dataclass(frozen=True)
class SplitData:
    name: str
    X: np.ndarray
    y: np.ndarray
    row_ids: np.ndarray
    row_hashes: tuple[str, ...]
    feature_matrix_hash: str
    label_hash: str
    row_hash: str


@dataclass(frozen=True)
class PartitionBundle:
    dataset_id: str
    run_mode: str
    split_schedule_id: str
    split_seed: int
    train_count: int
    validation_count: int
    calibration_count: int
    locked_benchmark_count: int
    audit_benchmark_count: int
    benchmark_count: int
    train_hash: str
    validation_hash: str
    calibration_hash: str
    locked_benchmark_hash: str
    audit_benchmark_hash: str
    partition_manifest_hash: str
    splits: dict[str, SplitData]
    feature_count: int
    source_config_hash: str
    preprocessing_hash: str
    working_frame_hash: str

    @property
    def benchmark_split_name(self) -> str:
        return "locked_benchmark" if self.run_mode == "locked" else "audit_benchmark"

    @property
    def benchmark(self) -> SplitData:
        return self.splits[self.benchmark_split_name]


_SOURCE_CACHE: dict[tuple[str, str, int], pd.DataFrame] = {}
_PARTITION_CACHE: dict[tuple[str, str, str, int, int, str], PartitionBundle] = {}


def build_partition_bundle(
    dataset_id: str,
    run_mode: str,
    split_schedule_id: str,
    split_seed: int,
    partition_row_count: int = 120,
    ch10a_root: Path | None = None,
    class_balance_strategy: str = "minority_preserving_cap",
) -> PartitionBundle:
    """Create empirical train/validation/calibration/locked/audit partitions."""

    # console.log: phase2 empirical partition bundle build begins.
    console.log(
        "phase2.dataset_builder.partition.start "
        f"dataset={dataset_id} mode={run_mode} split={split_schedule_id}"
    )
    source_root = ch10a_root or _default_ch10a_root()
    cache_key = (
        str(source_root.resolve()),
        dataset_id,
        run_mode,
        split_schedule_id,
        int(split_seed),
        int(partition_row_count),
        class_balance_strategy,
    )
    cached = _PARTITION_CACHE.get(cache_key)
    if cached is not None:
        # console.log: phase2 empirical partition cache hit.
        console.log(
            "phase2.dataset_builder.partition.cache_hit "
            f"dataset={dataset_id} split={split_schedule_id}"
        )
        return cached

    dataset_config_path = source_root / "configs" / "datasets" / f"{dataset_id}.yaml"
    config = _load_yaml(dataset_config_path)
    source_frame = _load_source_frame(source_root, config, partition_row_count)
    working_frame = _select_working_frame(
        source_frame, config, split_seed, partition_row_count, class_balance_strategy
    )
    labels = _binary_labels(working_frame, config)
    assignments = _create_assignments(labels, split_seed, DEFAULT_SPLIT_RATIOS)
    validate_partition_isolation(
        {
            split_name: [
                _row_hash(dataset_id, int(working_frame.iloc[index]["source_row_index"]))
                for index in indices
            ]
            for split_name, indices in assignments.items()
        }
    )
    splits = _preprocess_splits(working_frame, labels, assignments, config)
    manifest_payload = {
        "dataset_id": dataset_id,
        "run_mode": run_mode,
        "split_schedule_id": split_schedule_id,
        "split_seed": split_seed,
        "partition_row_count": int(len(working_frame)),
        "class_balance_strategy": class_balance_strategy,
        "split_hashes": {name: split.row_hash for name, split in splits.items()},
        "label_hashes": {name: split.label_hash for name, split in splits.items()},
        "source_config_hash": sha256_file(dataset_config_path),
        "working_frame_hash": _hash_dataframe(working_frame),
    }
    bundle = PartitionBundle(
        dataset_id=dataset_id,
        run_mode=run_mode,
        split_schedule_id=split_schedule_id,
        split_seed=int(split_seed),
        train_count=len(splits["train"].y),
        validation_count=len(splits["validation"].y),
        calibration_count=len(splits["calibration"].y),
        locked_benchmark_count=len(splits["locked_benchmark"].y),
        audit_benchmark_count=len(splits["audit_benchmark"].y),
        benchmark_count=len(
            splits["locked_benchmark" if run_mode == "locked" else "audit_benchmark"].y
        ),
        train_hash=splits["train"].row_hash,
        validation_hash=splits["validation"].row_hash,
        calibration_hash=splits["calibration"].row_hash,
        locked_benchmark_hash=splits["locked_benchmark"].row_hash,
        audit_benchmark_hash=splits["audit_benchmark"].row_hash,
        partition_manifest_hash=sha256_json(manifest_payload),
        splits=splits,
        feature_count=int(splits["train"].X.shape[1]),
        source_config_hash=manifest_payload["source_config_hash"],
        preprocessing_hash=sha256_json(
            {
                "numeric": config["features"].get("numeric", []),
                "categorical": config["features"].get("categorical", []),
                "preprocessing": config["preprocessing"],
            }
        ),
        working_frame_hash=manifest_payload["working_frame_hash"],
    )
    _PARTITION_CACHE[cache_key] = bundle
    # console.log: phase2 empirical partition bundle build completed.
    console.log(
        "phase2.dataset_builder.partition.complete "
        f"hash={bundle.partition_manifest_hash} benchmark_rows={bundle.benchmark_count}"
    )
    return bundle


def validate_partition_isolation(partitions: dict[str, list[str]]) -> None:
    """Fail if any row identifier overlaps another partition."""

    # console.log: phase2 partition isolation validation begins.
    console.log("phase2.dataset_builder.isolation.start")
    seen: dict[str, str] = {}
    for partition_name, rows in partitions.items():
        for row_hash in rows:
            previous = seen.get(row_hash)
            if previous is not None:
                raise ValueError(
                    f"Partition overlap detected: {previous} and {partition_name}"
                )
            seen[row_hash] = partition_name
    # console.log: phase2 partition isolation validation completed.
    console.log(f"phase2.dataset_builder.isolation.complete rows={len(seen)}")


def _default_ch10a_root() -> Path:
    candidates = [
        Path("../MAVS-Chapter-10A"),
        Path("../MAVS-Ch10A"),
        Path("C:/Users/Saif malik/MAVS-Chapter-10A"),
        Path("C:/Users/Saif malik/MAVS-Ch10A"),
    ]
    for candidate in candidates:
        if (candidate / "configs" / "datasets").exists():
            return candidate.resolve()
    raise FileNotFoundError("Unable to locate Chapter 10A source root")


def _load_yaml(path: Path) -> dict[str, Any]:
    # console.log: phase2 Chapter 10A YAML config load begins.
    console.log(f"phase2.dataset_builder.yaml_load.start path={path}")
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"YAML config must be a mapping: {path}")
    # console.log: phase2 Chapter 10A YAML config load completed.
    console.log(f"phase2.dataset_builder.yaml_load.complete path={path}")
    return payload


def _load_source_frame(
    ch10a_root: Path, config: dict[str, Any], partition_row_count: int
) -> pd.DataFrame:
    dataset_id = str(config["dataset_id"])
    cache_key = (str(ch10a_root.resolve()), dataset_id, int(partition_row_count))
    cached = _SOURCE_CACHE.get(cache_key)
    if cached is not None:
        # console.log: phase2 source frame cache hit.
        console.log(f"phase2.dataset_builder.source.cache_hit dataset={dataset_id}")
        return cached.copy()

    # console.log: phase2 source frame acquisition begins.
    console.log(f"phase2.dataset_builder.source.load.start dataset={dataset_id}")
    source = config["source"]
    adapter = source["adapter"]
    if adapter == "sklearn_breast_cancer":
        data = load_breast_cancer(as_frame=True)
        frame = data.frame.copy()
        if "target" not in frame.columns:
            frame["target"] = data.target
    elif adapter in {"openml", "openml_with_manual_fallback"}:
        try:
            data = fetch_openml(
                data_id=int(source["openml_data_id"]), as_frame=True, parser="auto"
            )
            frame = data.frame.copy()
        except Exception:
            fallback = source.get("manual_fallback_path")
            if adapter != "openml_with_manual_fallback" or not fallback:
                raise
            fallback_path = ch10a_root / str(fallback)
            if not fallback_path.exists():
                raise
            frame = pd.read_csv(fallback_path)
    else:
        raise ValueError(f"Unsupported Chapter 10A source adapter: {adapter}")
    frame = frame.copy()
    frame.columns = [str(column) for column in frame.columns]
    if "source_row_index" not in frame.columns:
        frame.insert(0, "source_row_index", range(len(frame)))
    _validate_columns(frame, config)
    _SOURCE_CACHE[cache_key] = frame
    # console.log: phase2 source frame acquisition completed.
    console.log(
        "phase2.dataset_builder.source.load.complete "
        f"dataset={dataset_id} rows={len(frame)} columns={len(frame.columns)}"
    )
    return frame.copy()


def _select_working_frame(
    frame: pd.DataFrame,
    config: dict[str, Any],
    split_seed: int,
    partition_row_count: int,
    class_balance_strategy: str,
) -> pd.DataFrame:
    labels = _binary_labels(frame, config)
    if len(frame) <= partition_row_count:
        selected = frame.copy()
    elif class_balance_strategy == "minority_preserving_cap":
        rng = np.random.default_rng(split_seed)
        positive_indices = np.flatnonzero(labels.to_numpy(dtype=np.int8) == 1)
        negative_indices = np.flatnonzero(labels.to_numpy(dtype=np.int8) == 0)
        per_class = max(5, partition_row_count // 2)
        positive_take = min(len(positive_indices), per_class)
        negative_take = min(len(negative_indices), partition_row_count - positive_take)
        if positive_take < 5 or negative_take < 5:
            raise ValueError(
                f"Dataset {config['dataset_id']} does not have enough class support"
            )
        selected_indices = np.concatenate(
            [
                rng.choice(positive_indices, size=positive_take, replace=False),
                rng.choice(negative_indices, size=negative_take, replace=False),
            ]
        )
        rng.shuffle(selected_indices)
        selected = frame.iloc[np.sort(selected_indices)].copy()
    else:
        selected, _ = train_test_split(
            frame,
            train_size=partition_row_count,
            random_state=split_seed,
            stratify=labels,
            shuffle=True,
        )
        selected = selected.sort_values("source_row_index").copy()
    # console.log: phase2 working frame selection completed.
    console.log(
        "phase2.dataset_builder.working_frame.complete "
        f"dataset={config['dataset_id']} rows={len(selected)} strategy={class_balance_strategy}"
    )
    return selected.reset_index(drop=True)


def _binary_labels(frame: pd.DataFrame, config: dict[str, Any]) -> pd.Series:
    target = config["target"]
    raw = frame[target["column"]].astype(str)
    allowed = {str(target["positive_class"]), *[str(v) for v in target["negative_classes"]]}
    unknown = set(raw.dropna().unique()).difference(allowed)
    if unknown:
        raise ValueError(f"Unknown target labels for {config['dataset_id']}: {sorted(unknown)}")
    return (raw == str(target["positive_class"])).astype(int)


def _create_assignments(
    labels: pd.Series, split_seed: int, ratios: dict[str, float]
) -> dict[str, np.ndarray]:
    desired_counts = _desired_split_counts(len(labels), ratios)
    y = labels.to_numpy(dtype=np.int8)
    remaining_indices = np.arange(len(labels))
    remaining_labels = y
    assignments: dict[str, np.ndarray] = {}
    for offset, split_name in enumerate(SPLIT_ORDER[:-1]):
        desired_count = desired_counts[split_name]
        selected, remaining_indices, _, remaining_labels = train_test_split(
            remaining_indices,
            remaining_labels,
            train_size=desired_count,
            random_state=split_seed + offset,
            stratify=remaining_labels,
            shuffle=True,
        )
        assignments[split_name] = np.sort(selected)
    assignments[SPLIT_ORDER[-1]] = np.sort(remaining_indices)
    return assignments


def _desired_split_counts(row_count: int, ratios: dict[str, float]) -> dict[str, int]:
    raw_counts = {split_name: ratios[split_name] * row_count for split_name in SPLIT_ORDER}
    counts = {name: int(np.floor(value)) for name, value in raw_counts.items()}
    remainder = row_count - sum(counts.values())
    fractional = sorted(
        SPLIT_ORDER,
        key=lambda split_name: (raw_counts[split_name] - counts[split_name], split_name),
        reverse=True,
    )
    for split_name in fractional[:remainder]:
        counts[split_name] += 1
    if any(counts[split_name] <= 0 for split_name in SPLIT_ORDER):
        raise ValueError(f"Split ratios produce an empty split: rows={row_count} counts={counts}")
    return counts


def _preprocess_splits(
    frame: pd.DataFrame,
    labels: pd.Series,
    assignments: dict[str, np.ndarray],
    config: dict[str, Any],
) -> dict[str, SplitData]:
    feature_columns = list(config["features"].get("numeric", [])) + list(
        config["features"].get("categorical", [])
    )
    feature_frame = _normalize_missing(frame[feature_columns], config["preprocessing"])
    transformer = _build_transformer(config)
    # console.log: phase2 train-only preprocessing fit begins.
    console.log(
        "phase2.dataset_builder.preprocessing.fit.start "
        f"dataset={config['dataset_id']} train_rows={len(assignments['train'])}"
    )
    transformer.fit(feature_frame.iloc[assignments["train"]], labels.iloc[assignments["train"]])
    # console.log: phase2 train-only preprocessing fit completed.
    console.log(f"phase2.dataset_builder.preprocessing.fit.complete dataset={config['dataset_id']}")
    splits: dict[str, SplitData] = {}
    for split_name in SPLIT_ORDER:
        indices = assignments[split_name]
        X = np.asarray(transformer.transform(feature_frame.iloc[indices]), dtype=np.float64)
        y = labels.iloc[indices].to_numpy(dtype=np.int8)
        row_ids = frame.iloc[indices]["source_row_index"].to_numpy(dtype=np.int64)
        row_hashes = tuple(_row_hash(str(config["dataset_id"]), int(row_id)) for row_id in row_ids)
        splits[split_name] = SplitData(
            name=split_name,
            X=X,
            y=y,
            row_ids=row_ids,
            row_hashes=row_hashes,
            feature_matrix_hash=_hash_array(X),
            label_hash=_hash_array(y),
            row_hash=sha256_json(list(row_hashes)),
        )
        # console.log: phase2 empirical split transformation completed.
        console.log(
            "phase2.dataset_builder.preprocessing.split.complete "
            f"dataset={config['dataset_id']} split={split_name} rows={len(y)} features={X.shape[1]}"
        )
    return splits


def _build_transformer(config: dict[str, Any]) -> ColumnTransformer:
    preprocessing = config["preprocessing"]
    numeric_steps: list[tuple[str, Any]] = [
        ("imputer", SimpleImputer(strategy=preprocessing["numeric_imputation"])),
    ]
    if preprocessing["numeric_scaling"] == "standard":
        numeric_steps.append(("scaler", StandardScaler()))
    categorical_steps: list[tuple[str, Any]] = [
        ("imputer", SimpleImputer(strategy=preprocessing["categorical_imputation"])),
    ]
    if preprocessing["categorical_encoding"] == "one_hot":
        categorical_steps.append(("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)))
    transformers: list[tuple[str, Any, list[str]]] = []
    if config["features"].get("numeric"):
        transformers.append(("numeric", Pipeline(numeric_steps), list(config["features"]["numeric"])))
    if config["features"].get("categorical"):
        transformers.append(
            ("categorical", Pipeline(categorical_steps), list(config["features"]["categorical"]))
        )
    return ColumnTransformer(transformers=transformers, remainder="drop")


def _normalize_missing(frame: pd.DataFrame, preprocessing: dict[str, Any]) -> pd.DataFrame:
    result = frame.copy()
    for marker in preprocessing.get("missing_values", []):
        result = result.replace(marker, pd.NA)
    return result


def _validate_columns(frame: pd.DataFrame, config: dict[str, Any]) -> None:
    required = set(config["features"].get("numeric", []))
    required.update(config["features"].get("categorical", []))
    required.add(config["target"]["column"])
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns for {config['dataset_id']}: {missing}")


def _row_hash(dataset_id: str, source_row_index: int) -> str:
    return sha256_json({"dataset_id": dataset_id, "source_row_index": int(source_row_index)})


def _hash_array(array: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(array)
    payload = {
        "shape": list(contiguous.shape),
        "dtype": str(contiguous.dtype),
        "bytes_sha256": __import__("hashlib").sha256(contiguous.tobytes()).hexdigest(),
    }
    return sha256_json(payload)


def _hash_dataframe(frame: pd.DataFrame) -> str:
    return __import__("hashlib").sha256(
        frame.to_csv(index=False, lineterminator="\n").encode("utf-8")
    ).hexdigest()
