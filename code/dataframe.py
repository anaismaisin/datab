# Étape 1 : importer la bibliothèque pandas
import pandas as pd

# Étape 2 : indiquer le chemin vers ton fichier CSV
# ⚠️ Mets bien le bon chemin selon où est ton fichier
file_path = "C:/Users/anais/OneDrive/master 1 q1/datab/code/top_tracks_simple.csv"

# Étape 3 : lire le CSV et créer le DataFrame
df = pd.read_csv(file_path)

# Étape 4 : afficher les 5 premières lignes
print(df.head())

# (Optionnel) vérifier le nom des colonnes
print(df.columns)
print(df)