import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Chargement de la clé secrète
load_dotenv()

# 2. Initialisation de l'agent
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

print("--- Agent CardiAc : Démarrage ---")

# 3. Le Cerveau (Prompt Système)
instruction_systeme = """
Tu es CardiAc, un assistant IA expert en cardiologie.
Ton rôle est d'analyser les descriptions de symptômes ou d'ECG.
Si tu détectes une urgence vitale, commence ta réponse par "ALERTE ROUGE".
Sinon, donne une analyse rassurante.
Ajoute toujours un avertissement que tu es une IA.
"""

# 4. Simulation (Input)
symptomes_patient = "Douleur thoracique irradiant dans le bras gauche, sueurs froides."

print(f"Analyse du cas : {symptomes_patient}")

# 5. Appel à l'IA
response = client.chat.completions.create(
    model="gpt-5.1",
    messages=[
        {"role": "system", "content": instruction_systeme},
        {"role": "user", "content": symptomes_patient}
    ]
)
