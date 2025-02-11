from rag import call_openai_api
from summary_manager import get_latest_summary

# ID de conversation fictif pour le test
conversation_id = "test_rag_interactive_003"

print("Bienvenue dans le test interactif du RAG Manager !")
print("Vous allez pouvoir interagir avec le modèle et voir l'évolution de l'histoire alternative.\n")

while True:
    user_input = input("Votre action dans l'histoire alternative : ")
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("Fin du test. Merci d'avoir participé !")
        break

    response = call_openai_api(conversation_id, user_input)
    print("\nRéponse du LLM :")
    print(response)

    summary = get_latest_summary(conversation_id)
    print("\nRésumé actuel de l'histoire :")
    print(summary)

    print("\n---\n")
