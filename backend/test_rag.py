import unittest
from unittest.mock import patch, MagicMock
from backend.rag import call_openai_api
from backend.summary_manager import get_latest_summary

class TestRAG(unittest.TestCase):
    @patch("backend.rag.openai.OpenAI")
    def test_call_openai_api(self, mock_openai):
        """Teste si call_openai_api retourne une réponse formatée sans appeler OpenAI."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Réponse simulée de l'IA"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        response = call_openai_api("test_rag_interactive_003", "Quelle est la capitale de la France ?")
        self.assertIsInstance(response, str)
        self.assertEqual(response, "Réponse simulée de l'IA")

    @patch("backend.summary_manager.get_latest_summary")
    def test_get_latest_summary(self, mock_summary):
        """Teste si get_latest_summary retourne un résumé simulé."""
        mock_summary.return_value = "Réponse simulée de l'IA"