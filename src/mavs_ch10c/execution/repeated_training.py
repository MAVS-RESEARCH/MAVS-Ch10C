"""Empirical repeated specialist training for Phase 2."""

from __future__ import annotations

import hashlib
import pickle
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, log_loss
from sklearn.neural_network import MLPClassifier

from mavs_ch10c import console
from mavs_ch10c.execution.dataset_builder import PartitionBundle, SplitData
from mavs_ch10c.verification.hash_utils import sha256_file, sha256_json


@dataclass(frozen=True)
class SpecialistFitRecord:
    fit_id: str
    dataset_id: str
    specialist_id: str
    execution_seed: int
    split_schedule_id: str
    initialization_schedule_id: str
    model_config_hash: str
    model_family: str
    train_partition_hash: str
    validation_partition_hash: str
    calibration_partition_hash: str
    locked_benchmark_hash: str
    audit_benchmark_hash: str
    checkpoint_hash: str
    probability_output_hash: str
    calibration_object_hash: str
    calibration_split_hash: str
    training_row_count: int
    validation_row_count: int
    calibration_row_count: int
    feature_count: int
    train_accuracy: float
    train_f1: float
    validation_accuracy: float
    validation_f1: float
    calibration_error_before: float
    calibration_error_after: float
    convergence_status: str
    epoch_count: int
    loss_curve_hash: str
    model_specifics: str
    effective_random_seed: int
    rf_n_estimators: str
    rf_max_depth: str
    rf_class_weight: str
    rf_max_features: str
    gbt_learning_rate: str
    gbt_estimator_count: str
    gbt_max_leaf_nodes: str
    gbt_min_samples_leaf: str
    mlp_hidden_layer_sizes: str
    mlp_activation: str
    mlp_solver: str
    mlp_max_epochs: str
    mlp_patience: str
    tuning_performed: bool


@dataclass(frozen=True)
class FittedSpecialist:
    record: SpecialistFitRecord
    validation_probabilities: np.ndarray
    benchmark_probabilities: np.ndarray
    benchmark_supports: np.ndarray


_FIT_CACHE: dict[tuple[str, int, str, str, str, str], FittedSpecialist] = {}


def train_specialists_for_unit(
    unit: dict[str, Any],
    partition_bundle: PartitionBundle,
    ch10a_root: Path,
    specialist_config_hashes: dict[str, str],
) -> list[FittedSpecialist]:
    """Train active specialists for one empirical repetition unit."""

    # console.log: phase2 empirical repeated training begins.
    console.log(
        "phase2.repeated_training.train_unit.start "
        f"dataset={unit['dataset_id']} composition={unit['specialist_composition_id']}"
    )
    fitted: list[FittedSpecialist] = []
    for specialist_id in str(unit["specialist_ids"]).split(","):
        fitted.append(
            train_specialist(
                unit=unit,
                partition_bundle=partition_bundle,
                specialist_id=specialist_id,
                ch10a_root=ch10a_root,
                specialist_config_hashes=specialist_config_hashes,
            )
        )
    # console.log: phase2 empirical repeated training completed.
    console.log(f"phase2.repeated_training.train_unit.complete fits={len(fitted)}")
    return fitted


