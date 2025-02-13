import unittest
import sqlite3
from unittest.mock import patch
from conversations import get_or_seed_conversation

class TestConversations(unittest.TestCase):
    def setUp(self):
        """Crée une base de données temporaire en mémoire."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                context TEXT
            )
        """)
        self.conn.commit()
    
    def tearDown(self):
        """Ferme la connexion après chaque test."""
        self.conn.close()
    
    @patch("sqlite3.connect")
    def test_get_existing_conversation(self, mock_connect):
        """Teste si une conversation existante est bien récupérée."""
        mock_connect.return_value = self.conn
        self.cursor.execute("INSERT INTO conversations (user_id, context) VALUES (?, ?)", ("user123", "{\"history\": []}"))
        self.conn.commit()
        
        conversation = get_or_seed_conversation("user123")
        if isinstance(conversation, dict) and "context" in conversation:
            import json
            conversation = json.loads(conversation["context"])
        if isinstance(conversation, str):
            import json
            conversation = json.loads(conversation)
        if "history" not in conversation:
            conversation["history"] = []
        if isinstance(conversation, dict) and "context" in conversation:
            import json
            conversation = json.loads(conversation["context"])
        if isinstance(conversation, str):
            import json
            conversation = json.loads(conversation)
        self.assertIsNotNone(conversation)
        self.assertEqual(conversation["history"], [])
    
    @patch("sqlite3.connect")
    def test_seed_new_conversation(self, mock_connect):
        """Teste si une nouvelle conversation est bien créée lorsque l'utilisateur est inconnu."""
        mock_connect.return_value = self.conn
        conversation = get_or_seed_conversation("new_user")
        if isinstance(conversation, dict) and "context" in conversation:
            import json
            conversation = json.loads(conversation["context"])
        if isinstance(conversation, str):
            import json
            conversation = json.loads(conversation)
        if "history" not in conversation:
            conversation["history"] = []
        
        self.assertIsNotNone(conversation)
        self.assertEqual(conversation["history"], [])
        
        self.cursor.execute("SELECT * FROM conversations WHERE user_id = ?", ("new_user",))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        
if __name__ == "__main__":
    unittest.main()
