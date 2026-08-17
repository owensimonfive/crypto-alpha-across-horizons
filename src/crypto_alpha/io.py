"""Repository-path and frozen-artifact loading helpers."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


def locate_repo_root(start: str | Path | None = None) -> Path:
    """Locate the public repository root.

    CRYPTO_ALPHA_PUBLIC_ROOT takes precedence when set.
    """
    env_root = os.getenv("CRYPTO_ALPHA_PUBLIC_ROOT")
    if env_root:
        candidate = Path(env_root).expanduser().resolve()
        if (candidate / "pyproject.toml").exists():
            return candidate

    current = Path(start or Path.cwd()).expanduser().resolve()
    candidates = [current, *current.parents]
    for candidate in candidates:
        if (
            (candidate / "pyproject.toml").exists()
            and (candidate / "notebooks").is_dir()
            and (candidate / "results" / "tables").is_dir()
        ):
            return candidate

    raise FileNotFoundError(
        "Could not locate public repo root. Set CRYPTO_ALPHA_PUBLIC_ROOT."
    )


def load_public_universe(repo_root: str | Path) -> pd.DataFrame:
    path = Path(repo_root) / "data" / "universe" / "monthly_universe.csv"
    frame = pd.read_csv(path)
    frame["effective_month"] = pd.to_datetime(
        frame["effective_month"], utc=True
    )
    return frame


def load_frozen_finalists(repo_root: str | Path) -> pd.DataFrame:
    path = Path(repo_root) / "results" / "tables" / "frozen_finalists.csv"
    return pd.read_csv(path)


def load_final_holdout_metrics(repo_root: str | Path) -> pd.DataFrame:
    path = Path(repo_root) / "results" / "tables" / "final_holdout_metrics.csv"
    return pd.read_csv(path)
