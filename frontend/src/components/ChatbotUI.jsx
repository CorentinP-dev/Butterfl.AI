import { useState, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

const CONVERSATION_UUID = window.crypto.randomUUID();

function LinkRenderer(props) {
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
  const [loadingMessage, setLoadingMessage] = useState("");
  const [temperature, setTemperature] = useState(0.7);
  const [errorMessage, setErrorMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [showPopup, setShowPopup] = useState(true);


  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/query";

  const loadingMessages = [
    { name: "une biere", emoji: "🍺" },
    { name: "un dry martini", emoji: "🍸" },
    { name: "un champagne", emoji: "🥂" },
    { name: "un café", emoji: "☕️" },
    { name: "un verre de lait", emoji: "🥛" },
    { name: "un whisky", emoji: "🥃" },
    { name: "une tequila sunrise", emoji: "🍹" },
    { name: "un biberon", emoji: "🍼" },
    { name: "un cocktail pas ouf", emoji: "🧉" },
    { name: "un verre de bordeaux", emoji: "🍷" },
  ];

  const updateLoadingMessage = () => {
    const randomMessage = loadingMessages[Math.floor(Math.random() * loadingMessages.length)];
    setLoadingMessage(`John le Barman sert ${randomMessage.name} ${randomMessage.emoji}`);
  };

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(updateLoadingMessage, 1000);
    }
    return () => clearInterval(interval);
  }, [loading]);

  useEffect(() => {
    if (messages.length > 0) {
      window.scrollTo(0, document.body.scrollHeight);
    }
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage("");

    try {
      const prompt = query;
      setQuery("");
      setMessages((prevMessages) => [...prevMessages, { role: "user", content: prompt }]);

      console.log("🔵 Température AVANT envoi :", temperature);

      const res = await axios.post(API_URL, {
        query: prompt,
        conversation_id: CONVERSATION_UUID,
        temperature: temperature,
      });

      console.log("🟢 Réponse API :", res.data);

      setMessages((prevMessages) => [...prevMessages, { role: "assistant", content: res.data.response }]);
      setResponse(res.data.response);
    } catch (error) {
      console.error("🔴 Erreur API :", error);
      setErrorMessage("Erreur lors de la récupération des données.");
    }

    setLoading(false);
  };

  const handleBeerClick = () => {
    setTemperature((prevTemp) => {
      const newTemp = Math.min(prevTemp + 0.1, 3); // test
      console.log("🍺 Nouvelle Température :", newTemp);
      return newTemp;
    });
  };

  const handleWaterClick = () => {
    setTemperature((prevTemp) => {
      const newTemp = Math.max(prevTemp - 0.1, 0);
      console.log("🥤 Nouvelle Température :", newTemp);
      return newTemp;
    });
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-white p-4 chat-container">
      {showPopup && (
        <div className="mt-6 p-4 bg-gray-700 text-white rounded-lg self-start max-w-xs">
          <h2 className="text-xl font-bold mb-2">Et si ... ?</h2>
          <p>Bienvenue, dans le butterfly, le bar de John.<br/>Avec John vous aimez bien refaire le monde.<br/>À chaque ça commence avec "Et si ..."</p>
          <p>Attention l'abus d'alcool est dangereux pour la santé.</p>
          <button className="mt-4 bg-blue-500 px-4 py-2 rounded" onClick={() => setShowPopup(false)}>
            J'ai compris
          </button>
        </div>
      )}
      <div className="flex flex-col items-center justify-center h-full">
        <h1 className="text-3xl font-semibold text-center mb-6">Butterfl.IA 🦋</h1>
        <form className="w-full gap-2" onSubmit={handleSubmit}>
          <div className="espace">
            {loading ? loadingMessage : ""}
            <div className="ton-oncle">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Posez une question..."
                className="w-full p-3 border border-gray-700 rounded-lg bg-red-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
              />
              <button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg transition duration-200"
                disabled={loading}
              >
                {loading ? "Recherche ..." : "Envoyer"}
              </button>

              {/* Jauge de température juste au-dessus des boutons */}
              <div className="temperature-control w-full mt-6 mb-4">
                <p className="text-center text-lg mb-2">Température : {temperature.toFixed(1)}</p>
                <div className="w-full bg-gray-600 rounded-full h-2 mb-4">
                  <div
                    className="bg-blue-500 h-2 rounded-full"
                    style={{ width: `${(temperature / 5) * 100}%` }}
                  ></div>
                </div>
              </div>

              {/* Boutons pour ajuster la température */}
              <div className="buttons-container">
                <input
                  type="button"
                  value="🍺"
                  className="beer-button"
                  onClick={handleBeerClick}
                />
                <input
                  type="button"
                  value="🥤"
                  className="water-button"
                  onClick={handleWaterClick}
                />
              </div>
            </div>
          </div>
        </form>

        {messages.map((message, index) =>
          message.role === "user" ? (
            <div key={index} className="mt-6 p-4 bg-blue-600 text-white rounded-lg self-end max-w-xs">
              <p className="text-gray-300">{message.content}</p>
            </div>
          ) : (
            <div key={index} className="mt-6 p-4 bg-gray-700 text-white rounded-lg self-start max-w-xs">
              <h2 className="font-bold text-lg text-gray-200">Réponse :</h2>
              <p className="text-gray-300">
                <ReactMarkdown components={{ a: LinkRenderer }}>
                  {message.content}
                </ReactMarkdown>
              </p>
            </div>
          )
        )}
      </div>
    </div>
  );
}
