import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from conversations import get_or_seed_conversation
from rag import call_openai_api  # Mise à jour pour utiliser la nouvelle version du RAG

# Charger les variables d'environnement
load_dotenv()

# Création de l'API FastAPI
app = FastAPI()

# Ajouter CORS pour permettre les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (mettre un domaine précis en prod)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP
    allow_headers=["*"],  # Autorise tous les headers
)

# Modèle de requête pour l'API
class QueryModel(BaseModel):
    query: str
    conversation_id: str

# Endpoint de vérification de l'API
@app.get("/health")
def health_check():
    return {"status": "API is running"}

# Endpoint pour interroger le RAG
@app.post("/query")
def query_rag(request: QueryModel):
    conversation_id = request.conversation_id
    conversation = get_or_seed_conversation(conversation_id)
    response = call_openai_api(conversation_id, request.query)  # Mise à jour pour s'assurer que le contexte est pris en compte
    return {"response": response}

# Lancer le serveur si exécuté directement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
