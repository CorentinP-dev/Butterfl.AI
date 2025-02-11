import { useState, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

const CONVERSATION_UUID = window.crypto.randomUUID()

function LinkRenderer(props) {
  console.log({ props });
  return (
    <a href={props.href} target="_blank" rel="noreferrer">
      {props.children}
    </a>
  );
}

export default function Chatbot() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState(""); // Pour le message de chargement
  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/query";

  const [messages, setMessages] = useState([])

  const loadingMessages = [
    { name: "Voltaire", emoji: "⚡" },
    { name: "Rousseau", emoji: "🌱" },
    { name: "Montesquieu", emoji: "⚖️" },
    { name: "Diderot", emoji: "📚" },
    { name: "Kant", emoji: "💭" },
  ];

  // Fonction pour mettre à jour le message de chargement
  const updateLoadingMessage = () => {
    const randomMessage = loadingMessages[Math.floor(Math.random() * loadingMessages.length)];
    setLoadingMessage(`Je demande à ${randomMessage.name} ${randomMessage.emoji}`);
  };

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(updateLoadingMessage, 1000); // Change toutes les 1 secondes
    }
    return () => clearInterval(interval); // Clean-up lorsque le composant est démonté ou que le chargement s'arrête
  }, [loading]);

  useEffect(() => {
    if (messages.length > 0) {
      window.scrollTo(0, document.body.scrollHeight);
    }
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const prompt = query;
      setQuery("");
      setMessages(messages => {
        return [...messages, {role: "user", content: prompt}]
      })
      const res = await axios.post(API_URL, { query: prompt, conversation_id: CONVERSATION_UUID });
      setMessages(messages => {
        return [...messages, {role: "assistant", content: res.data.response}]
      })
      setResponse(res.data.response);
    } catch (error) {
      setResponse("Erreur lors de la récupération des données.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-4 chat-container">
      <div className="flex flex-col items-center justify-center h-full">
        <h1 className="text-3xl font-semibold text-center mb-6">LumIA 💡</h1>
        <h3 className="text-1l text-center mb-6">LumIA, l’héritière des Lumières pour éclairer votre savoir historique.</h3>
        <form className="w-full gap-2" onSubmit={handleSubmit}>
          <div className="espace">
            {loading ? loadingMessage : ""}
            <div className="ton-oncle">
              <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Posez une question..."
              className="w-full p-3 border border-gray-700 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
            />
            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg transition duration-200"
              disabled={loading}
            >
              {loading ? "Recherche ..." : "Envoyer"}
            </button>
            </div>

          </div>
        </form>
        {messages.map((message, index) =>
          message.role === "user" ? (
              <div className="mt-6 p-4 bg-gray-700 shadow-md rounded-lg">
                <h2 className="font-bold text-lg text-gray-200">Question :</h2>
                <p className="text-gray-300">{message.content}</p
                >
              </div>):
              <div className="mt-6 p-4 bg-gray-700 shadow-md rounded-lg">
                <h2 className="font-bold text-lg text-gray-200">Réponse :</h2>
                <p className="text-gray-300"><ReactMarkdown components={{a: LinkRenderer}}>{message.content}</ReactMarkdown></p>
              </div>
        )}
      </div>
    </div>
  );
}
