import pandas as pd
import numpy as np
from collections import defaultdict

# === 1. Charger le CSV existant ===
file_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/tracks_with_all_features.csv"
df = pd.read_csv(file_path)
print(f"{len(df)} morceaux chargés.")

# === 2. Colonnes binaires à transformer en one-hot pondéré ===
binary_features = {
    "gender": ("male", "female"),
    "mood_acoustic": ("acoustic", "non_acoustic"),
    "mood_aggressive": ("aggressive", "non_aggressive"),
    "mood_electronic": ("electronic", "non_electronic"),
    "mood_happy": ("happy", "not_happy"),
    "mood_party": ("party", "not_party"),
    "mood_relaxed": ("relaxed", "not_relaxed"),
    "mood_sad": ("sad", "not_sad"),
    "timbre": ("bright", "dark"),
    "tonal_atonal": ("tonal", "atonal"),
    "voice_instrumental": ("voice", "instrumental"),
    "danceability": ("danceable", "not_danceable")
}

# === 3. Création des colonnes one-hot pondérées ===
for feature, (pos_label, neg_label) in binary_features.items():
    value_col = f"{feature}_value"
    prob_col = f"{feature}_prob"
    if value_col in df.columns and prob_col in df.columns:
        df[f"{feature}_{pos_label}"] = df.apply(
            lambda r: r[prob_col] if str(r[value_col]).lower() == pos_label.lower() else 0,
            axis=1
        )
        df[f"{feature}_{neg_label}"] = df.apply(
            lambda r: r[prob_col] if str(r[value_col]).lower() == neg_label.lower() else 0,
            axis=1
        )
        print(f" {feature}_{pos_label} et {feature}_{neg_label} ajoutées.")

# === 4. Fonction pour agréger les genres multi-modèles ===
def extract_genre_features(row, df_columns):
    genre_scores = defaultdict(float)
    for col in df_columns:
        if col.startswith("genre_") and col.endswith("_value"):
            base = col.replace("_value", "")
            value = row.get(f"{base}_value")
            prob = row.get(f"{base}_prob")
            if isinstance(value, str) and not pd.isna(prob):
                genre_scores[value] += prob

    total = sum(genre_scores.values())
    if total > 0:
        for g in genre_scores:
            genre_scores[g] /= total  # normalisation somme=1
    return genre_scores

# === 5. Extraire et ajouter les genres ===
genre_columns = set()
for idx, row in df.iterrows():
    genres = extract_genre_features(row, df.columns)
    for g, score in genres.items():
        colname = f"genre_{g.lower().replace(' ', '_')}"
        df.at[idx, colname] = score
        genre_columns.add(colname)
print(f" Genres extraits et ajoutés ({len(genre_columns)} genres uniques).")

# === 6. Remplacer NaN par 0 pour la similarité cosinus ===
df = df.fillna(0)

# === 7. Sauvegarde du CSV final ===
output_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/tracks_final_ready.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"\nFichier final sauvegardé : {output_path}")
print(f" {len(df)} morceaux prêts pour cosine similarity.")
