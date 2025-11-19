# holter_loader.py
import pandas as pd


POSSIBLE_HR_COLUMNS = ["heart_rate", "hr", "bpm", "HeartRate", "HR"]


class HolterDataError(Exception):
    pass


def load_holter_csv(path: str) -> pd.DataFrame:
    """
    Charge un fichier CSV de données Holter.

    On s'attend à trouver une colonne de fréquence cardiaque (bpm).
    Noms possibles : heart_rate, hr, bpm, etc.
    """
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise HolterDataError(f"Impossible de lire le fichier CSV : {e}")

    if df.empty:
        raise HolterDataError("Le fichier CSV est vide.")

    hr_col = None
    for col in POSSIBLE_HR_COLUMNS:
        if col in df.columns:
            hr_col = col
            break

    if hr_col is None:
        raise HolterDataError(
            f"Aucune colonne de fréquence cardiaque trouvée. "
            f"Colonnes attendues : {POSSIBLE_HR_COLUMNS}. Colonnes présentes : {list(df.columns)}"
        )

    # On conserve aussi les autres colonnes (timestamp, etc.) si elles existent
    df = df.copy()
    df.rename(columns={hr_col: "heart_rate_bpm"}, inplace=True)

    return df
