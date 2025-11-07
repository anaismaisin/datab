import musicbrainzngs
import requests
import json

# 1️⃣ Configurer MusicBrainz
musicbrainzngs.set_useragent("anamaisin", "0.1.0", "anais.maisin@gmail.com")

# 2️⃣ Rechercher un morceau précis (ici Freddie Mercury - Living On My Own)
try:
    result = musicbrainzngs.search_recordings(artist="Freddie Mercury", recording="Living On My Own", limit=1)
    recording = result["recording-list"][0]
    print(f"Titre : {recording['title']}")
    print(f"MBID du morceau : {recording['id']}")
except musicbrainzngs.NetworkError as e:
    print(" Erreur réseau :", e)
    exit()

# 3️⃣ Requête vers AcousticBrainz (high-level)
mbid = recording["id"]
url = f"https://acousticbrainz.org/api/v1/{mbid}/high-level"

response = requests.get(url)

print("\n--- Résultat AcousticBrainz (high-level) ---")
if response.status_code == 200:
    data = response.json()

    # Quelques features intéressantes
    print("Mood :", data["highlevel"]["mood_acoustic"]["value"])
    print("Danceability :", data["highlevel"]["danceability"]["value"])
    print("Gender voix :", data["highlevel"]["gender"]["value"])
    print("Style global :", data["highlevel"]["genre_dortmund"]["value"])
    print("Energy :", data["highlevel"]["mood_happy"]["value"])

else:
    print("Erreur :", response.status_code, "- Données non disponibles pour ce morceau.")

print(json.dumps(data["highlevel"], indent=4))
