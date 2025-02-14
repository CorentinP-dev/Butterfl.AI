from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "teknium/OpenHermes-2.5-Mistral-7B"

print("⏳ Téléchargement et chargement du modèle OpenHermes 7B sur CPU...")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

print("✅ Modèle OpenHermes 7B chargé !")

while True:
    user_input = input("Proposez un changement historique pour commencer l'histoire (ou 'exit' pour quitter) : ")
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("Fin du test.")
        break

    prompt = f"""
    Tu es un narrateur d'histoires alternatives pour un jeu appelé 'And if ...'.
    Crée un récit immersif basé sur ce changement historique, décris les conséquences, et propose 3 choix interactifs à la fin.
    Contexte initial : {user_input}
    Commence l'histoire maintenant :
    """

    inputs = tokenizer(prompt, return_tensors="pt").to("gpu")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=500,
            do_sample=True,
            top_k=40,
            top_p=0.92,
            temperature=0.7,
            repetition_penalty=1.2
        )

    print("\n📝 Histoire générée :")
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
    print("\n---")
