import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)

class TestIntegration(unittest.TestCase):
    @patch("backend.api.call_openai_api")
    def test_frontend_backend_query(self, mock_openai):
        """Teste l'intégration entre le frontend et le backend via /query."""
        mock_openai.return_value = "Réponse simulée de l'IA"
        response = client.post("/query", json={"query": "Quelle est la capitale de la France ?", "conversation_id": "test123"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "Réponse simulée de l'IA"})

    @patch("backend.api.call_openai_api")
    def test_frontend_backend_query_error(self, mock_openai):
        """Teste la gestion des erreurs lorsque OpenAI retourne une erreur."""
        mock_openai.side_effect = Exception("Erreur OpenAI")
        response = client.post("/query", json={"query": "Pourquoi le ciel est bleu ?", "conversation_id": "test456"})
        
        self.assertEqual(response.status_code, 500)
        self.assertIn("Erreur lors de la génération de la réponse", response.text)

if __name__ == "__main__":
    unittest.main()
