from summary_manager import get_latest_summary, update_summary

# ID de conversation fictif pour le test
conversation_id = "test_10"

# Texte simulé pour l'histoire alternative
text1 = "Napoléon a gagné Waterloo et commence une conquête de l'Europe."
text2 = "L'Angleterre prépare une riposte et Wellington mène une offensive."

# Test de mise à jour et de récupération
print("🔹 Mise à jour du résumé avec le premier texte...")
update_summary(conversation_id, text1)
print("Résumé actuel :", get_latest_summary(conversation_id))

print("\n🔹 Mise à jour du résumé avec un deuxième événement...")
update_summary(conversation_id, text2)
print("Résumé mis à jour :", get_latest_summary(conversation_id))


import os
import sqlite3
import unittest
from summary_manager import init_db

class TestSummaryManager(unittest.TestCase):
    def setUp(self):
        """Supprime la base de données avant chaque test."""
        if os.path.exists("summary.db"):
            os.remove("summary.db")
    
    def test_init_db(self):
        """Vérifie que la base de données et la table summaries sont bien créées."""
        init_db()
        self.assertTrue(os.path.exists("summary.db"))  # Vérifie si le fichier existe
        
        conn = sqlite3.connect("summary.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='summaries';")
        table_exists = cursor.fetchone() is not None
        conn.close()
        
        self.assertTrue(table_exists, "La table summaries n'existe pas")

if __name__ == "__main__":
    unittest.main()

import os
import sqlite3
import unittest
from unittest.mock import patch, MagicMock
from summary_manager import init_db, generate_summary

class TestSummaryManager(unittest.TestCase):
    def setUp(self):
        """Supprime la base de données avant chaque test."""
        if os.path.exists("summary.db"):
            os.remove("summary.db")
    
    def test_init_db(self):
        """Vérifie que la base de données et la table summaries sont bien créées."""
        init_db()
        self.assertTrue(os.path.exists("summary.db"))  # Vérifie si le fichier existe
        
        conn = sqlite3.connect("summary.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='summaries';")
        table_exists = cursor.fetchone() is not None
        conn.close()
        
        self.assertTrue(table_exists, "La table summaries n'existe pas")
    
    @patch("summary_manager.openai.OpenAI")
    def test_generate_summary(self, mock_openai):
        """Vérifie que generate_summary() renvoie bien un résumé formaté."""
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Phrase 1. Phrase 2. Phrase 3."))]
        
        mock_client.chat.completions.create.return_value = mock_response
        
        summary = generate_summary("Texte de test")
        self.assertIsNotNone(summary)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)
        self.assertEqual(len(summary.split(".")), 4)  # 3 phrases + dernier split vide

if __name__ == "__main__":
    unittest.main()
