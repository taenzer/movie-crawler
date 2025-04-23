import os
import re
import json
import requests

def sanitize_filename(name):
    # Entferne ungültige Zeichen für Windows-Dateinamen
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_image(url, path, name_prefix):
    try:
        filename = url.split("/")[-1].split("?")[0]
        filename = f"{name_prefix}-{filename}"
        filepath = os.path.join(path, filename)
        img_data = requests.get(url).content
        with open(filepath, 'wb') as handler:
            handler.write(img_data)
        print(f"Bild gespeichert: {filename}")
    except Exception as e:
            print(f"Fehler beim Herunterladen des Bildes: {e}")

def save_meta(data, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Metadaten gespeichert: {filepath}")
    except Exception as e:
        print(f"Fehler beim Speichern der Metadaten: {e}")


def save_moviedata(movie):
    clean_title = sanitize_filename(movie.get('title', 'error'))
    folder_path = os.path.join(f"{os.getcwd()}\data\\", clean_title)
    os.makedirs(folder_path, exist_ok=True)

    relevant_data = {
        "titel": movie.get('title'),
        "jahr": movie.get('release_date'),
        "laufzeit": movie.get('runtime'),
        "beschreibung": movie.get('overview')
    }
    download_image(
        f"https://image.tmdb.org/t/p/w1280{movie.get('backdrop_path')}",
        folder_path,
        "backdrop"
    )
    download_image(
        f"https://image.tmdb.org/t/p/w780{movie.get('poster_path')}",
        folder_path,
        "poster"
    )
    save_meta(relevant_data, os.path.join(folder_path, "info.json"))

