"""
Streamlit frontend for CardIAc
Fichier: CardIAc_streamlit_app.py
Usage:
    pip install -r requirements.txt
    streamlit run CardIAc_streamlit_app.py

Requirements (suggested):
    streamlit
    pandas
    matplotlib
    requests
    pillow

This frontend expects an API endpoint to analyze ECG files/images (configurable via CARDIAC_API_URL env var).
If none provided, the app will mock responses for local testing.
"""

import os
import io
import json
import base64
from typing import Optional

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import requests

# ----------------------
# Configuration
# ----------------------
API_URL = os.environ.get("CARDIAC_API_URL", "http://localhost:8000/analyze")
MOCK_MODE = os.environ.get("CARDIAC_MOCK", "1") == "1"

# ----------------------
# Helpers
# ----------------------

def call_analysis_api(file_bytes: bytes, filename: str, filetype: str) -> dict:
    """
    Send file to backend API and return parsed JSON response.
    The backend is expected to return JSON with at least:
      {"diagnosis": "Normal / Abnormal / Critical", "probability": 0.92, "details": {...}}
    """
    if MOCK_MODE:
        # Return a mocked response for development
        return {
            "diagnosis": "Normal",
            "probability": 0.03,
            "severity": "low",
            "message": "Aucun signe d'anomalie critique détecté.",
            "standards_comparison": {
                "heart_rate": {"value": 72, "reference": "60-100 BPM"},
                "qrs_duration_ms": {"value": 90, "reference": "<120 ms"}
            }
        }

    files = {"file": (filename, io.BytesIO(file_bytes), filetype)}
    try:
        resp = requests.post(API_URL, files=files, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def plot_ecg_from_csv(df: pd.DataFrame):
    """Plot ECG timeseries stored in pandas DataFrame.
    We expect either a single column or multiple leads as columns.
    """
    st.write("### Aperçu du tracé ECG")
    plt.figure(figsize=(10, 3))
    # If index is not numeric, create a sample x axis
    if df.shape[1] == 1:
        y = df.iloc[:, 0].values
        x = range(len(y))
        plt.plot(x, y)
        plt.ylabel("Amplitude")
        plt.xlabel("Échantillon")
    else:
        # Plot first 3 leads max for preview
        for i, col in enumerate(df.columns[:3]):
            plt.plot(df.index, df[col], label=str(col))
        plt.legend(loc="upper right")
    plt.tight_layout()
    st.pyplot(plt)


# ----------------------
# UI
# ----------------------

st.set_page_config(page_title="CardIAc — Analyse d'ECG", layout="wide")

# Header
col1, col2 = st.columns([0.18, 0.82])
with col1:
    st.image("https://raw.githubusercontent.com/your-org/CardIAc/main/logo.png" if not MOCK_MODE else "https://picsum.photos/120/120", width=100)
with col2:
    st.title("CardIAc — Assistant IA pour l'analyse d'ECG")
    st.caption("Analyse instantanée d'ECG, comparaison aux standards et déclenchement d'alerte en cas d'anomalie critique")

st.markdown("---")

# Sidebar settings
with st.sidebar:
    st.header("Paramètres")
    st.write(f"API endpoint: `{API_URL}`")
    if st.button("Basculer mock/dev mode"):
        st.warning("Pour changer le mode, modifiez la variable d'environnement CARDIAC_MOCK avant de lancer l'app.")
    st.write("\n")
    st.caption("Format attendu côté serveur : image (jpg/png) ou fichier CSV/TSV contenant les échantillons ECG")


# Main interaction area
st.subheader("1) Importer un ECG")
col_up1, col_up2 = st.columns(2)
with col_up1:
    img_file = st.file_uploader("Télécharger une image d'ECG (jpg/png)", type=["png", "jpg", "jpeg"], key="img_uploader")
    if img_file:
        try:
            image = Image.open(img_file).convert("RGB")
            st.image(image, caption="ECG importé — aperçu", use_column_width=True)
        except Exception as e:
            st.error(f"Impossible d'ouvrir l'image: {e}")

with col_up2:
    data_file = st.file_uploader("Ou télécharger un fichier de données (CSV/TSV) contenant l'ECG)", type=["csv", "tsv", "txt"], key="data_uploader")
    if data_file:
        try:
            # detect delimiter
            raw = data_file.read()
            sample = raw[:4096].decode(errors="ignore")
            sep = "," if "," in sample else "\t"
            df = pd.read_csv(io.BytesIO(raw), sep=sep)
            st.write(df.head())
            plot_ecg_from_csv(df)
        except Exception as e:
            st.error(f"Impossible de lire le fichier de données: {e}")

st.markdown("---")

st.subheader("2) Lancer l'analyse")
cols = st.columns([1, 1, 1])
with cols[0]:
    run_btn = st.button("Analyser maintenant")
with cols[1]:
    priority = st.selectbox("Niveau d'urgence simulé (pour tests)", options=["auto", "low", "medium", "high"], index=0)
with cols[2]:
    add_notes = st.text_input("Notes patient / Contexte (optionnel)")

if run_btn:
    with st.spinner("Analyse en cours — envoi au modèle IA..."):
        # Prepare payload
        file_bytes = None
        filename = ""
        filetype = ""
        if img_file:
            file_bytes = img_file.read()
            filename = getattr(img_file, "name", "ecg_upload.jpg")
            filetype = "image/jpeg"
        elif data_file:
            # rebuild bytes from df to send raw
            data_file.seek(0)
            file_bytes = data_file.read()
            filename = getattr(data_file, "name", "ecg_upload.csv")
            filetype = "text/csv"
        else:
            st.error("Aucun fichier ECG fourni. Téléchargez une image ou un fichier de données.")
            st.stop()

        result = call_analysis_api(file_bytes, filename, filetype)

    if result.get("error"):
        st.error(f"Erreur lors de l'appel à l'API: {result['error']}")
    else:
        # Show results
        st.success("Analyse terminée")
        diag = result.get("diagnosis", "Inconnu")
        prob = result.get("probability", None)
        severity = result.get("severity", "unknown")
        message = result.get("message", "")

        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.metric("Diagnostic", diag, delta=f"Probabilité: {prob}" if prob is not None else "")
            st.write(f"**Sévérité**: {severity}")
            if message:
                st.info(message)

            st.write("\n")
            if severity in ["high", "critical"] or (prob is not None and prob > 0.8):
                st.error("Anomalie critique détectée — préparation d'une alerte pour les urgences.")
                if st.button("Préparer Alerte d'urgence"):
                    # This is a placeholder for an actual alerting flow
                    st.write("Alerte préparée — envoyée au service d'urgence (simulation).")
            else:
                st.success("Aucune anomalie critique détectée. Conseils: rester calme, consulter votre médecin si symptômes persistent.")

        with col_b:
            st.write("### Détails & comparaison aux standards")
            sc = result.get("standards_comparison", {})
            if sc:
                st.json(sc)
            else:
                st.write("Pas de données standards fournies par l'API.")

        # raw debug
        if st.checkbox("Afficher la réponse brute (debug)"):
            st.json(result)

st.markdown("---")

st.subheader("3) Guides et installation")
st.markdown(
    """
- Cloner le dépôt.
- Installer les dépendances : `pip install -r requirements.txt`
- Configurer la clé API / endpoint via les variables d'environnement `CARDIAC_API_URL` et `CARDIAC_MOCK`.
- Lancer le backend (ex: `python main.py`) puis lancer cette interface :

```bash
streamlit run CardIAc_streamlit_app.py
```

"""
)

st.caption("CardIAc — outil d'aide à la décision. Ne remplace pas un diagnostic médical professionnel.")

# Footer with quick links
st.markdown("---")
links_col1, links_col2 = st.columns(2)
with links_col1:
    st.write("**Architecture**: Python + OpenAI GPT-4o (backend)")
with links_col2:
    st.write("Sécurité: gérez vos clés via .env / variables d'environnement")


if __name__ == '__main__':
    pass
