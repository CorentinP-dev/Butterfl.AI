conversations = {}

def seed_conversation(conversation_id: str):
    global conversations

    conversation = {
        "id": conversation_id,
        "messages": [{"role": "system", "content": "Tu es un assistant spécialisé en histoire."}],
    }

    conversations[conversation_id] = conversation
    return conversation


def get_or_seed_conversation(conversation_id: str):
    if conversation_id not in conversations:
        return seed_conversation(conversation_id)
    return conversations[conversation_id]
