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
