#!/usr/bin/env python3
"""Numerically check a scalar logistic cross-entropy derivative."""
from __future__ import annotations

import argparse
import json
import math
import platform
import sys
from pathlib import Path


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


def loss(weight: float, x: float, target: int, bias: float = -0.2) -> float:
    z = weight * x + bias
    return max(z, 0.0) - z * target + math.log1p(math.exp(-abs(z)))


def analytic_gradient(weight: float, x: float, target: int, bias: float = -0.2) -> float:
    return (sigmoid(weight * x + bias) - target) * x


def central_difference(weight: float, x: float, target: int, step: float) -> float:
    return (loss(weight + step, x, target) - loss(weight - step, x, target)) / (2 * step)


def relative_error(a: float, b: float) -> float:
    return abs(a - b) / max(1e-12, abs(a) + abs(b))


def run(x: float, target: int, step: float, weight: float = 0.4) -> dict:
    if target not in {0, 1}:
        raise ValueError("target must be 0 or 1")
    if step <= 0:
        raise ValueError("step must be positive")
    analytic = analytic_gradient(weight, x, target)
    checks = []
    for h in (step * 100, step * 10, step, step / 10, step / 100):
        numeric = central_difference(weight, x, target, h)
        checks.append({"step": h, "analytic": analytic, "central_difference": numeric, "relative_error": relative_error(analytic, numeric)})
    best = min(checks, key=lambda row: row["relative_error"])
    extreme = []
    for w in (-1000.0, 1000.0):
        extreme.append({"weight": w, "loss": loss(w, x, target), "gradient": analytic_gradient(w, x, target), "finite": math.isfinite(loss(w, x, target))})
    return {
        "exercise": "finite-difference",
        "question": "Does the analytic gradient of scalar logistic cross-entropy match a central finite difference at this point?",
        "assumptions": ["binary target", "scalar weight/input", "fixed bias=-0.2", "evaluation point is smooth", "double-precision Python float"],
        "notation_and_shapes": {"weight": "scalar", "x": "scalar", "target": "{0,1}", "logit": "weight*x+bias"},
        "equation_steps": ["L=max(z,0)-y*z+log(1+exp(-abs(z)))", "dL/dz=sigmoid(z)-y", "dL/dw=(sigmoid(z)-y)*x"],
        "configuration": {"weight": weight, "x": x, "target": target, "requested_step": step},
        "environment": {"python": sys.version.split()[0], "platform": platform.platform(), "dependencies": "standard library only"},
        "numerical_checks": checks,
        "best_check": best,
        "status": "consistent_at_tested_point" if best["relative_error"] < 1e-7 else "investigate",
        "extreme_cases": extreme,
        "error_analysis": {
            "if_large_error": ["analytic chain-rule error", "wrong target/sign", "step too large: truncation", "step too small: cancellation", "non-smooth or unstable expression"],
            "scope": "A local scalar check does not validate tensor broadcasting, the objective, data, optimization, or generalization.",
        },
        "artifact_path": "this JSON output",
        "optimization_prediction": "For positive x and target=1, a negative gradient makes gradient descent increase weight at this point.",
        "generalization_failure": "The data distribution and model specification are not tested by this derivative check.",
        "next_experiment": "Implement a two-feature vector version and assert every intermediate shape before comparing gradients.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exercise", choices=("finite-difference",), default="finite-difference")
    parser.add_argument("--x", type=float, default=0.7)
    parser.add_argument("--target", type=int, choices=(0, 1), default=1)
    parser.add_argument("--step", type=float, default=1e-5)
    parser.add_argument("--weight", type=float, default=0.4)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        data = run(args.x, args.target, args.step, args.weight)
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
