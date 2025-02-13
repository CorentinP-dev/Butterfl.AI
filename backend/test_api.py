import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.api import app # Importation de l'application FastAPI

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_health_endpoint(self):
        """Teste si l'endpoint /health fonctionne correctement."""
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "API is running"})
    
    @patch("backend.api.call_openai_api")
    def test_query_endpoint(self, mock_openai):
        """Teste l'endpoint /query avec un mock de call_openai_api."""
        mock_openai.return_value = "Réponse simulée de l'IA"
        response = client.post("/query", json={"query": "Quelle est la capitale de la France ?", "conversation_id": "test123"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "Réponse simulée de l'IA"})

if __name__ == "__main__":
    unittest.main()
