import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def standardize_data(df, label_col="knight"):
	# on enleve les col non numériques
	# ici juste knight
	features = df.drop(columns=[label_col])
	scaler = StandardScaler()
	standardized = scaler.fit_transform(features)
	standardized_df = pd.DataFrame(standardized, columns=features.columns)
	standardized_df[label_col] = df[label_col].values
	return standardized_df

def plot_scatter_std(df, x, y):
	plt.figure(figsize=(6, 6))
	for label in [0, 1]:
		sub = df[df["knight"] == label]
		plt.scatter(sub[x], sub[y], alpha=0.6, label="Sith" if label == 0 else "Jedi")
	plt.xlabel(x)
	plt.ylabel(y)
	plt.title(f"Standardized: {x} vs {y}")
	plt.legend()
	plt.grid(True)
	plt.tight_layout()
	plt.show()

def main():
	train_df = pd.read_csv("../data/Train_knight.csv")
	train_df.columns = train_df.columns.str.strip()
	train_df["knight"] = train_df["knight"].map({"Jedi": 1, "Sith": 0})

	print(train_df.head(1))
	std_df = standardize_data(train_df)
	print(std_df.head(1))

	# On réutilise le scatter plot : Empowered vs Prescience
	plot_scatter_std(std_df, "Empowered", "Prescience")

if __name__ == "__main__":
	main()