def train_specialist(
    *,
    unit: dict[str, Any],
    partition_bundle: PartitionBundle,
    specialist_id: str,
    ch10a_root: Path,
    specialist_config_hashes: dict[str, str],
) -> FittedSpecialist:
    """Fit one specialist and calibration object using only allowed partitions."""

    cache_key = (
        str(unit["dataset_id"]),
        int(unit["execution_seed"]),
        str(unit["split_schedule_id"]),
        str(unit["initialization_schedule_id"]),
        specialist_id,
        partition_bundle.partition_manifest_hash,
    )
    cached = _FIT_CACHE.get(cache_key)
    if cached is not None:
        # console.log: phase2 empirical specialist fit cache hit.
        console.log(
            "phase2.repeated_training.fit.cache_hit "
            f"dataset={unit['dataset_id']} specialist={specialist_id}"
        )
        return cached

    # console.log: phase2 empirical specialist fit begins.
    console.log(
        "phase2.repeated_training.fit.start "
        f"dataset={unit['dataset_id']} specialist={specialist_id} seed={unit['execution_seed']}"
    )
    model_config_path = ch10a_root / "configs" / "models" / f"{specialist_id}.yaml"
    calibration_config_path = ch10a_root / "configs" / "models" / "calibration.yaml"
    model_config = _load_yaml(model_config_path)
    calibration_config = _load_yaml(calibration_config_path)
    model_config_hash = _lookup_model_config_hash(specialist_id, specialist_config_hashes)
    empirical_seed = _empirical_seed(model_config, unit)
    estimator = _build_estimator(model_config, empirical_seed)
    train = partition_bundle.splits["train"]
    validation = partition_bundle.splits["validation"]
    calibration = partition_bundle.splits["calibration"]
    benchmark = partition_bundle.benchmark
    _assert_split_isolation(partition_bundle)
    convergence = _fit_estimator(estimator, model_config, train, validation)
    raw_calibration = _positive_probabilities(estimator, calibration.X)
    calibrator = _fit_sigmoid_calibrator(raw_calibration, calibration.y, calibration_config)
    train_prob = calibrator.predict_proba(_logit_features(_positive_probabilities(estimator, train.X)))[:, 1]
    validation_prob = calibrator.predict_proba(
        _logit_features(_positive_probabilities(estimator, validation.X))
    )[:, 1]
    calibration_prob = calibrator.predict_proba(_logit_features(raw_calibration))[:, 1]
    benchmark_prob = calibrator.predict_proba(
        _logit_features(_positive_probabilities(estimator, benchmark.X))
    )[:, 1]
    benchmark_support = 2.0 * benchmark_prob - 1.0
    checkpoint_hash = _hash_pickle(
        {
            "estimator": estimator,
            "calibrator": calibrator,
            "model_config_hash": model_config_hash,
            "partition_manifest_hash": partition_bundle.partition_manifest_hash,
        }
    )
    probability_output_hash = _hash_array(benchmark_prob)
    calibration_object_hash = _hash_pickle(calibrator)
    loss_curve = convergence.get("validation_loss_curve", [])
    base = {
        "dataset_id": unit["dataset_id"],
        "specialist_id": specialist_id,
        "execution_seed": int(unit["execution_seed"]),
        "split_schedule_id": unit["split_schedule_id"],
        "initialization_schedule_id": unit["initialization_schedule_id"],
        "model_config_hash": model_config_hash,
        "partition_manifest_hash": partition_bundle.partition_manifest_hash,
    }
    model_specifics = _model_specifics(model_config, partition_bundle)
    record = SpecialistFitRecord(
        fit_id=sha256_json(base)[:24],
        dataset_id=str(unit["dataset_id"]),
        specialist_id=specialist_id,
        execution_seed=int(unit["execution_seed"]),
        split_schedule_id=str(unit["split_schedule_id"]),
        initialization_schedule_id=str(unit["initialization_schedule_id"]),
        model_config_hash=model_config_hash,
        model_family=str(model_config["model_family"]),
        train_partition_hash=partition_bundle.train_hash,
        validation_partition_hash=partition_bundle.validation_hash,
        calibration_partition_hash=partition_bundle.calibration_hash,
        locked_benchmark_hash=partition_bundle.locked_benchmark_hash,
        audit_benchmark_hash=partition_bundle.audit_benchmark_hash,
        checkpoint_hash=checkpoint_hash,
        probability_output_hash=probability_output_hash,
        calibration_object_hash=calibration_object_hash,
        calibration_split_hash=partition_bundle.calibration_hash,
        training_row_count=partition_bundle.train_count,
        validation_row_count=partition_bundle.validation_count,
        calibration_row_count=partition_bundle.calibration_count,
        feature_count=partition_bundle.feature_count,
        train_accuracy=_accuracy(train.y, train_prob),
        train_f1=_f1(train.y, train_prob),
        validation_accuracy=_accuracy(validation.y, validation_prob),
        validation_f1=_f1(validation.y, validation_prob),
        calibration_error_before=_expected_calibration_error(calibration.y, raw_calibration),
        calibration_error_after=_expected_calibration_error(calibration.y, calibration_prob),
        convergence_status=str(convergence["status"]),
        epoch_count=int(convergence["epoch_count"]),
        loss_curve_hash=sha256_json(loss_curve),
        model_specifics=sha256_json(model_specifics),
        effective_random_seed=empirical_seed,
        rf_n_estimators=_specific(model_specifics, "rf_n_estimators"),
        rf_max_depth=_specific(model_specifics, "rf_max_depth"),
        rf_class_weight=_specific(model_specifics, "rf_class_weight"),
        rf_max_features=_specific(model_specifics, "rf_max_features"),
        gbt_learning_rate=_specific(model_specifics, "gbt_learning_rate"),
        gbt_estimator_count=_specific(model_specifics, "gbt_estimator_count"),
        gbt_max_leaf_nodes=_specific(model_specifics, "gbt_max_leaf_nodes"),
        gbt_min_samples_leaf=_specific(model_specifics, "gbt_min_samples_leaf"),
        mlp_hidden_layer_sizes=_specific(model_specifics, "mlp_hidden_layer_sizes"),
        mlp_activation=_specific(model_specifics, "mlp_activation"),
        mlp_solver=_specific(model_specifics, "mlp_solver"),
        mlp_max_epochs=_specific(model_specifics, "mlp_max_epochs"),
        mlp_patience=_specific(model_specifics, "mlp_patience"),
        tuning_performed=False,
    )
    result = FittedSpecialist(
        record=record,
        validation_probabilities=validation_prob,
        benchmark_probabilities=benchmark_prob,
        benchmark_supports=benchmark_support,
    )
    _FIT_CACHE[cache_key] = result
    # console.log: phase2 empirical specialist fit completed.
    console.log(
        "phase2.repeated_training.fit.complete "
        f"fit_id={record.fit_id} validation_f1={record.validation_f1:.6f}"
    )
    return result


