import pandas as pd
from sklearn.model_selection import train_test_split
import sys
import os

def main():
	# Lire le fichier d'origine
	if len(sys.argv) != 2:
		print("Usage: python split.py <path_to_csv>")
		return
	if not os.path.isfile(sys.argv[1]):
		print(f"Erreur : le fichier {sys.argv[1]} n'existe pas.")
		return
	df = pd.read_csv(sys.argv[1])
	df.columns = df.columns.str.strip()

	# Split 80% entraînement, 20% validation
	train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)

	# Sauvegarde
	train_df.to_csv("Training_knight.csv", index=False)
	val_df.to_csv("Validation_knight.csv", index=False)

	# Info utilisateur
	print("Split terminé :")
	print(f"  - Données totales : {len(df)}")
	print(f"  - Entraînement    : {len(train_df)} lignes (80%)")
	print(f"  - Validation      : {len(val_df)} lignes (20%)")

if __name__ == "__main__":
	main()
