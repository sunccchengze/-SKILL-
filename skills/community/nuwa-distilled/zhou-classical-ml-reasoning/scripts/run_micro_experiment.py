#!/usr/bin/env python3
"""Dependency-free classical-ML experiment with split-before-fit discipline."""
from __future__ import annotations

import argparse
import json
import math
import platform
import random
import sys
from pathlib import Path


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def log_loss(rows, weights) -> float:
    total = 0.0
    for _, features, label in rows:
        p = min(max(sigmoid(weights[0] + sum(w * x for w, x in zip(weights[1:], features))), 1e-12), 1 - 1e-12)
        total -= label * math.log(p) + (1 - label) * math.log(1 - p)
    return total / len(rows)


def confusion(rows, weights):
    out = {"tn": 0, "fp": 0, "fn": 0, "tp": 0}
    detailed = []
    for sample_id, features, label in rows:
        p = sigmoid(weights[0] + sum(w * x for w, x in zip(weights[1:], features)))
        pred = int(p >= 0.5)
        key = "tp" if pred == label == 1 else "tn" if pred == label == 0 else "fp" if pred == 1 else "fn"
        out[key] += 1
        loss = -(label * math.log(max(p, 1e-12)) + (1 - label) * math.log(max(1 - p, 1e-12)))
        detailed.append({"sample_id": sample_id, "label": label, "prediction": pred, "probability": round(p, 6), "log_loss": round(loss, 6), "bucket": key})
    out["accuracy"] = (out["tp"] + out["tn"]) / len(rows)
    return out, detailed


def run(seed: int, epochs: int, learning_rate: float) -> dict:
    if epochs < 1 or learning_rate <= 0:
        raise ValueError("epochs and learning rate must be positive")
    rng = random.Random(seed)
    rows = []
    for idx in range(160):
        x1, x2 = rng.gauss(0, 1), rng.gauss(0, 1)
        label = int(1.4 * x1 - 0.9 * x2 + rng.gauss(0, 0.7) > 0)
        rows.append((idx, [x1, x2], label))
    rng.shuffle(rows)
    train_raw, validation_raw, test_raw = rows[:100], rows[100:130], rows[130:]
    means = [sum(row[1][j] for row in train_raw) / len(train_raw) for j in range(2)]
    stds = [math.sqrt(sum((row[1][j] - means[j]) ** 2 for row in train_raw) / len(train_raw)) for j in range(2)]
    def transform(part):
        return [(idx, [(features[j] - means[j]) / stds[j] for j in range(2)], label) for idx, features, label in part]
    train, validation, test = transform(train_raw), transform(validation_raw), transform(test_raw)
    majority = int(sum(label for _, _, label in train) >= len(train) / 2)
    baseline_validation_accuracy = sum(label == majority for _, _, label in validation) / len(validation)
    weights = [0.0, 0.0, 0.0]
    history = []
    for epoch in range(1, epochs + 1):
        gradients = [0.0, 0.0, 0.0]
        for _, features, label in train:
            p = sigmoid(weights[0] + sum(w * x for w, x in zip(weights[1:], features)))
            error = p - label
            gradients[0] += error
            gradients[1] += error * features[0]
            gradients[2] += error * features[1]
        weights = [w - learning_rate * g / len(train) for w, g in zip(weights, gradients)]
        val_confusion, _ = confusion(validation, weights)
        history.append({"epoch": epoch, "train_log_loss": round(log_loss(train, weights), 8), "validation_log_loss": round(log_loss(validation, weights), 8), "validation_accuracy": round(val_confusion["accuracy"], 8)})
    validation_confusion, _ = confusion(validation, weights)
    # Frozen configuration: final test touched once below.
    test_confusion, test_details = confusion(test, weights)
    hardest = sorted(test_details, key=lambda row: (-row["log_loss"], row["sample_id"]))[:3]
    return {
        "exercise": "split-baseline",
        "problem_card": {"task": "binary prediction", "prediction_unit": "synthetic independent row", "label_timing": "generated before modeling", "deployment_distribution": "same synthetic process only", "primary_metric": "log loss", "secondary_metric": "accuracy"},
        "hypothesis": "Train-only standardized logistic regression will beat a training-majority baseline on validation accuracy.",
        "model_assumption_card": {"family": "logistic regression", "inductive_bias": "linear log-odds", "diagnostic": "validation loss/accuracy and error buckets", "falsifier": "no baseline gain or structured nonlinear residual errors"},
        "configuration": {"seed": seed, "epochs": epochs, "learning_rate": learning_rate, "split_sizes": {"train": 100, "validation": 30, "test": 30}},
        "environment": {"python": sys.version.split()[0], "platform": platform.platform(), "dependencies": "standard library only"},
        "data_flow": "generate -> split -> fit means/stds on train only -> transform -> train/validation -> freeze -> one final test",
        "preprocessing_fit": {"source": "train only", "means": means, "stds": stds},
        "baseline": {"training_majority_class": majority, "validation_accuracy": baseline_validation_accuracy},
        "metric_history": history,
        "validation": validation_confusion,
        "final_test": {"touches": 1, **test_confusion},
        "artifact_path": "this JSON output",
        "error_analysis": {"hardest_test_examples": hardest, "buckets": {key: test_confusion[key] for key in ("fp", "fn", "tp", "tn")}, "warning": "Do not tune this version from final-test errors."},
        "hypothesis_status": "supported" if validation_confusion["accuracy"] > baseline_validation_accuracy else "refuted_or_uncertain",
        "uncertainty": "one finite synthetic split; no interval or deployment extrapolation",
        "next_experiment": "Keep split fixed; add one x1*x2 feature to test whether a nonlinear interaction improves validation log loss.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exercise", choices=("split-baseline",), default="split-baseline")
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--learning-rate", type=float, default=0.1)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = run(args.seed, args.epochs, args.learning_rate)
    except ValueError as exc:
        parser.error(str(exc))
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
