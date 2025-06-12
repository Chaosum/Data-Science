from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

def reduce_to_2D(df):
	if "knight" in df.columns:
		X = df.drop(columns="knight")
	else:
		X = df
	pca = PCA(n_components=2)
	X_reduced = pca.fit_transform(X)
	return X_reduced

def plot_feature_pairs(train_df, test_df, x, y, w, z):
	plt.figure(figsize=(10, 8))

	# 1. Train (x, y) — coloré
	plt.subplot(2, 2, 1)
	for label in [0, 1]:
		sub = train_df[train_df["knight"] == label]
		plt.scatter(sub[x], sub[y], c="blue" if label == 0 else "red", alpha=0.6, label="Sith" if label == 0 else "Jedi")
	plt.ylabel(y)
	plt.legend()

	# 2. Test (x, y) — non coloré
	plt.subplot(2, 2, 3)
	plt.scatter(test_df[x], test_df[y], c="green",alpha=0.6)
	plt.xlabel(x)
	plt.ylabel(y)
	plt.legend(["knight"], loc="best")

	# 3. Train (w, z) — coloré
	plt.subplot(2, 2, 2)
	for label in [0, 1]:
		sub = train_df[train_df["knight"] == label]
		plt.scatter(sub[w], sub[z], alpha=0.6, c="blue" if label == 0 else "red" , label="Sith" if label == 0 else "Jedi")
	plt.ylabel(z)
	plt.legend()

	# 4. Test (w, z) — non coloré
	plt.subplot(2, 2, 4)
	plt.scatter(test_df[w], test_df[z], c="green", alpha=0.6)
	plt.xlabel(w)
	plt.ylabel(z)
	plt.legend(["knight"], loc="best")

	plt.tight_layout()
	plt.show()

def main():
	train_df = pd.read_csv("../data/Train_knight.csv")
	test_df = pd.read_csv("../data/Test_knight.csv")

	train_df.columns = train_df.columns.str.strip()
	test_df.columns = test_df.columns.str.strip()

	train_df["knight"] = train_df["knight"].map({"Jedi": 1, "Sith": 0})

	# Choisis tes features ici :
	x = "Empowered"
	y = "Prescience"
	w = "Deflection"
	z = "Survival"

	plot_feature_pairs(train_df, test_df, x=x, y=y, w=w, z=z)


if __name__ == "__main__":
	main()