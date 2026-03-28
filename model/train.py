import json
import logging
import os
import sys
import time

import numpy as np
from pythonjsonlogger import jsonlogger
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
LOG_FILE = os.path.join(os.path.dirname(__file__), "training.log")

logger = logging.getLogger("lr_training")
logger.setLevel(logging.INFO)

# File handler — JSON format for Logstash
file_handler = logging.FileHandler(LOG_FILE)
file_formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
file_handler.setFormatter(file_formatter)

# Console handler — human-readable
console_handler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter(
    "%(asctime)s  %(levelname)-8s  %(message)s", datefmt="%H:%M:%S"
)
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# ---------------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------------
def generate_data(n_samples: int = 500, noise: float = 5.0, seed: int = 42):
    """Generate synthetic single-feature linear data."""
    rng = np.random.default_rng(seed)
    X = rng.uniform(0, 100, size=(n_samples, 1))
    y = 2.8 * X.squeeze() + 15.0 + rng.normal(0, noise, size=n_samples)
    return X, y


# ---------------------------------------------------------------------------
# Training pipeline
# ---------------------------------------------------------------------------
def train():
    logger.info("Pipeline started", extra={"stage": "init"})

    # --- Data ---
    X, y = generate_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    logger.info(
        "Data split complete",
        extra={
            "stage": "data",
            "n_total": len(X),
            "n_train": len(X_train),
            "n_test": len(X_test),
        },
    )

    # --- Preprocessing ---
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    logger.info(
        "Scaling complete",
        extra={
            "stage": "preprocessing",
            "scaler_mean": round(float(scaler.mean_[0]), 4),
            "scaler_std": round(float(scaler.scale_[0]), 4),
        },
    )

    # --- Training ---
    t0 = time.perf_counter()
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    duration_ms = round((time.perf_counter() - t0) * 1000, 2)

    logger.info(
        "Model training complete",
        extra={
            "stage": "training",
            "duration_ms": duration_ms,
            "coefficients": [round(c, 6) for c in model.coef_.tolist()],
            "intercept": round(float(model.intercept_), 6),
        },
    )

    # --- Evaluation ---
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    logger.info(
        "Evaluation complete",
        extra={
            "stage": "evaluation",
            "r2_score": round(r2, 6),
            "mse": round(mse, 6),
            "rmse": round(rmse, 6),
            "n_test_samples": len(y_test),
        },
    )

    if r2 < 0.80:
        logger.warning(
            "R² below threshold",
            extra={"stage": "evaluation", "r2_score": round(r2, 6), "threshold": 0.80},
        )

    logger.info("Pipeline finished", extra={"stage": "done"})
    print(f"\n  R²   = {r2:.4f}")
    print(f"  RMSE = {rmse:.4f}")
    print(f"  Log  → {LOG_FILE}\n")


if __name__ == "__main__":
    train()
