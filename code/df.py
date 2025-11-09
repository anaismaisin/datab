import pandas as pd
import musicbrainzngs
import time

file_path = "C:/Users/anais/OneDrive/master 1 q1/datab/top_500_tracks_before_2018.csv"
df = pd.read_csv(file_path)

df = df.rename(columns={
    "Artist": "artist",
    "track_name": "track_name"
})
df = df[["artist", "track_name"]]

# Afficher les 5 premières lignes pour vérification
print("Aperçu du tableau :\n")
print(df.head())

output_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/clean_tracks.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\n Tableau nettoyé et sauvegardé dans : {output_path}")

#extraction des id dans musicbrainz
# Configurer MusicBrainz
musicbrainzngs.set_useragent("anamaisin", "0.1.0", "anais.maisin@gmail.com")

# Lire le fichier « clean » avec artist + track_name
file_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/clean_tracks.csv"
df = pd.read_csv(file_path)
df["mbid"] = None

def get_recording_mbid(artist, track_name):
    try:
        result = musicbrainzngs.search_recordings(
            artist=artist,
            recording=track_name,
            limit=1,
            fmt="json"
        )
        if result["recording-list"]:
            return result["recording-list"][0]["id"]
        else:
            return None
    except Exception as e:
        print(f"Erreur pour {artist} — {track_name}: {e}")
        return None

# Boucle pour chaque ligne
for idx, row in df.iterrows():
    if pd.isna(row["mbid"]):  # seulement si encore vide
        artist = row["artist"]
        track = row["track_name"]
        print(f"Traitement {idx+1}/{len(df)} : {artist} — {track}")
        mbid = get_recording_mbid(artist, track)
        df.at[idx, "mbid"] = mbid
        print(" → MBID :", mbid)
        time.sleep(1)  # pause d’1 seconde

# Sauvegarder le tableau modifié
output_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/tracks_with_mbid.csv"
df.to_csv(output_path, index=False, encoding="utf-8")
print("✅ Terminée. Fichier modifié sauvegardé :", output_path)