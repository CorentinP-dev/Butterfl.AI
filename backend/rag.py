import openai
from backend.summary_manager import get_latest_summary, update_summary
from vector_database.index_documents import get_events_for_conversation, add_alternative_event


# Fonction pour appeler l'API OpenAI et générer une réponse
def call_openai_api(conversation_id, user_input):
    client = openai.OpenAI()

    # Récupérer le dernier résumé généré
    summary = get_latest_summary(conversation_id)

    # Récupérer les événements passés
    events = get_events_for_conversation(conversation_id, n_results=5)
    events_text = "\n".join([f"- {event['title']}: {event['description']}" for event in events])

    # Construire le prompt avec une meilleure structure
    prompt = f"""
    🏰 **Jeu narratif interactif - Histoire alternative** 🏰

    📜 **Contexte de l’histoire alternative actuelle** :  
    {summary}

    🔍 **Événements passés importants** :  
    {events_text}

    🎭 **Action du joueur** :  
    {user_input}

    ✍️ **Règles pour générer la suite :**  
    1️⃣ **Respecte l’histoire alternative en cours.** Ne reviens jamais à la réalité historique initiale.  
    2️⃣ **Adopte un ton immersif et captivant**, comme un maître du jeu. Décris les conséquences du choix du joueur avec détails.  
    3️⃣ **Propose systématiquement des choix interactifs** à la fin du texte, permettant au joueur d’influencer la suite du récit.  
    4️⃣ **Ajoute un sentiment de progression.** Le joueur doit sentir que ses décisions influencent réellement le destin du monde uchronique.  

    ✨ **Génère maintenant la suite de l’histoire en respectant ces principes.**
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "Tu es un narrateur expert en uchronie. Ta mission est de créer une histoire immersive où chaque choix du joueur modifie le cours de l'histoire."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    response_text = response.choices[0].message.content

    # Mettre à jour le résumé avec la nouvelle réponse générée
    update_summary(conversation_id, response_text)

    # Ajouter l'événement généré à ChromaDB
    event_id = f"EVT_{conversation_id}_{len(events) + 1}"  # Générer un identifiant unique
    add_alternative_event(conversation_id, event_id, f"Événement {len(events) + 1}", response_text, summary)

    return response_text
