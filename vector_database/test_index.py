import os
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv
from chromadb_setup import get_chroma_collection

# Charger les variables d'environnement
load_dotenv()

# Configuration des chemins
DATA_DIR = "../data_scraping/wikipedia_data"

# Vérification du dossier wikipedia_data
if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Le dossier {DATA_DIR} n'existe pas. Vérifiez son emplacement !")

# Récupération de la base ChromaDB via la fonction factorisée
vectorstore = get_chroma_collection()


# Fonction pour charger et chunker les documents
def load_and_chunk_documents(limit=5):
    documents = []
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")][:limit]  # Limiter aux 5 premiers fichiers
    print(f"📂 Chargement des {len(files)} premiers fichiers JSON...")

    for idx, file in enumerate(files):
        file_path = os.path.join(DATA_DIR, file)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            text = data.get("text", "")
            title = data.get("title", "")
            url = data.get("url", "")

            if text:
                # Chunking du texte
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=100
                )
                chunks = text_splitter.split_text(text)

                for chunk in chunks:
                    documents.append(Document(page_content=chunk, metadata={"title": title, "url": url}))
        print(f"✔️ {idx + 1}/{len(files)} - Fichier {file} traité ({len(chunks)} chunks extraits)")

    return documents


# Fonction pour indexer les documents dans ChromaDB
def index_documents():
    documents = load_and_chunk_documents()
    print(f"🗂️ Indexation de {len(documents)} chunks de texte...")

    # Ajout des documents à ChromaDB via LangChain
    vectorstore.add_documents(documents)
    print("✅ Indexation terminée !")


if __name__ == "__main__":
    index_documents()
