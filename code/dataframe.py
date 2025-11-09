import pandas as pd
import requests
import time
import json

# Charger ton CSV ===
file_path = "mettre le chemin d'acces"
df = pd.read_csv(file_path)

# Vérifie les colonnes attendues
print("Colonnes du CSV :", df.columns.tolist())

# === 2️⃣ Créer une liste pour stocker les résultats ===
results = []

# === 3️⃣ Boucle sur chaque chanson ===
for index, row in df.iterrows():
    artist = row["artist"]
    track = row["track_name"]
    mbid = row["id"]

    print(f"\n🎧 Traitement {index+1}/{len(df)} : {artist} - {track}")

    url = f"https://acousticbrainz.org/api/v1/{mbid}/high-level"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Récupérer uniquement la section "highlevel"
            features = data.get("highlevel", {})

            # Extraire les principales caractéristiques avec précaution
            feature_values = {
                "artist": artist,
                "track_name": track,
                "mbid": mbid
            }

            for feature_name, feature_data in features.items():
                # Certaines features ont un sous-dictionnaire avec 'value'
                if isinstance(feature_data, dict) and "value" in feature_data:
                    feature_values[feature_name] = feature_data["value"]
                else:
                    feature_values[feature_name] = None

            results.append(feature_values)
            print(f"✅ Données ajoutées ({len(feature_values)} colonnes)")

        else:
            print(f"⚠️ Erreur {response.status_code} pour {track}")
            results.append({
                "artist": artist,
                "track_name": track,
                "mbid": mbid
            })

    except Exception as e:
        print(f"❌ Erreur pour {track} :", e)
        results.append({
            "artist": artist,
            "track_name": track,
            "mbid": mbid
        })

    # Attendre 1 seconde pour respecter la limite API
    time.sleep(1)

# === 4️⃣ Convertir la liste en DataFrame ===
features_df = pd.DataFrame(results)

# === 5️⃣ Sauvegarder dans un fichier ===
output_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/acousticbrainz_features.csv"
features_df.to_csv(output_path, index=False, encoding="utf-8")

print("\n✅ Extraction terminée !")
print(f"💾 Données sauvegardées dans : {output_path}")
print(f"📊 Taille finale du tableau : {features_df.shape[0]} lignes x {features_df.shape[1]} colonnes")
