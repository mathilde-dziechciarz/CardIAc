# analysis.py
import numpy as np
import pandas as pd
from typing import Dict


def compute_heart_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calcule des métriques simples à partir des données Holter.

    Ces métriques seront envoyées au modèle OpenAI pour interprétation.
    """
    hr = df["heart_rate_bpm"].astype(float).to_numpy()

    mean_hr = float(np.mean(hr))
    min_hr = float(np.min(hr))
    max_hr = float(np.max(hr))
    std_hr = float(np.std(hr))

    n = len(hr)
    if n == 0:
        raise ValueError("Aucune donnée de fréquence cardiaque disponible.")

    pct_above_100 = float(np.sum(hr > 100) / n * 100.0)
    pct_above_120 = float(np.sum(hr > 120) / n * 100.0)
    pct_below_50 = float(np.sum(hr < 50) / n * 100.0)

    metrics = {
        "mean_hr": round(mean_hr, 1),
        "min_hr": round(min_hr, 1),
        "max_hr": round(max_hr, 1),
        "std_hr": round(std_hr, 1),
        "pct_above_100": round(pct_above_100, 1),
        "pct_above_120": round(pct_above_120, 1),
        "pct_below_50": round(pct_below_50, 1),
        "num_samples": int(n),
    }

    return metrics
