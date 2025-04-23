import requests
import sys
import os
import msvcrt
from dotenv import load_dotenv
from includes.filmauswahl import zeige_filmauswahl
from includes.savedata import save_moviedata

load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


def suche_filme(titel):
    url = f"https://api.themoviedb.org/3/search/movie?include_adult=true&language=de-DE&page=1&query={titel}"
    response = requests.get(url, headers=headers)
    return response.json().get("results", [])

def filminfos(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=de-DE"
    response = requests.get(url, headers=headers)
    return response.json()

def warte_auf_taste():
    print("\nFertig. Drücke [Enter] für einen neuen Durchlauf oder [ESC] zum Beenden.")
    while True:
        key = msvcrt.getch()
        if key == b'\x1b':  # ESC
            return False
        elif key in (b'\r', b'\n'):  # Enter
            return True


def clear_console():
    os.system("cls")

def main():
    while True:
        clear_console()
        try:
            titel = input("Filmtitel eingeben: ")
            filme = suche_filme(titel)
            if not filme:
                print("Keine Ergebnisse gefunden.")
                return

            auswahl = zeige_filmauswahl(filme)
            print(f"Lade Infos zu \"{auswahl['title']}\" (ID: {auswahl['id']})...")
            save_moviedata(filminfos(auswahl['id']))
        except KeyboardInterrupt:
            print("\nBeendet mit STRG+C.")
            break
        
        if not warte_auf_taste():
            break

if __name__ == "__main__":
    main()