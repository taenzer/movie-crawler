import os
import re
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
from includes.datapreview import zeige_und_bestaetige

load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

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

def get_trailer_url(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=de-DE"
    response = requests.get(url, headers=headers)
    videos = response.json().get("results", [])
    
    # Filter & sort
    filtered = [
        video for video in videos
        if video["type"].lower() == "trailer" and video["official"] and video["site"].lower() == "youtube"
    ]
    # Sort nach Datum (frühestes zuerst)
    sorted_videos = sorted(filtered, key=lambda v: datetime.fromisoformat(v["published_at"].replace("Z", "+00:00")))

    if sorted_videos:
        return f"https://www.youtube.com/watch?v={sorted_videos[0]['key']}"
    else:
        return ""


def save_moviedata(movie):
    clean_title = sanitize_filename(movie.get('title', 'error'))
    folder_path = os.path.join(f"{os.getcwd()}\data\\", clean_title)
    os.makedirs(folder_path, exist_ok=True)

    relevant_data = {
        "titel": movie.get('title'),
        "jahr": movie.get('release_date'),
        "laufzeit": movie.get('runtime'),
        "beschreibung": movie.get('overview'),
        "studios": [firma["name"] for firma in movie.get('production_companies')],
        "trailer": get_trailer_url(movie.get('id')),
        "genres": [genre["name"] for genre in movie.get('genres')],
    }

    if(zeige_und_bestaetige(relevant_data)):
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

