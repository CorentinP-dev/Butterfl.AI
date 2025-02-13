import chromadb
from sentence_transformers import SentenceTransformer

# Charger un modèle d'embedding local
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def embedding_function(text):
    return embedding_model.encode(text).tolist()


# Connexion à ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="alternative_history_events")


# Fonction pour ajouter un nouvel événement dans ChromaDB
def add_alternative_event(conversation_id, event_id, title, description, context):
    event_text = f"{title}. {description}. Contexte : {context}"
    embedding = embedding_function(event_text)

    collection.add(
        ids=[event_id],
        embeddings=[embedding],
        metadatas=[{
            "conversation_id": conversation_id,
            "title": title,
            "description": description,
            "context": context
        }]
    )

    print(f"✅ Événement ajouté à la conversation {conversation_id} : {title}")


# Fonction pour récupérer les événements liés à une conversation
def get_events_for_conversation(conversation_id, n_results=5):
    results = collection.query(
        query_embeddings=[[0] * 384],  # Utilise un vecteur neutre pour récupérer les événements
        n_results=n_results,
        where={"conversation_id": conversation_id}
    )

    if not results["ids"]:  # Vérifie si aucun événement n'est trouvé
        print("⚠ Aucun événement trouvé pour cette conversation.")
        return []

    events = []
    for i in range(len(results["ids"][0])):
        events.append({
            "id": results["ids"][0][i],
            "title": results["metadatas"][0][i]["title"],
            "description": results["metadatas"][0][i]["description"],
            "context": results["metadatas"][0][i]["context"]
        })

    return events

