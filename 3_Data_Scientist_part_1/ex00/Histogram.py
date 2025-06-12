from matplotlib import pyplot as plt
import pandas as pd

def main():
	# Lire le fichier CSV
	df = pd.read_csv("./data/Test_knight.csv")
	
	features = df.columns
	n_features = len(features)

	# Choisir un nombre de lignes / colonnes pour les subplots
	n_cols = 5
	n_rows = (n_features // n_cols) + (n_features % n_cols > 0)  # arrondi supérieur

	# graphique 1 : overlay des knights
	plt.figure(figsize=(10, 10))

	for i, col in enumerate(features):
		plt.subplot(n_rows, n_cols, i + 1)
		plt.title(col)
		plt.hist(df[col], bins=40, alpha=0.5, color='green', label='Knights')
		plt.legend(fontsize=6)
		plt.tight_layout()
	# graphique 2 : overlay des knights par feature
	df = pd.read_csv("./data/Train_knight.csv")

	features = df.columns[:-1] 
	n_features = len(features)

	# Choisir un nombre de lignes / colonnes pour les subplots
	n_cols = 5
	n_rows = (n_features // n_cols) + (n_features % n_cols > 0)  # arrondi supérieur
	plt.figure(figsize=(10, 10))

	for i, col in enumerate(features):
		plt.subplot(n_rows, n_cols, i + 1)
		for label in df['knight'].unique():
			subset = df[df['knight'] == label]
			plt.hist(subset[col], color="blue" if label == "Jedi" else "red", bins=35, alpha=0.5, label=label)
		plt.title(col)
		plt.legend()
		plt.tight_layout()
	plt.show()


if __name__ == "__main__":
	main()
