import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

# 1. Chargement de la configuration (Clé API)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("--- Agent CardiAc (Vision) : Démarrage ---")

# 2. Fonction technique pour que l'IA puisse "voir" l'image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Nom du fichier image (DOIT être présent dans le dépôt GitHub)
image_path = "ECG-1.jpeg"

try:
    # Vérification de sécurité : l'image existe-t-elle ?
    if not os.path.exists(image_path):
        print(f"❌ ERREUR : L'image '{image_path}' est introuvable.")
        print("Assurez-vous d'avoir uploadé le fichier image sur GitHub/dans le dossier.")
    else:
        print(f"Lecture de l'image : {image_path}...")
        base64_image = encode_image(image_path)

        # 3. Le Prompt Système (Le cerveau du cardiologue)
        instruction_systeme = """
        Tu es CardiAc, un assistant IA expert en cardiologie d'urgence.
        Ta mission : Analyser visuellement l'ECG fourni.

        FORMAT DE RÉPONSE ATTENDU :
        1. Rythme : (Sinusal, Fibrillation, etc.)
        2. Anomalies visibles : (Segment ST, Ondes T, etc.)
        3. DIAGNOSTIC : (Normal ou Pathologique)
        4. ACTION : (Rien à signaler OU "ALERTE ROUGE - APPELER LE 15")
        
        IMPORTANT : Ajoute toujours le disclaimer : "Je suis une IA, consultez impérativement un médecin."
        """
        
        print("Analyse en cours avec le modèle gpt-4o...")
    
        # 4. Envoi de l'image et du texte à l'IA
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": instruction_systeme},
                {"role": "user", "content": [
                    {"type": "text", "text": "Voici l'ECG du patient. Analyse-le s'il te plaît."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            max_tokens=500
        )
        # 5. Affichage du résultat
        print("\n--- RÉSULTAT DE L'ANALYSE ---")
        print(response.choices[0].message.content)
        
except Exception as e:
    print(f"Une erreur technique est survenue : {e}")