def fit_records_hash(records: list[SpecialistFitRecord]) -> str:
    return sha256_json([asdict(record) for record in records])


def _load_yaml(path: Path) -> dict[str, Any]:
    # console.log: phase2 model YAML load begins.
    console.log(f"phase2.repeated_training.yaml_load.start path={path}")
    with path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"YAML config must be a mapping: {path}")
    # console.log: phase2 model YAML load completed.
    console.log(f"phase2.repeated_training.yaml_load.complete path={path}")
    return payload


def _build_estimator(model_config: dict[str, Any], seed: int):
    model_id = model_config["model_id"]
    training = model_config["training"]
    # console.log: phase2 frozen estimator build begins.
    console.log(f"phase2.repeated_training.estimator.start model={model_id} seed={seed}")
    if model_id == "random_forest":
        estimator = RandomForestClassifier(
            n_estimators=int(training["n_estimators"]),
            max_depth=int(training["max_depth"]),
            min_samples_leaf=int(training["min_samples_leaf"]),
            min_samples_split=int(training["min_samples_split"]),
            max_features=training["max_features"],
            class_weight=training["class_weight"],
            n_jobs=1,
            bootstrap=bool(training["bootstrap"]),
            random_state=seed,
        )
    elif model_id == "gradient_boosted_trees":
        estimator = HistGradientBoostingClassifier(
            max_iter=int(training["max_iter"]),
            learning_rate=float(training["learning_rate"]),
            max_leaf_nodes=int(training["max_leaf_nodes"]),
            min_samples_leaf=int(training["min_samples_leaf"]),
            l2_regularization=float(training["l2_regularization"]),
            random_state=seed,
            early_stopping=False,
        )
    elif model_id == "mlp":
        estimator = MLPClassifier(
            hidden_layer_sizes=tuple(int(v) for v in training["hidden_layer_sizes"]),
            activation=training["activation"],
            solver=training["solver"],
            alpha=float(training["alpha"]),
            learning_rate_init=float(training["learning_rate_init"]),
            batch_size=int(training["batch_size"]),
            max_iter=1,
            warm_start=True,
            shuffle=True,
            random_state=seed,
        )
    else:
        raise ValueError(f"Unsupported model id: {model_id}")
    # console.log: phase2 frozen estimator build completed.
    console.log(f"phase2.repeated_training.estimator.complete model={model_id}")
    return estimator


