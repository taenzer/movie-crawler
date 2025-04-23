import requests
import os
import json
import re

# === DEINE API-KEYS HIER EINFÜGEN ===
OMDB_API_KEY = "DEIN_OMDB_API_KEY"
TMDB_API_KEY = "DEIN_TMDB_API_KEY"

def sanitize_filename(name):
    # Entferne ungültige Zeichen für Windows-Dateinamen
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_movie_info_omdb(title):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["Response"] == "True":
            return data
        else:
            print("Film nicht in OMDb gefunden.")
    else:
        print("Fehler bei OMDb-Anfrage.")
    return None

def get_movie_still_tmdb(title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    search_resp = requests.get(search_url)
    if search_resp.status_code == 200:
        results = search_resp.json().get("results")
        if results:
            movie_id = results[0]["id"]
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={TMDB_API_KEY}"
            images_resp = requests.get(details_url)
            if images_resp.status_code == 200:
                backdrops = images_resp.json().get("backdrops")
                if backdrops:
                    backdrop_path = backdrops[0]["file_path"]
                    return f"https://image.tmdb.org/t/p/original{backdrop_path}"
    print("Kein Filmstill bei TMDB gefunden.")
    return None

def download_image(url, filepath):
    try:
        img_data = requests.get(url).content
        with open(filepath, 'wb') as handler:
            handler.write(img_data)
        print(f"Bild gespeichert: {filepath}")
    except Exception as e:
        print(f"Fehler beim Herunterladen des Bildes: {e}")

def save_metadata(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Metadaten gespeichert: {filepath}")
    except Exception as e:
        print(f"Fehler beim Speichern der Metadaten: {e}")

if __name__ == "__main__":
    title = input("Gib den Filmtitel ein: ")
    movie = get_movie_info_omdb(title)

    if movie:
        clean_title = sanitize_filename(movie.get('Title', title))
        folder_path = os.path.join(os.getcwd(), clean_title)
        os.makedirs(folder_path, exist_ok=True)

        # Zeige Infos an
        print("\n--- OMDb Filminformationen ---")
        print(f"Titel: {movie.get('Title')}")
        print(f"Beschreibung: {movie.get('Plot')}")
        print(f"FSK: {movie.get('Rated')}")
        print(f"Länge: {movie.get('Runtime')}")
        print(f"Studio: {movie.get('Production')}")

        # Bild speichern
        if movie.get('Poster') and movie['Poster'] != "N/A":
            download_image(movie['Poster'], os.path.join(folder_path, "poster.jpg"))

        # Filmstill holen & speichern
        still_url = get_movie_still_tmdb(title)
        if still_url:
            download_image(still_url, os.path.join(folder_path, "filmstill.jpg"))

        # Metadaten als JSON speichern
        relevant_data = {
            "Titel": movie.get("Title"),
            "Beschreibung": movie.get("Plot"),
            "FSK": movie.get("Rated"),
            "Laufzeit": movie.get("Runtime"),
            "Produktionsfirma": movie.get("Production"),
            "Poster_URL": movie.get("Poster"),
            "Filmstill_URL": still_url or "Nicht gefunden"
        }
        save_metadata(relevant_data, os.path.join(folder_path, "info.json"))
