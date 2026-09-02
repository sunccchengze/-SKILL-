#!/usr/bin/env python3
"""Dependency-free, deterministic LAB-TRACE demonstration with train-only preprocessing."""
from __future__ import annotations

import argparse
import json
import math
import platform
import random
import sys
from pathlib import Path


def mse(rows: list[tuple[float, float]], w: float, b: float) -> float:
    return sum((w * x + b - y) ** 2 for x, y in rows) / len(rows)


def make_data(seed: int) -> list[tuple[int, float, float]]:
    rng = random.Random(seed)
    rows = []
    for idx in range(120):
        x = rng.uniform(-3.0, 3.0)
        noise = rng.gauss(0.0, 0.25)
        rows.append((idx, x, 2.5 * x - 0.7 + noise))
    rng.shuffle(rows)
    return rows


def run(seed: int, epochs: int, learning_rate: float) -> dict:
    if epochs < 1 or learning_rate <= 0:
        raise ValueError("epochs and learning rate must be positive")
    raw = make_data(seed)
    train_raw, validation_raw, test_raw = raw[:80], raw[80:100], raw[100:]
    mean_x = sum(x for _, x, _ in train_raw) / len(train_raw)
    std_x = math.sqrt(sum((x - mean_x) ** 2 for _, x, _ in train_raw) / len(train_raw))
    transform = lambda rows: [(idx, (x - mean_x) / std_x, y) for idx, x, y in rows]
    train, validation, test = transform(train_raw), transform(validation_raw), transform(test_raw)
    train_xy = [(x, y) for _, x, y in train]
    validation_xy = [(x, y) for _, x, y in validation]
    test_xy = [(x, y) for _, x, y in test]
    baseline_b = sum(y for _, y in train_xy) / len(train_xy)
    baseline_validation = mse(validation_xy, 0.0, baseline_b)
    w = b = 0.0
    history = []
    for epoch in range(1, epochs + 1):
        grad_w = 2 * sum((w * x + b - y) * x for x, y in train_xy) / len(train_xy)
        grad_b = 2 * sum(w * x + b - y for x, y in train_xy) / len(train_xy)
        w -= learning_rate * grad_w
        b -= learning_rate * grad_b
        history.append({"epoch": epoch, "train_mse": round(mse(train_xy, w, b), 8), "validation_mse": round(mse(validation_xy, w, b), 8)})
    # The final test is evaluated exactly here, after the training configuration is frozen.
    test_mse = mse(test_xy, w, b)
    errors = sorted(
        ({"sample_id": idx, "prediction": round(w * x + b, 6), "target": round(y, 6), "absolute_error": round(abs(w * x + b - y), 6)} for idx, x, y in test),
        key=lambda row: (-row["absolute_error"], row["sample_id"]),
    )[:3]
    return {
        "question": "Can gradient descent recover a noisy linear relationship without preprocessing leakage?",
        "hypothesis": "A trained linear model will beat a train-mean baseline on validation MSE.",
        "prediction": "Validation MSE will decrease over epochs; final test is touched once after freezing.",
        "configuration": {"seed": seed, "epochs": epochs, "learning_rate": learning_rate, "split_sizes": {"train": 80, "validation": 20, "test": 20}},
        "environment": {"python": sys.version.split()[0], "platform": platform.platform(), "dependencies": "standard library only"},
        "data_flow": "generate -> split -> fit mean/std on train only -> transform each split -> train/validation -> frozen final test",
        "preprocessing_fit": {"source": "train only", "mean_x": mean_x, "std_x": std_x},
        "baseline": {"model": "training-target mean", "validation_mse": baseline_validation},
        "metric_history": history,
        "frozen_model": {"weight_on_standardized_x": w, "bias": b},
        "final_test": {"touches": 1, "mse": test_mse},
        "artifact_path": "this JSON output",
        "error_analysis": {"largest_test_residuals": errors, "candidate_buckets": ["noise/outlier", "range edge", "model mismatch"], "warning": "Do not tune this experiment version from final-test errors."},
        "hypothesis_status": "supported" if history[-1]["validation_mse"] < baseline_validation else "refuted_or_uncertain",
        "next_experiment": "Hold split and seed fixed; add one quadratic feature to test the model-mismatch bucket.",
        "limitations": ["synthetic small data", "one split", "not a D2L framework notebook", "no deployment claim"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--learning-rate", type=float, default=0.05)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        data = run(args.seed, args.epochs, args.learning_rate)
    except ValueError as exc:
        parser.error(str(exc))
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
