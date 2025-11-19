# config.py
import os
import sys


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def ensure_api_key():
    """
    Vérifie que la clé OpenAI est bien définie.
    Si non, affiche un message clair et propose la commande à exécuter.
    """
    if not OPENAI_API_KEY:
        msg = (
            "❌ Aucune clé OpenAI détectée.\n\n"
            "Pour utiliser l'analyse intelligente, définis la variable d'environnement OPENAI_API_KEY.\n"
            "Exemples :\n"
            "  - Linux / macOS : export OPENAI_API_KEY=\"ta_cle_ici\"\n"
            "  - Windows (PowerShell) : setx OPENAI_API_KEY \"ta_cle_ici\"\n\n"
            "Tu peux toutefois lancer le programme : il affichera seulement l'analyse statistique locale."
        )
        print(msg, file=sys.stderr)
        return False
    return True
