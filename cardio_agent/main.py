# main.py
import argparse
from textwrap import dedent

from holter_loader import load_holter_csv, HolterDataError
from analysis import compute_heart_metrics
from openai_agent import analyze_with_openai
from config import ensure_api_key


def parse_args():
    parser = argparse.ArgumentParser(
        description="Prototype d'agent d'analyse de données Holter cardiaques."
    )
    parser.add_argument("csv_path", help="Chemin vers le fichier CSV Holter.")
    return parser.parse_args()


def main():
    print(
        dedent(
            """
            🩺  Agent d'analyse Holter (prototype)
            ------------------------------------
            ⚠️ Ceci est un démonstrateur technique.
            ⚠️ Ce n'est PAS un dispositif médical.
            ⚠️ Il ne fournit PAS d'avis médical ni de diagnostic.
            """
        )
    )

    args = parse_args()

    # Vérification de la clé OpenAI
    ensure_api_key()

    # Chargement du CSV
    try:
        df = load_holter_csv(args.csv_path)
    except HolterDataError as e:
        print(f"❌ Erreur : {e}")
        return

    print("📄 Données Holter chargées.")

    # Calcul des métriques
    metrics = compute_heart_metrics(df)
    print("\n📊 Métriques extraites :")
    for k, v in metrics.items():
        print(f"  - {k}: {v}")

    print("\n📡 Envoi à OpenAI pour analyse...\n")

    # Analyse via GPT
    text = analyze_with_openai(metrics)

    print("===== RÉSULTAT =====\n")
    print(text)
    print("\n=====================")


if __name__ == "__main__":
    main()
