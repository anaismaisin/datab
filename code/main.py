import musicbrainzngs
import requests
import json
import pandas as pd

# 1️⃣ Configurer MusicBrainz
musicbrainzngs.set_useragent("anamaisin", "0.1.0", "anais.maisin@gmail.com")

# 2️⃣ Rechercher un morceau précis (ici Freddie Mercury - Living On My Own)
try:
    result = musicbrainzngs.search_recordings(artist="Freddie Mercury", recording="Living On My Own", limit=1)
    recording = result["recording-list"][0]
    print(f"Titre : {recording['title']}")
    print(f"MBID du morceau : {recording['id']}")
except musicbrainzngs.NetworkError as e:
    print("❌ Erreur réseau :", e)
    exit()

# 3️⃣ Requête vers AcousticBrainz (high-level)
mbid = recording["id"]
url = f"https://acousticbrainz.org/api/v1/{mbid}/high-level"

response = requests.get(url)

print("\n--- Résultat AcousticBrainz (high-level) ---")
if response.status_code == 200:
    data = response.json()
    features = data.get("highlevel", {})

    # 4️⃣ Extraire les features sous forme de dictionnaire
    feature_values = {
        "artist": "Freddie Mercury",
        "track_name": recording["title"],
        "mbid": mbid
    }

    # Pour chaque feature, on récupère la catégorie (value) et la probabilité (probability)
    for feature_name, feature_data in features.items():
        if isinstance(feature_data, dict):
            # Ajoute la valeur catégorielle
            feature_values[feature_name] = feature_data.get("value")

            # Ajoute la probabilité numérique si elle existe
            if "probability" in feature_data:
                feature_values[f"{feature_name}_prob"] = feature_data["probability"]
        else:
            feature_values[feature_name] = None
            feature_values[f"{feature_name}_prob"] = None

    # 5️⃣ Transformer en DataFrame
    df = pd.DataFrame([feature_values])

    print("\n🎶 Caractéristiques extraites sous forme de tableau :")
    print(df.T)  # affichage vertical pour plus de lisibilité

    # 6️⃣ Sauvegarde optionnelle
    df.to_csv("freddie_mercury_features.csv", index=False, encoding="utf-8")
    print("\n💾 Fichier sauvegardé : freddie_mercury_features.csv")

else:
    print("❌ Erreur :", response.status_code, "- Données non disponibles pour ce morceau.")


