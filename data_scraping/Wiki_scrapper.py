import requests
from bs4 import BeautifulSoup
import re
import time
import json
import os
from unidecode import unidecode

WIKI_BASE_URL = "https://fr.wikipedia.org/wiki/"
OUTPUT_DIR = "wikipedia_data"  # Dossier de sortie pour stocker les fichiers JSON
KEYWORDS_FILE = "wikipedia_keywords.json"  # Fichier contenant les mots-clés Wikipédia

# Création du dossier si inexistant
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


# Fonction pour récupérer et parser une page Wikipédia
def get_wikipedia_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur {response.status_code} en récupérant {url}")
        return None
    return BeautifulSoup(response.text, "html.parser")


# Fonction pour nettoyer et structurer le texte
def clean_text(soup):
    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        return ""

    # Suppression des balises non pertinentes
    for unwanted in content.find_all(["sup", "table", "style", "script", "figure", "img", "ul", "ol", "nav", "footer"]):
        unwanted.decompose()

    # Extraction des paragraphes avec titres de sections
    sections = []
    current_section = "Introduction"
    section_text = []

    for element in content.find_all(["h2", "h3", "p"]):
        if element.name in ["h2", "h3"]:
            if section_text:
                sections.append(f"{current_section}\n{' '.join(section_text)}")
                section_text = []
            current_section = element.get_text().strip()
        elif element.name == "p" and element.get_text().strip():
            section_text.append(element.get_text().strip())

    if section_text:
        sections.append(f"{current_section}\n{' '.join(section_text)}")

    # Nettoyage du texte
    cleaned_text = "\n\n".join(sections)
    cleaned_text = cleaned_text.replace('\xa0', ' ')  # Remplacer NBSP par un espace normal
    cleaned_text = re.sub(r'\[.*?\]', '', cleaned_text)  # Supprimer les références [1], [2], etc.
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Suppression des espaces multiples

    return cleaned_text


# Fonction principale de scraping
def scrape_wikipedia():
    # Charger les mots-clés depuis le fichier JSON
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        keywords_list = json.load(f)

    for keyword in keywords_list:
        url = WIKI_BASE_URL + keyword
        print(f"Scraping: {url}")

        soup = get_wikipedia_page(url)
        if not soup:
            continue

        title = soup.find("h1", {"id": "firstHeading"}).get_text().strip()
        text = clean_text(soup)

        print(f"Extrait {len(text)} caractères de texte pour {title}.")

        # Normalisation du titre pour le nom de fichier
        normalized_title = unidecode(title)
        file_name = os.path.join(OUTPUT_DIR, f"{re.sub(r'[^a-zA-Z0-9_-]', '_', normalized_title)}.json")

        # Sauvegarde dans un fichier JSON
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump({"title": title, "url": url, "text": text}, f, ensure_ascii=False, indent=4)

        time.sleep(1)  # Pause pour éviter de surcharger Wikipédia


# Lancer le scraping
scrape_wikipedia()
