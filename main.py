import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

# 1. Chargement de la clé
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2. Fonction encodage image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Nom de l'image (Vérifie bien que c'est le bon nom !)
image_path = "ECG_1.png"

try:
    if not os.path.exists(image_path):
        print(f"❌ ERREUR : L'image '{image_path}' est introuvable.")
    else:
        print(f"Lecture de l'image : {image_path}...")
        base64_image = encode_image(image_path)

        # --- C'EST ICI QUE TOUT CHANGE ---
        # Prompt structuré selon la méthode médicale standard
        instruction_systeme = """
        Tu es CardiAc, un assistant IA expert en interprétation d'électrocardiogrammes (ECG).

        TA MISSION :
        Analyse l'image fournie en suivant scrupuleusement cette grille de lecture clinique :

        1. FRÉQUENCE & RYTHME :
           - Estimation de la fréquence (BPM)
           - Le rythme est-il régulier ?
           - Présence d'ondes P ? (Rythme sinusal)
        
        2. ANALYSE DES ONDES :
           - Complexe QRS : Fin (<0.12s) ou Large ?
           - Segment ST : Recherche spécifique de SUS-DÉCALAGE (Signe d'infarctus) ou sous-décalage.
           - Onde T : Normale, inversée ou ample ?
        
        3. SYNTHÈSE :
           - Résume les anomalies trouvées.
        
        4. DÉCISION (OBLIGATOIRE) :
           - Si sus-décalage ST ou arythmie dangereuse -> Écris "🔴 ALERTE ROUGE : APPEL 15/112"
           - Si anomalies mineures -> Écris "🟠 ALERTE ORANGE : CONSULTATION RAPIDE"
           - Si normal -> Écris "🟢 RAS : NORMAL"
        
        DISCLAIMER :
        Conclus impérativement par : "Analyse générée par une IA (Prototype). Ne remplace pas l'avis d'un médecin."
        """
           
        print("Analyse experte en cours avec gpt-4o...")

         response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": instruction_systeme},
                {"role": "user", "content": [
                    {"type": "text", "text": "Fais l'analyse clinique complète de cet ECG."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            max_tokens=800 # On laisse un peu plus de place pour la réponse détaillée
        )
           
        print("\n--- RAPPORT CLINIQUE IA ---")
        print(response.choices[0].message.content)
        
except Exception as e:
    print(f"Erreur : {e}")

       

