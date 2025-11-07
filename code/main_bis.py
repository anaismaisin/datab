import musicbrainzngs
import requests
import json
import random
import time

# 1️⃣ Configurer MusicBrainz
musicbrainzngs.set_useragent("anamaisin", "0.1.0", "anais.maisin@gmail.com")

artists_names = [
    "Adele",
    "Ed Sheeran",
    "Taylor Swift",
    "Drake",
    "Beyoncé",
    "Rihanna",
    "The Weeknd",
    "Billie Eilish",
    "Bruno Mars",
    "Dua Lipa"
]

# 3️⃣ Dictionnaire pour stocker les chansons
artists_songs = {}

print("🔍 Récupération des 10 chansons les plus connues pour chaque artiste...\n")

for name in artists_names:
    try:
        # Recherche de l'artiste (on prend le premier résultat le plus pertinent)
        result = musicbrainzngs.search_artists(artist=name, limit=1)
        if not result["artist-list"]:
            print(f"⚠️ Aucun résultat trouvé pour {name}")
            continue

        artist = result["artist-list"][0]
        artist_id = artist["id"]

        print(f"\n🎤 {artist['name']} — ID : {artist_id}")
        print("   Récupération des morceaux...")

        # Récupère jusqu’à 100 morceaux, puis on filtrera les 10 premiers
        recordings_data = musicbrainzngs.browse_recordings(artist=artist_id, limit=100)
        recordings = recordings_data.get("recording-list", [])

        # Supprime les doublons par titre
        seen_titles = set()
        songs = []
        for rec in recordings:
            title = rec["title"]
            if title.lower() not in seen_titles:
                seen_titles.add(title.lower())
                songs.append({
                    "title": title,
                    "id": rec["id"]
                })
            if len(songs) == 10:
                break

        # Stocke dans le dictionnaire principal
        artists_songs[name] = songs

        # Affiche les résultats
        for i, song in enumerate(songs, start=1):
            print(f"   {i}. {song['title']} — MBID : {song['id']}")

        time.sleep(1)  # Pause pour ne pas spammer l’API

    except musicbrainzngs.NetworkError as e:
        print(f"⚠️ Erreur réseau pour {name} :", e)
        time.sleep(3)
    except Exception as e:
        print(f"⚠️ Problème pour {name} :", e)
        time.sleep(2)

# 4️⃣ Optionnel : sauvegarde dans un fichier JSON
import json
with open("top10_chansons_artistes.json", "w", encoding="utf-8") as f:
    json.dump(artists_songs, f, indent=4, ensure_ascii=False)

print("\n✅ Extraction terminée ! Les données ont été sauvegardées dans 'top10_chansons_artistes.json'.")