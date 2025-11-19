# openai_agent.py
from typing import Dict, Optional
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL


def build_openai_client() -> Optional[OpenAI]:
    """
    Crée un client OpenAI si la clé est disponible.
    """
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)


SYSTEM_PROMPT = """
Tu es un assistant d'analyse de données cardiaques dans un prototype de recherche.
Tu reçois des métriques résumées provenant d'un Holter (fréquence cardiaque en bpm).

RÔLE :
- Expliquer en français simple ce que signifient ces métriques.
- Classer le profil dans une catégorie parmi : "NORMAL", "À SURVEILLER", "RISQUE ÉLEVÉ".
- Proposer une recommandation très générale (surveillance, consultation médicale, urgence).
- Toujours rappeler clairement que :
    - Ceci est un PROTOTYPE technique.
    - Ce n'est PAS un dispositif médical.
    - Ce n'est PAS un avis médical.
    - L'utilisateur doit consulter un professionnel de santé pour toute décision.

CONTRAINTES :
- Ne donner aucun diagnostic.
- Ne citer aucun traitement.
- Parler en français seulement.
"""

def analyze_with_openai(metrics: Dict[str, float]) -> str:
    """
    Envoie les métriques à OpenAI pour obtenir une analyse et une recommandation.

    Retourne du texte en français.
    """
    client = build_openai_client()
    if client is None:
        return (
            "⚠️ Analyse OpenAI impossible : aucune clé API trouvée.\n"
            "Installe une clé dans OPENAI_API_KEY pour activer l'analyse."
        )

    user_prompt = (
        "Voici les métriques extraites du Holter :\n"
        f"{metrics}\n\n"
        "Analyse ces données selon les directives du système."
    )

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return completion.choices[0].message.content
