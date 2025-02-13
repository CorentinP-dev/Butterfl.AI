from index_documents import add_alternative_event, get_events_for_conversation

# ID de conversation fictif pour le test
conversation_id = "test_convo_001"

# Simulation d'événements dans l'histoire alternative
add_alternative_event(conversation_id, "EVT_001", "Napoléon conquiert Londres", "Après sa victoire à Waterloo, Napoléon envahit l'Angleterre et établit un gouvernement militaire.", "Conquête de l'Angleterre en 1815")
add_alternative_event(conversation_id, "EVT_002", "Révolte anglaise contre Napoléon", "Les forces anglaises résistent à l'occupation et organisent une insurrection à Londres.", "Occupation française de Londres en 1816")

# Récupération des événements pour cette conversation
print("🔹 Récupération des événements de la conversation :")
events = get_events_for_conversation(conversation_id)
for event in events:
    print(event)
