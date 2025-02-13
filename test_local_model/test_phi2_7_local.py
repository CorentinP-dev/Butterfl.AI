from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "microsoft/phi-2"

print("⏳ Téléchargement et chargement du modèle Phi-2 en float32 sur CPU...")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
    device_map="cpu"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

system_prompt = """
Tu es un narrateur d'histoires alternatives pour un jeu narratif interactif appelé 'And if ...'.
Ton rôle :
- Créer des récits immersifs et cohérents basés sur des changements historiques proposés par le joueur.
- Décrire les conséquences et l'évolution du monde avec richesse et détails.
- Proposer 3 choix d'actions interactives à la fin de chaque génération, permettant au joueur d'influencer le cours de l'histoire.
- Maintenir une continuité logique et éviter les contradictions dans le récit.
Tu es créatif, précis, et immersif.
"""

print("✅ Modèle chargé avec succès sur CPU en float32 !")

while True:
    user_input = input("Proposez un changement historique pour commencer l'histoire (ou 'exit' pour quitter) : ")
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("Fin du test.")
        break

    prompt = f"""
    {system_prompt}

    📜 **Contexte initial** :
    {user_input}
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
