import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# === 1. Charger le CSV final ===
file_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/tracks_final_ready.csv"
df = pd.read_csv(file_path)
print(f"{len(df)} morceaux chargés.")

# === 2. Générer une playlist aléatoire de 10 titres ===
playlist_random = df.sample(10, random_state=42)
playlist_ids = playlist_random.index.tolist()  # pour exclure de la base

print("\n Playlist aléatoire sélectionnée :")
print(playlist_random[["artist", "track_name"]])

# === 3. Sélectionner toutes les colonnes numériques pour la comparaison ===
feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
print(f"\n🔹 {len(feature_cols)} colonnes utilisées pour la recommandation.")

# === 4. Exclure la playlist de la base ===
df_base = df.drop(index=playlist_ids)

# === 5. Calculer la similarité cosinus et recommander ===
playlist_vector = playlist_random[feature_cols].mean(axis=0).values.reshape(1, -1)
base_vectors = df_base[feature_cols].values
sim = cosine_similarity(base_vectors, playlist_vector).flatten()

# Top 2 morceaux les plus similaires
top_indices = sim.argsort()[-2:][::-1]
reco_top = df_base.iloc[top_indices].copy()
top_scores = sim[top_indices]

# === 6. Afficher les résultats ===
print("\n Top 2 recommandations (basées sur toutes les features) :")
for i, row in enumerate(reco_top.itertuples()):
    print(f"{row.artist} — {row.track_name} | score: {top_scores[i]:.3f}")

# === 7. Créer un mini DataFrame avec les vecteurs ===
mini_df = pd.DataFrame(
    [playlist_vector.flatten(), 
     base_vectors[top_indices[0]], 
     base_vectors[top_indices[1]]],
    index=[
        "playlist_vector", 
        f"reco_1_{reco_top.iloc[0]['track_name']}", 
        f"reco_2_{reco_top.iloc[1]['track_name']}"
    ],
    columns=feature_cols
)

print("\n Mini DataFrame des vecteurs :")
print(mini_df.head())

# === 8. Sauvegarder en CSV ===
output_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/mini_vectors.csv"
mini_df.to_csv(output_path, index=True, encoding="utf-8")

print(f"\n Mini DataFrame sauvegardé : {output_path}")
