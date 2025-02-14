from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["ACCELERATE_DISABLE_MPS"] = "1"

model_name = "mistralai/Mistral-3B-v0.1"  # Exemple, si disponible, ou un autre modèle entre 1-3B

print("⏳ Téléchargement et chargement du modèle Mistral 3B sur CPU...")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
    device_map="cpu"
)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

print("✅ Modèle Mistral 3B chargé avec succès sur CPU !")

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

    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
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
