from dotenv import load_dotenv
from chromadb_setup import get_chroma_collection

# Charger les variables d'environnement
load_dotenv()

# Récupération de la base ChromaDB via la fonction factorisée
vectorstore = get_chroma_collection()


# Fonction pour interroger ChromaDB via LangChain
def query_chromadb(query, top_k=5):
    print("\n🔍 Recherche des documents pertinents...")
    results = vectorstore.similarity_search(query, k=top_k)

    if not results:
        print("Aucun document trouvé.")
        return

    print("\n🔹 Résultats trouvés :")
    for i, doc in enumerate(results):
        print(f"\n[{i + 1}] {doc.metadata.get('title', 'Titre inconnu')}")
        print(f"URL: {doc.metadata.get('url', 'URL non disponible')}")
        print(f"Extrait: {doc.page_content[:500]}...")  # Affichage des 500 premiers caractères

    # Retourner les documents pour une intégration dans GPT-4
    return results


# Fonction pour afficher tous les documents indexés
def list_indexed_documents():
    print("\n📂 Documents indexés dans ChromaDB :")
    results = vectorstore.get()
    if not results or not results.get("metadatas"):
        print("Aucun document trouvé dans la base.")
        return

    for i, meta in enumerate(results["metadatas"]):
        print(f"[{i + 1}] {meta.get('title', 'Titre inconnu')} - {meta.get('url', 'URL non disponible')}")


# Exécution du script avec une question utilisateur
def main():
    while True:
        print("\nOptions :")
        print("1 - Poser une question à ChromaDB")
        print("2 - Lister les documents indexés")
        print("3 - Quitter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            query = input("\nPose une question : ")
            query_chromadb(query)
        elif choice == "2":
            list_indexed_documents()
        elif choice == "3":
            break
        else:
            print("Option invalide. Veuillez choisir 1, 2 ou 3.")


if __name__ == "__main__":
    main()
