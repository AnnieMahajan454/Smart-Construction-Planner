from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


@dataclass
class TrainedModel:
    estimator: RandomForestRegressor
    feature_names: Tuple[str, ...]


def train_demand_predictor(features: pd.DataFrame) -> Tuple[TrainedModel, Dict[str, float]]:
    """Train a baseline demand predictor using RandomForest.

    Target column: `target_demand_next_hour`.
    Returns trained model and metrics.
    """
    target_col = "target_demand_next_hour"
    X = features.drop(columns=[target_col])
    y = features[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(random_state=42, n_estimators=300, max_depth=None, n_jobs=-1)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "mae": float(mean_absolute_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds)),
    }
    return TrainedModel(model, tuple(X.columns)), metrics


def predict_demand(trained: TrainedModel, X: pd.DataFrame) -> np.ndarray:
    """Run inference using the trained model, aligning feature columns."""
    X = X.reindex(columns=list(trained.feature_names), fill_value=0)
    return trained.estimator.predict(X)


