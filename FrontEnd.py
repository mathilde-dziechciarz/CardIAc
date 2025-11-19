"""
CardIAc Streamlit frontend
Fichier: CardIAc_streamlit_frontend.py
But: Ce fichier est une base complète pour l'interface Streamlit de l'application CardIAc.
Il contient :
- upload d'ECG (image ou CSV/JSON de signal)
- affichage rapide (image + signal plot)
- placeholder pour chargement du modèle IA et de la fonction de prédiction
- affichage des probabilités de diagnostic et explications simples
- options côté utilisateur (seuils, modèle, export du rapport)

A adapter : implémenter `load_model()` et `predict_ecg()` pour connecter votre modèle réel.
"""

from typing import Dict, Any, Tuple
import io
import json
import base64
import tempfile
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ---------------------------
# Configuration de la page
# ---------------------------
st.set_page_config(page_title="CardIAc — Analyse d'ECG par IA", layout="wide")

# ---------------------------
# Fonctions utilitaires (à remplacer/adapter)
# ---------------------------
@st.cache_data
def load_model(model_name: str = "cardiac-net-v1") -> Any:
    """Chargement du modèle IA (placeholder).
    Remplacez cette fonction pour charger votre modèle (torch/onnx/tf...) et renvoyer un objet utilisable par predict_ecg.
    """
    # TODO: implémenter le chargement réel
    # Exemple:
    # import torch
    # model = torch.load(path)
    # model.eval()
    class DummyModel:
        def predict(self, x: np.ndarray) -> Dict[str, float]:
            # Retourne un diagnostic factice
            return {
                "Rythme sinusal normal": 0.73,
                "Fibrillation auriculaire": 0.12,
                "Hypertrophie ventriculaire": 0.08,
                "Bloc de branche": 0.05,
                "Autre": 0.02,
            }
    return DummyModel()


def read_signal_from_csv(file: io.BytesIO) -> pd.DataFrame:
    """Lit un CSV d'ECG. On suppose que chaque colonne est un canal ou que le fichier contient 'time'+'v'"""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        raise


def preprocess_signal(df: pd.DataFrame) -> np.ndarray:
    """Preprocessing minimal : retourner un tableau numpy (1D ou 2D) utilisable par le modèle."""
    # TODO: appliquer bandpass, normalisation, resampling, segmentation, etc.
    if "amplitude" in df.columns:
        arr = df["amplitude"].to_numpy()
    else:
        # si plusieurs colonnes, prendre la première numérique non-time
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        arr = df[numeric_cols[0]].to_numpy()
    return arr


def predict_ecg(model: Any, signal: np.ndarray) -> Dict[str, float]:
    """Fonction d'inférence. Adapter selon l'API de votre modèle.
    Doit renvoyer un dictionnaire {diagnostic: probability}
    """
    # Placeholder : utiliser model.predict si disponible
    if hasattr(model, "predict"):
        return model.predict(signal)
    # sinon renvoyer un exemple
    return {
        "Rythme sinusal normal": 0.60,
        "Fibrillation auriculaire": 0.25,
        "Hypertrophie ventriculaire": 0.10,
        "Bloc de branche": 0.03,
        "Autre": 0.02,
    }


def make_report(patient_name: str, age: str, uploaded_filename: str, prediction: Dict[str, float]) -> str:
    """Génère un rapport texte simple"""
    lines = []
    lines.append("CardIAc — Rapport d'analyse ECG")
    lines.append("===============================")
    lines.append(f"Patient: {patient_name}")
    lines.append(f"Âge: {age}")
    lines.append(f"Fichier analysé: {uploaded_filename}")
    lines.append("")
    lines.append("Probabilités (ordre décroissant) :")
    for k, v in sorted(prediction.items(), key=lambda x: x[1], reverse=True):
        lines.append(f" - {k}: {v*100:.1f}%")
    lines.append("")
    lines.append("Remarques : Ceci est une estimation fournie par un modèle d'IA. Ne remplace pas un avis médical. En cas de doute, consultez un professionnel de santé.")
    return "\n".join(lines)

# ---------------------------
# UI - Barre latérale
# ---------------------------
st.sidebar.title("Paramètres")
model_choice = st.sidebar.selectbox("Modèle IA", ["cardiac-net-v1", "cardiac-net-v2 (expérimental)"], index=0)
confidence_threshold = st.sidebar.slider("Seuil d'alerte (probabilité)", 0.0, 1.0, 0.2)
show_explainability = st.sidebar.checkbox("Afficher explication (saliency / heatmap)", value=True)

# Load model
with st.sidebar.expander("Chargement du modèle"):
    st.write(f"Chargement du modèle: {model_choice}")
    model = load_model(model_choice)
    st.success("Modèle chargé (placeholder)")