def _fit_estimator(
    estimator: Any,
    model_config: dict[str, Any],
    train: SplitData,
    validation: SplitData,
) -> dict[str, Any]:
    model_id = model_config["model_id"]
    sample_weight = _balanced_sample_weight(train.y)
    if model_id != "mlp":
        fit_kwargs = {"sample_weight": sample_weight} if model_id == "gradient_boosted_trees" else {}
        # console.log: phase2 non-MLP estimator fit begins.
        console.log(f"phase2.repeated_training.fit_estimator.start model={model_id}")
        estimator.fit(train.X, train.y, **fit_kwargs)
        # console.log: phase2 non-MLP estimator fit completed.
        console.log(f"phase2.repeated_training.fit_estimator.complete model={model_id}")
        return {
            "status": "single_fit_complete",
            "epoch_count": int(getattr(estimator, "n_iter_", 1) or 1),
            "validation_loss_curve": [],
        }
    training = model_config["training"]
    max_epochs = int(training["max_epochs"])
    patience = int(training["patience"])
    tolerance = float(training["tolerance"])
    best_loss = float("inf")
    best_state: dict[str, Any] | None = None
    stale_epochs = 0
    losses: list[float] = []
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        warnings.filterwarnings("ignore", message="Got `batch_size` less than 1 or larger than sample size.*")
        for epoch in range(1, max_epochs + 1):
            # console.log: phase2 MLP epoch fit begins.
            console.log(f"phase2.repeated_training.mlp_epoch.start epoch={epoch}")
            try:
                estimator.fit(train.X, train.y, sample_weight=sample_weight)
            except TypeError:
                estimator.fit(train.X, train.y)
            probabilities = _positive_probabilities(estimator, validation.X)
            current_loss = float(log_loss(validation.y, np.column_stack([1.0 - probabilities, probabilities])))
            losses.append(current_loss)
            if current_loss + tolerance < best_loss:
                best_loss = current_loss
                best_state = _extract_mlp_state(estimator)
                stale_epochs = 0
            else:
                stale_epochs += 1
            # console.log: phase2 MLP epoch fit completed.
            console.log(
                f"phase2.repeated_training.mlp_epoch.complete epoch={epoch} validation_log_loss={current_loss:.8f}"
            )
            if stale_epochs >= patience:
                break
    if best_state is not None:
        _restore_mlp_state(estimator, best_state)
    return {
        "status": "fixed_validation_early_stopping_complete",
        "epoch_count": len(losses),
        "validation_loss_curve": losses,
    }


def _fit_sigmoid_calibrator(
    probabilities: np.ndarray, labels: np.ndarray, calibration_config: dict[str, Any]
) -> LogisticRegression:
    # console.log: phase2 calibration fit begins.
    console.log(f"phase2.repeated_training.calibration.start rows={len(labels)}")
    clip = calibration_config["probability_clip"]
    model = LogisticRegression(
        random_state=int(calibration_config["random_seed"]),
        max_iter=1000,
        solver="lbfgs",
    )
    model.fit(_logit_features(probabilities, float(clip["min"]), float(clip["max"])), labels)
    # console.log: phase2 calibration fit completed.
    console.log("phase2.repeated_training.calibration.complete")
    return model


def _positive_probabilities(estimator: Any, X: np.ndarray) -> np.ndarray:
    probabilities = estimator.predict_proba(X)
    if probabilities.ndim != 2 or probabilities.shape[1] != 2:
        raise ValueError(f"Expected binary predict_proba output, got {probabilities.shape}")
    return np.asarray(probabilities[:, 1], dtype=np.float64)


def _logit_features(probabilities: np.ndarray, clip_min: float = 1e-6, clip_max: float = 0.999999) -> np.ndarray:
    clipped = np.clip(np.asarray(probabilities, dtype=np.float64), clip_min, clip_max)
    logits = np.log(clipped / (1.0 - clipped))
    return logits.reshape(-1, 1)


def _balanced_sample_weight(labels: np.ndarray) -> np.ndarray:
    labels = np.asarray(labels, dtype=np.int8)
    counts = np.bincount(labels, minlength=2).astype(np.float64)
    weights = np.zeros_like(counts)
    nonzero = counts > 0
    weights[nonzero] = len(labels) / (2.0 * counts[nonzero])
    return weights[labels]


def _accuracy(labels: np.ndarray, probabilities: np.ndarray) -> float:
    return float(accuracy_score(labels, (probabilities >= 0.5).astype(np.int8)))


def _f1(labels: np.ndarray, probabilities: np.ndarray) -> float:
    return float(f1_score(labels, (probabilities >= 0.5).astype(np.int8), zero_division=0))


def _expected_calibration_error(labels: np.ndarray, probabilities: np.ndarray, bins: int = 10) -> float:
    labels = np.asarray(labels, dtype=np.int8)
    probabilities = np.asarray(probabilities, dtype=np.float64)
    edges = np.linspace(0.0, 1.0, bins + 1)
    total = float(len(labels))
    error = 0.0
    for lower, upper in zip(edges[:-1], edges[1:]):
        if upper == 1.0:
            mask = (probabilities >= lower) & (probabilities <= upper)
        else:
            mask = (probabilities >= lower) & (probabilities < upper)
        if not np.any(mask):
            continue
        confidence = float(np.mean(probabilities[mask]))
        accuracy = float(np.mean(labels[mask]))
        error += (float(np.sum(mask)) / total) * abs(accuracy - confidence)
    return float(error)


