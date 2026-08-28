"""A self-contained grouped-validation demo for mechanical fault diagnosis.

The data are synthetic and are intended for workflow practice, not for proving
real-world diagnostic performance.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    f1_score,
)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


SEED = 42
FS_HZ = 2_000
DURATION_S = 2.0
LABELS = np.array(["normal", "unbalance", "misalignment"])
FEATURE_NAMES = np.array(
    ["rms", "peak_to_peak", "crest_factor", "kurtosis", "band_1x", "band_2x"]
)


def simulate_window(
    label: str,
    speed_hz: float,
    run_signature: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Generate one acceleration window in m/s²."""
    time_s = np.arange(0, DURATION_S, 1 / FS_HZ)
    phase = rng.uniform(0, 2 * np.pi)
    amplitudes = {
        "normal": (0.35, 0.08, 0.06),
        "unbalance": (1.10, 0.12, 0.09),
        "misalignment": (0.65, 0.85, 0.12),
    }
    amp_1x, amp_2x, noise_std = amplitudes[label]

    signal = (
        amp_1x * np.sin(2 * np.pi * speed_hz * time_s + phase)
        + amp_2x * np.sin(2 * np.pi * 2 * speed_hz * time_s + 0.4 * phase)
        + run_signature * np.sin(2 * np.pi * 11 * time_s)
        + noise_std * rng.normal(size=time_s.size)
    )
    if label == "misalignment":
        impulse_locations = rng.choice(time_s.size, size=8, replace=False)
        signal[impulse_locations] += rng.normal(0.9, 0.12, size=impulse_locations.size)
    return signal


def band_energy(signal: np.ndarray, center_hz: float, half_width_hz: float = 2.0) -> float:
    """Return normalized spectral energy near a physical frequency."""
    centered = signal - signal.mean()
    window = np.hanning(centered.size)
    spectrum = np.fft.rfft(centered * window)
    frequency_hz = np.fft.rfftfreq(centered.size, d=1 / FS_HZ)
    power = np.abs(spectrum) ** 2
    selected = np.abs(frequency_hz - center_hz) <= half_width_hz
    return float(power[selected].sum() / (power.sum() + np.finfo(float).eps))


def extract_features(signal: np.ndarray, speed_hz: float) -> np.ndarray:
    """Extract six small, physically interpretable features."""
    centered = signal - signal.mean()
    rms = np.sqrt(np.mean(centered**2))
    standard_deviation = centered.std()
    kurtosis = np.mean((centered / (standard_deviation + np.finfo(float).eps)) ** 4)
    return np.array(
        [
            rms,
            np.ptp(centered),
            np.max(np.abs(centered)) / (rms + np.finfo(float).eps),
            kurtosis,
            band_energy(centered, speed_hz),
            band_energy(centered, 2 * speed_hz),
        ]
    )


def make_dataset() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create windows while retaining independent run IDs for splitting."""
    rng = np.random.default_rng(SEED)
    rows: list[np.ndarray] = []
    targets: list[str] = []
    groups: list[str] = []

    for label in LABELS:
        for run_number in range(12):
            speed_hz = rng.uniform(23.0, 27.0)
            run_signature = rng.uniform(0.01, 0.07)
            run_id = f"{label}-run-{run_number:02d}"
            for _ in range(8):
                signal = simulate_window(label, speed_hz, run_signature, rng)
                rows.append(extract_features(signal, speed_hz))
                targets.append(label)
                groups.append(run_id)
    return np.vstack(rows), np.array(targets), np.array(groups)


def grouped_split(
    X: np.ndarray, y: np.ndarray, groups: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Create a stratified split while keeping every run on only one side."""
    splitter = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=SEED)
    train_idx, test_idx = next(splitter.split(X, y, groups))
    assert set(groups[train_idx]).isdisjoint(groups[test_idx])
    assert set(y[train_idx]) == set(LABELS) == set(y[test_idx])
    return train_idx, test_idx


def save_feature_plot(X: np.ndarray, y: np.ndarray, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    for label in LABELS:
        selected = y == label
        ax.scatter(X[selected, 4], X[selected, 5], s=18, alpha=0.65, label=label)
    ax.set(
        xlabel="Normalized energy near 1x speed",
        ylabel="Normalized energy near 2x speed",
        title="Physical feature space (synthetic data)",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "feature_space.png", dpi=180)
    plt.close(fig)


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    X, y, groups = make_dataset()
    train_idx, test_idx = grouped_split(X, y, groups)

    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    models = {
        "logistic_regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=2_000, random_state=SEED),
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=SEED,
            n_jobs=-1,
        ),
    }

    metric_rows = []
    predictions = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        prediction = model.predict(X_test)
        predictions[name] = prediction
        metric_rows.append(
            {
                "model": name,
                "accuracy": accuracy_score(y_test, prediction),
                "macro_f1": f1_score(y_test, prediction, average="macro"),
                "train_runs": np.unique(groups[train_idx]).size,
                "test_runs": np.unique(groups[test_idx]).size,
            }
        )
        print(f"\n{name}\n{'-' * len(name)}")
        print(classification_report(y_test, prediction, digits=3))

    with (output_dir / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=metric_rows[0].keys())
        writer.writeheader()
        writer.writerows(metric_rows)

    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(
        y_test,
        predictions["random_forest"],
        labels=LABELS,
        normalize="true",
        cmap="Blues",
        values_format=".2f",
        ax=ax,
    )
    ax.set_title("Random forest · grouped test runs")
    fig.tight_layout()
    fig.savefig(output_dir / "confusion_matrix.png", dpi=180)
    plt.close(fig)

    save_feature_plot(X, y, output_dir)
    print(f"Features: {', '.join(FEATURE_NAMES)}")
    print(f"Saved results to: {output_dir}")


if __name__ == "__main__":
    main()
