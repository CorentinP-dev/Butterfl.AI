from summary_manager import get_latest_summary, update_summary

# ID de conversation fictif pour le test
conversation_id = "test_10"

# Texte simulé pour l'histoire alternative
text1 = "Napoléon a gagné Waterloo et commence une conquête de l'Europe."
text2 = "L'Angleterre prépare une riposte et Wellington mène une offensive."

# Test de mise à jour et de récupération
print("🔹 Mise à jour du résumé avec le premier texte...")
update_summary(conversation_id, text1)
print("Résumé actuel :", get_latest_summary(conversation_id))

print("\n🔹 Mise à jour du résumé avec un deuxième événement...")
update_summary(conversation_id, text2)
print("Résumé mis à jour :", get_latest_summary(conversation_id))
