import pandas as pd
import musicbrainzngs
import time
import re

# === 1. Charger le CSV ===
file_path = r"C:\Users\anais\OneDrive\master 1 q1\datab\code\top_tracks_simple.csv"
df = pd.read_csv(file_path)

# Normaliser les colonnes
df = df.rename(columns={"Artist": "artist", "track_name": "track_name"})
df = df[["artist", "track_name"]]

# Ajouter la colonne mbid si elle n’existe pas
if "mbid" not in df.columns:
    df["mbid"] = None

# === 2. Configurer MusicBrainz ===
musicbrainzngs.set_useragent("anamaisin", "0.1.0", "anais.maisin@gmail.com")

# === 3. Fonction de nettoyage du titre ===
def clean_track_name(name):
    name = re.sub(r"\(.*?\)", "", name)
    name = re.sub(r"feat\.?.*", "", name, flags=re.IGNORECASE)
    return name.strip()

# === 4. Fonction pour récupérer le MBID ===
def get_recording_mbid(artist, track_name):
    try:
        result = musicbrainzngs.search_recordings(
            artist=artist,
            recording=track_name,
            limit=1
        )
        if "recording-list" in result and len(result["recording-list"]) > 0:
            return result["recording-list"][0]["id"]
        else:
            return None
    except Exception as e:
        print(f"Erreur pour {artist} — {track_name}: {e}")
        return None

# === 5. Boucle principale ===
for idx, row in df.iterrows():
    # On ne traite que les lignes sans mbid déjà défini
    if pd.isna(row["mbid"]):
        artist = row["artist"]
        track = clean_track_name(row["track_name"])
        print(f"Traitement {idx+1}/{len(df)} : {artist} — {track}")

        mbid = get_recording_mbid(artist, track)
        df.at[idx, "mbid"] = mbid
        print(" → MBID :", mbid)

        time.sleep(1)  # pause d’1 seconde pour respecter la limite MusicBrainz

# === 6. Sauvegarde ===
output_path = r"C:\Users\anais\OneDrive\master 1 q1\datab\code\tracks_with_mbid.csv"
df.to_csv(output_path, index=False, encoding="utf-8")
print("Terminée. Fichier sauvegardé :", output_path)

mbid_df = df[["track_name", "artist", "mbid"]].copy()

print("\n🎵 Tableau final (aperçu) :")
print(mbid_df.head(10))

