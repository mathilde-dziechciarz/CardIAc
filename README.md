# CardIAc : Assistant IA pour l'analyse d'ECG

## 1. Le Problème
Les maladies cardiovasculaires nécessitent une détection rapide. Notre projet vise à aider les patients et les urgentistes à analyser un électrocardiogramme (ECG) instantanément pour détecter des anomalies critiques.

## 2. La Solution (Agentic AI)
CardIAc est un agent autonome qui :
- Récupère une image ou des données d'ECG.
- Analyse les tracés via une IA multimodale.
- Compare les résultats aux standards médicaux.
- **Action autonome :** Si une anomalie grave est détectée, il prépare une alerte pour les urgences. Sinon, il rassure le patient.

## 3. Installation Technique
Pour lancer ce projet :
1. Cloner le dépôt.
2. Installer les dépendances : `pip install -r requirements.txt`
3. Configurer la clé API dans un fichier `.env`.
4. Lancer l'agent : `python main.py`

## 4. Architecture
- **Langage :** Python
- **IA :** OpenAI GPT-4o (via API)
- **Sécurité :** Gestion des clés via variables d'environnement.
