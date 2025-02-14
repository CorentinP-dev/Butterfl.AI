import openai
from backend.summary_manager import get_latest_summary, update_summary
# from vector_database.index_documents import get_events_for_conversation, add_alternative_event  # RAG désactivé

# Fonction pour appeler l'API OpenAI et générer une réponse

def call_openai_api(conversation_id, user_input, temperature=0.7):
    client = openai.OpenAI()
    print(f"🔵 Température envoyée à OpenAI: {temperature}")

    summary = get_latest_summary(conversation_id)

    # RAG désactivé
    # events = get_events_for_conversation(conversation_id, n_results=3)
    # events_summary = summarize_events(events)

    # Nouveau prompt optimisé
    prompt = f"""
       🏰 **Jeu narratif interactif - Histoire alternative** 🏰

       📜 **Contexte de l’histoire alternative actuelle** :  
       {summary}

       🎭 **Action du joueur** :  
       {user_input}

       ✍️ **Règles pour générer la suite :**  
       1️⃣ **Respecte l’histoire alternative en cours.** Ne reviens jamais à la réalité historique initiale.  
       2️⃣ **Adopte un ton immersif et captivant**, comme un maître du jeu. Décris les conséquences du choix du joueur avec détails.  
       3️⃣ **Propose systématiquement des choix interactifs** à la fin du texte, permettant au joueur d’influencer la suite du récit.  
       4️⃣ **Ajoute un sentiment de progression.** Le joueur doit sentir que ses décisions influencent réellement le destin du monde uchronique.  

       ✨ **Génère maintenant la suite de l’histoire en respectant ces principes.**
       """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un narrateur d'histoires alternatives, créant des récits immersifs et cohérents où chaque choix du joueur influence l'histoire."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=1000
        )
        response_text = response.choices[0].message.content
    except Exception as e:
        print(f"🔴 Erreur lors de l’appel OpenAI : {e}")
        return "Une erreur s'est produite lors de la génération de l'histoire."

    update_summary(conversation_id, response_text)

    # RAG désactivé
    # event_id = f"EVT_{conversation_id}_{len(events) + 1}"
    # add_alternative_event(conversation_id, event_id, f"Événement {len(events) + 1}", response_text, summary)

    return response_text