def _hash_array(array: np.ndarray) -> str:
    contiguous = np.ascontiguousarray(array)
    digest = hashlib.sha256()
    digest.update(str(contiguous.shape).encode("utf-8"))
    digest.update(str(contiguous.dtype).encode("utf-8"))
    digest.update(contiguous.tobytes())
    return digest.hexdigest()


def _hash_pickle(value: Any) -> str:
    return hashlib.sha256(pickle.dumps(value, protocol=5)).hexdigest()


def _extract_mlp_state(estimator: Any) -> dict[str, Any]:
    return {
        "coefs_": [coef.copy() for coef in estimator.coefs_],
        "intercepts_": [intercept.copy() for intercept in estimator.intercepts_],
        "n_iter_": getattr(estimator, "n_iter_", None),
        "loss_": getattr(estimator, "loss_", None),
        "loss_curve_": list(getattr(estimator, "loss_curve_", [])),
    }


def _restore_mlp_state(estimator: Any, state: dict[str, Any]) -> None:
    estimator.coefs_ = [coef.copy() for coef in state["coefs_"]]
    estimator.intercepts_ = [intercept.copy() for intercept in state["intercepts_"]]
    estimator.n_iter_ = state["n_iter_"]
    estimator.loss_ = state["loss_"]
    estimator.loss_curve_ = list(state["loss_curve_"])


def _empirical_seed(model_config: dict[str, Any], unit: dict[str, Any]) -> int:
    return int(
        (
            int(model_config["random_seed"])
            + int(unit["execution_seed"])
            + int(unit["initialization_seed"])
        )
        % (2**31 - 1)
    )


def _lookup_model_config_hash(
    specialist_id: str, specialist_config_hashes: dict[str, str]
) -> str:
    suffix = f"configs/models/{specialist_id}.yaml"
    for path, digest in specialist_config_hashes.items():
        if path.endswith(suffix):
            return digest
    raise KeyError(f"Missing frozen model config hash for specialist: {specialist_id}")


def _model_specifics(model_config: dict[str, Any], partition_bundle: PartitionBundle) -> dict[str, Any]:
    training = dict(model_config["training"])
    specifics: dict[str, Any] = {
        "model_id": model_config["model_id"],
        "model_family": model_config["model_family"],
        "training": training,
        "feature_count": partition_bundle.feature_count,
        "training_row_count": partition_bundle.train_count,
    }
    model_id = str(model_config["model_id"])
    if model_id == "random_forest":
        specifics.update(
            {
                "rf_n_estimators": training["n_estimators"],
                "rf_max_depth": training["max_depth"],
                "rf_class_weight": training["class_weight"],
                "rf_max_features": training["max_features"],
            }
        )
    elif model_id == "gradient_boosted_trees":
        specifics.update(
            {
                "gbt_learning_rate": training["learning_rate"],
                "gbt_estimator_count": training["max_iter"],
                "gbt_max_leaf_nodes": training["max_leaf_nodes"],
                "gbt_min_samples_leaf": training["min_samples_leaf"],
            }
        )
    elif model_id == "mlp":
        specifics.update(
            {
                "mlp_hidden_layer_sizes": ",".join(
                    str(value) for value in training["hidden_layer_sizes"]
                ),
                "mlp_activation": training["activation"],
                "mlp_solver": training["solver"],
                "mlp_max_epochs": training["max_epochs"],
                "mlp_patience": training["patience"],
            }
        )
    return specifics


def _specific(model_specifics: dict[str, Any], key: str) -> str:
    value = model_specifics.get(key, "")
    return "" if value is None else str(value)


def _assert_split_isolation(partition_bundle: PartitionBundle) -> None:
    rows: dict[str, set[str]] = {
        split_name: set(split.row_hashes)
        for split_name, split in partition_bundle.splits.items()
    }
    for left_name, left_rows in rows.items():
        for right_name, right_rows in rows.items():
            if left_name >= right_name:
                continue
            overlap = left_rows.intersection(right_rows)
            if overlap:
                raise ValueError(
                    f"Benchmark isolation failure: {left_name} overlaps {right_name}"
                )
