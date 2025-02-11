# 📌 Chatbot Historique - Projet IA & RAG

## 🚀 Description

Ce projet est un **chatbot intelligent** basé sur **GPT-4** et un système de **RAG (Retrieval-Augmented Generation)**. Il est conçu pour aider les étudiants et professeurs à obtenir des réponses précises en utilisant des **sources documentaires indexées** dans une base de données vectorielle.

### 🏗 **Technologies utilisées**

- **Backend :** FastAPI, LangChain, ChromaDB, OpenAI API
- **Frontend :** React (Vite), TailwindCSS
- **Base de données :** ChromaDB (stockage vectoriel des documents)

---

## 📂 Structure du projet

```
/chatbot_project
│── /backend           # API et RAG
│   ├── api.py        # API FastAPI
│   ├── rag.py        # Gestion des embeddings et requêtes ChromaDB
│── /frontend         # Interface utilisateur
│   ├── src/components/ChatbotUI.jsx  # Composant du chatbot
│   ├── package.json  # Dépendances Frontend
│── /vector_database  # Gestion des données vectorielles
│   ├── chromadb/          # Base de données vectorielle ChromaDB
│   ├── index_documents.py  # Indexation des documents
│   ├── chromadb_setup.py   # Configuration de ChromaDB
│   ├── query_chromadb.py   # Recherche dans la base vectorielle
│   ├── test_index.py       # Tests d’indexation et requêtes
│── /data_scraping    # Données extraites et nettoyées
│── requirements.txt  # Dépendances Backend
│── .gitignore        # Exclusions Git
│── README.md         # Documentation
```

---

## ⚙️ Installation & Configuration

### **1️⃣ Cloner le projet**

```bash
git clone https://github.com/CorentinP-dev/chatbot_histoire
cd chatbot_histoire
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

### **3️⃣ Lancer l’API**

```bash
cd backend/
python3 api.py
```

L’API sera disponible sur `http://127.0.0.1:8000`

---

### **4️⃣ Installation du Frontend (aller dans le fichier frontend)**

```bash
cd frontend
npm install
```

#### Créer un fichier `.env.local` avec dedans : 

```bash
VITE_API_URL=http://127.0.0.1:8000/query
```

### **5️⃣ Lancer le Frontend**

```bash
npm run dev
```

Accédez au chatbot sur `http://localhost:5173/`

---

## 🔍 Utilisation

1. **Lancer le Backend** (`python api.py`)
2. **Lancer le Frontend** (`npm run dev`)
3. **Poser des questions sur l’histoire** via l’interface du chatbot

---

## 📌 Fonctionnalités

✅ Recherche contextuelle avec ChromaDB\
✅ Réponses enrichies par GPT-4\
✅ Affichage des sources des réponses\
✅ Interface utilisateur moderne et intuitive

---

## 🛠 Améliorations futures

-

🚀 **Contribuez & Améliorez le projet !** 🎯

Tous droits réservés à Corentin PELLETIER

