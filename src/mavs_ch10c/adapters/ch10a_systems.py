"""Shared Chapter 10 system, dataset, and specialist contracts."""

from __future__ import annotations

REQUIRED_DATASETS = [
    "breast_cancer_wisconsin",
    "adult_income",
    "credit_card_fraud",
    "bank_marketing",
]

REQUIRED_SPECIALISTS = [
    "random_forest",
    "gradient_boosted_trees",
    "mlp",
]

REQUIRED_SYSTEMS = [
    "single_model",
    "mean_ensemble",
    "static_weighted_ensemble",
    "veto_mavs",
    "pure_mavs_gc",
]


def assert_contract_matches(config: dict[str, object]) -> None:
    """Validate imported config lists against the Chapter 10 contract."""

    for key, expected in (
        ("required_datasets", REQUIRED_DATASETS),
        ("required_specialists", REQUIRED_SPECIALISTS),
        ("required_systems", REQUIRED_SYSTEMS),
    ):
        actual = list(config.get(key, []))
        missing = sorted(set(expected) - set(actual))
        unexpected = sorted(set(actual) - set(expected))
        if missing or unexpected:
            raise ValueError(
                f"{key} contract mismatch: missing={missing}, unexpected={unexpected}"
            )
