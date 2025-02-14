# 📌 "And if ..." - Jeu Narratif IA

## 🚀 Description

**"And if ..."** est un **jeu narratif interactif** développé par Butterfl_AI, utilisant **GPT-4** pour générer des histoires alternatives basées sur des changements historiques proposés par le joueur. Chaque choix du joueur influence l'uchronie et façonne l'histoire.

### 🏗 **Technologies utilisées**

- **Backend :** Python, OpenAI API
- **Frontend :** React, TailwindCSS
- **Base de données :** SQLite (pour stocker l'historique et les résumés)

---

## 📂 Structure du projet

```
/and_if_project
│── /backend              # Backend du jeu narratif
│   ├── rag.py            # Gestion de l'interaction avec l'API OpenAI et génération des récits
│   ├── summary_manager.py# Gestion des résumés dynamiques (backend)
│   ├── conversations.py  # Stockage des échanges bruts pour le frontend (backend)
│── /frontend             # Interface utilisateur
│   ├── src/components/GameUI.jsx  # Interface du jeu
│   ├── package.json      # Dépendances Frontend
│── requirements.txt      # Dépendances Backend
│── .gitignore            # Exclusions Git
│── README.md             # Documentation
```

---

## ⚙️ Installation & Configuration

### **1️⃣ Cloner le projet**

```bash
git clone https://github.com/CorentinP-dev/Butterfl.AI
```
#### Installer un environnement Python3
- Linux / Mac
 ```
  python3 -m venv myenv
  source myenv/bin/activate
  ```
- Windows
 ```
  python3 -m venv myenv
  myenv\Scripts\activate
  ```
#### Créer un fichier `.env` et y ajouter :
  ```
  OPENAI_API_KEY=your_openai_api_key
  ```


### **2️⃣ Installation du Backend (aller dans le fichier backend)**

```bash
pip3 install -r requirements.txt
```

### **3️⃣ Lancer le Backend**

```bash
python -m backend.api
```

---

### **4️⃣ Installation du Frontend (aller dans le fichier frontend)**

```bash
cd frontend
npm install
```

#### Créer un fichier `.env.local` avec dedans : 

```bash
VITE_API_URL=http://127.0.0.1:8000
```

### **5️⃣ Lancer le Frontend**

```bash
npm run dev
```

---

## 🔍 Utilisation

1. **Lancer le Backend** (`python rag.py`)
2. **Lancer le Frontend** (`npm run dev`)
3. **Jouer en proposant des changements historiques et en faisant des choix pour influencer l'histoire**

---

## 📌 Fonctionnalités

✅ Génération d'uchronies interactives avec GPT-4\
✅ Résumés dynamiques assurant la continuité\
✅ Interface utilisateur moderne et immersive

---

## 🛠 Améliorations futures
- Migration vers un modèle LLM local (Phi-2)
- Optimisation des prompts

🚀 **Contribuez & Améliorez le projet !** 🎯

Tous droits réservés à Butterfl_AI
