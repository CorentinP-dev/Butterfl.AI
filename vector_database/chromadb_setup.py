import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Définition du chemin de la base ChromaDB
CHROMA_DB_DIR = "chroma_db"


# Fonction pour initialiser et récupérer la collection ChromaDB
def get_chroma_collection():
    """Retourne une instance de la base ChromaDB prête à être utilisée."""
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings, collection_name="history_france")
