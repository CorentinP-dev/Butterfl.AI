import openai
import sqlite3
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("La clé API OpenAI est manquante. Ajoutez-la dans le fichier .env")


# Initialisation de la base de données pour stocker les résumés
def init_db():
    conn = sqlite3.connect("summary.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS summaries (
                        conversation_id TEXT PRIMARY KEY,
                        summary TEXT
                    )''')
    conn.commit()
    conn.close()


# Fonction pour récupérer le dernier résumé de la conversation
def get_latest_summary(conversation_id):
    conn = sqlite3.connect("summary.db")
    cursor = conn.cursor()
    cursor.execute("SELECT summary FROM summaries WHERE conversation_id = ?", (conversation_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ""  # Retourne le résumé ou une chaîne vide


# Fonction pour générer un résumé avec OpenAI GPT-4
def generate_summary(text):
    client = openai.OpenAI()  # Initialisation du client OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Tu es un narrateur d'histoires alternatives. Ta tâche est de résumer les événements fictifs créés par le joueur dans le cadre d'une uchronie."},
            {"role": "user",
             "content": f"""
            📜 **Histoire alternative actuelle** :  
            {text}

            ✍️ **Instructions pour le résumé** :  
            - Résume les événements clés de l’histoire alternative de manière concise mais détaillée (5 à 7 phrases maximum).  
            - Maintiens la cohérence avec l’univers uchronique et les décisions du joueur.  
            - Conserve un ton narratif immersif pour faciliter la continuité de l’histoire.

            ✨ Génère maintenant un résumé dynamique respectant ces principes.
            """}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content


# Fonction pour mettre à jour le résumé dans la base de données
def update_summary(conversation_id, new_text):
    summary = get_latest_summary(conversation_id) + " " + new_text  # Ajout du nouveau texte au résumé existant
    summary = generate_summary(summary)  # Génération d'un résumé condensé

    conn = sqlite3.connect("summary.db")
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO summaries (conversation_id, summary) VALUES (?, ?)", (conversation_id, summary))
    conn.commit()
    conn.close()

    return summary


# Initialiser la base de données au démarrage
init_db()