# ---------------------------
# UI - Corps principal
# ---------------------------
st.title("CardIAc — Analyse d'ECG par IA")
st.write("Téléversez un ECG (image ou CSV) ; l'IA vous donnera une probabilité de diagnostics possibles.")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Téléversement")
    uploaded_file = st.file_uploader("Choisir un fichier ECG (PNG/JPG, CSV)", type=["png", "jpg", "jpeg", "csv", "json"], accept_multiple_files=False)
    patient_name = st.text_input("Nom du patient", value="Anonyme")
    patient_age = st.text_input("Âge", value="?")
    analyze_button = st.button("Analyser")

    st.markdown("---")
    st.subheader("Options d'export")
    report_format = st.radio("Format de rapport", ("Texte (.txt)", "JSON (.json)"))

with col2:
    st.header("Visualisation")
    placeholder_vis = st.empty()

# ---------------------------
# Traitement à l'appui du bouton
# ---------------------------
if analyze_button and uploaded_file is not None:
    fname = uploaded_file.name
    file_bytes = uploaded_file.read()

    # Cas CSV / JSON (signal) ou image
    is_image = fname.lower().endswith((".png", ".jpg", ".jpeg"))
    is_csv = fname.lower().endswith(".csv") or fname.lower().endswith(".json")

    if is_image:
        # afficher l'image
        from PIL import Image
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        with placeholder_vis.container():
            st.image(image, caption=f"{fname}", use_column_width=True)
            st.write("Image détectée — tentative d'extraction non implémentée. Si vous disposez du signal natif, préférez le CSV/JSON.")

        # pour l'instant, on ne peut pas inférer depuis l'image (placeholder)
        st.warning("Prédiction depuis image non implémentée dans cet exemple. Convertissez l'ECG en CSV de signaux pour une vraie analyse.")
        prediction = predict_ecg(model, np.zeros(500))

    elif is_csv:
        # lire signal
        try:
            if fname.lower().endswith(".csv"):
                df = read_signal_from_csv(io.BytesIO(file_bytes))
            else:
                # JSON expected
                data = json.loads(file_bytes.decode("utf-8"))
                df = pd.DataFrame(data)

            # afficher preview
            with placeholder_vis.container():
                st.subheader("Aperçu du signal")
                st.dataframe(df.head(100))

                arr = preprocess_signal(df)
                fig, ax = plt.subplots(figsize=(8, 3))
                ax.plot(arr)
                ax.set_title("ECG — signal prétraité (aperçu)")
                ax.set_xlabel("Échantillon")
                ax.set_ylabel("Amplitude")
                st.pyplot(fig)

            # prédiction
            prediction = predict_ecg(model, arr)
        except Exception as e:
            st.error(f"Impossible de lire le fichier de signal: {e}")
            prediction = {}
    else:
        st.error("Format de fichier non supporté dans cet exemple.")
        prediction = {}

    # Afficher résultats
    if prediction:
        st.markdown("---")
        st.subheader("Résultats de l'IA")
        # trier et afficher
        items = sorted(prediction.items(), key=lambda x: x[1], reverse=True)
        labels = [k for k, v in items]
        probs = [v for k, v in items]

        # Bar chart matplotlib
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        y_pos = np.arange(len(labels))
        ax2.barh(y_pos, probs)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(labels)
        ax2.invert_yaxis()
        ax2.set_xlabel("Probabilité")
        ax2.set_xlim(0, 1)
        st.pyplot(fig2)

        # Top suggestion
        top_label, top_prob = items[0]
        st.metric(label="Diagnostic le plus probable", value=f"{top_label}", delta=f"{top_prob*100:.1f}%")

        # Alerte si au-dessus du seuil
        if top_prob >= confidence_threshold:
            st.success(f"Le modèle est confiant : {top_label} ({top_prob*100:.1f}%)")
        else:
            st.info("Aucune prédiction très confiante — veuillez interpréter prudemment.")

        # Explainability placeholder
        if show_explainability:
            st.subheader("Explication (placeholder)")
            st.write("Ici on afficherait une carte de 'saliency' ou d'attention montrant quelles parties du signal ont le plus contribué à la prédiction.")
            st.write("(Non implémenté — à remplacer par Integrated Gradients / GradCAM adapté au modèle.)")

        # Générer et proposer le rapport en download
        report_text = make_report(patient_name, patient_age, fname, prediction)
        if report_format.startswith("Texte"):
            b = report_text.encode("utf-8")
            st.download_button(label="Télécharger le rapport (.txt)", data=b, file_name=f"rapport_{fname}.txt", mime="text/plain")
        else:
            # JSON
            b = json.dumps({"patient": patient_name, "age": patient_age, "file": fname, "prediction": prediction}, ensure_ascii=False, indent=2).encode("utf-8")
            st.download_button(label="Télécharger le rapport (.json)", data=b, file_name=f"rapport_{fname}.json", mime="application/json")

    else:
        st.warning("Aucun résultat disponible.")

elif not analyze_button:
    with placeholder_vis.container():
        st.info("Importez un ECG (CSV/JSON idéalement) puis cliquez sur 'Analyser' pour lancer l'IA.")

# ---------------------------
# Footer / Avertissement légal
# ---------------------------
st.markdown("---")
st.caption("CardIAc — prototype d'aide à la décision. Ne remplace pas l'avis médical professionnel. Pour usage clinique, respecter la réglementation locale (CE/510k/ANSM/etc.) et effectuer une validation clinique.")

# EOF
