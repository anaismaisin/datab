import pandas as pd
import requests
import time

# === 1. Charger le CSV contenant les MBID ===
file_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/tracks_with_mbid.csv"
df = pd.read_csv(file_path)

# === 2. Fonction pour récupérer les features AcousticBrainz ===
def get_acousticbrainz_features(mbid):
    url = f"https://acousticbrainz.org/api/v1/{mbid}/high-level"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        if "highlevel" not in data:
            return None
        hl = data["highlevel"]

        features = {}
        for key, value in hl.items():
            if isinstance(value, dict):
                features[f"{key}_value"] = value.get("value")
                features[f"{key}_prob"] = value.get("probability")
        return features

    except Exception as e:
        print(f"Erreur pour {mbid}: {e}")
        return None

# === 3. Boucle principale ===
print(f"Début du traitement ({len(df)} morceaux)")
features_data = []
all_features_keys = set()

for idx, row in df.iterrows():
    mbid = row.get("mbid")
    artist = row.get("artist", "Unknown")
    track = row.get("track_name", "Unknown")

    if pd.isna(mbid) or not mbid:
        continue

    print(f"{idx+1}/{len(df)} - {artist} — {track}")
    features = get_acousticbrainz_features(mbid)

    if features:
        all_features_keys.update(features.keys())
        base_info = {"artist": artist, "track_name": track, "mbid": mbid}
        base_info.update(features)
        features_data.append(base_info)
        print(f"  {len(features)} features extraites")
    else:
        print("  Aucune feature disponible, ligne ignorée")

    time.sleep(1)

# === 4. Construire le DataFrame final ===
if not features_data:
    print("Aucun morceau avec features trouvé.")
else:
    df_features = pd.DataFrame(features_data)
    ordered_cols = ["artist", "track_name", "mbid"] + sorted(list(all_features_keys))
    df_features = df_features[ordered_cols]

    # === 5. Sauvegarde ===
    output_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/tracks_with_all_features.csv"
    df_features.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\nTerminé : {len(df_features)} morceaux sauvegardés dans {output_path}")
    print(f"Nombre total de features collectées : {len(all_features_keys)//2}")
