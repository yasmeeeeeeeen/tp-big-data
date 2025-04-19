import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
from requests.exceptions import ConnectTimeout, RequestException

sys.stdout.reconfigure(encoding='utf-8')


WIKIPEDIA_URL = "https://fr.wikipedia.org/wiki/"

def get_page_info(page_title):
    url = WIKIPEDIA_URL + page_title.replace(" ", "_") 
    
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status()   

        soup = BeautifulSoup(response.text, "html.parser")

       
        title = soup.find("h1", {"id": "firstHeading"}).text.strip()

        
        last_edit_info = soup.find("li", {"id": "footer-info-lastmod"})
        last_edit_text = last_edit_info.text if last_edit_info else "Inconnu"

       
        last_edit_date = last_edit_text.replace("Cette page a été modifiée pour la dernière fois le ", "").strip()

        return {
            "title": title,
            "last_edit_date": last_edit_date,
            "url": url
        }
    
    except (ConnectTimeout, RequestException) as e:
        print(f"Erreur lors de la récupération des informations de la page {page_title} : {e}")
        return None

def get_random_pages(limit=10):
    API_URL = "https://fr.wikipedia.org/w/api.php"
    pages = []
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": 0,
        "rnlimit": min(limit, 500)  # Max 500 par requête
    }

    while len(pages) < limit:
        try:
            response = requests.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            pages.extend([page["title"] for page in response.json()["query"]["random"]])
        except (ConnectTimeout, RequestException) as e:
            print(f"Erreur de connexion : {e}. Réessayer...")
            time.sleep(5)
            continue

        if len(pages) < limit:
            time.sleep(2)  
    return pages[:limit]


def main():
    print("Récupération de la liste des pages...")
    pages = get_random_pages(limit=10000)  
    print(f"{len(pages)} pages récupérées.")

    data = []

    for i, page_title in enumerate(pages, start=1):
        print(f"Scraping de la page {i} : {page_title}")
        info = get_page_info(page_title)
        if info:
            data.append(info)

        if i % 20 == 0:  
            time.sleep(2)

    df = pd.DataFrame(data)
    output_file = "wikipedia_pages10000.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Données exportées dans '{output_file}'.")


if __name__ == "__main__":
    main()
