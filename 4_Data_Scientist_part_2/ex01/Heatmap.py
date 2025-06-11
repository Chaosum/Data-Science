import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def main():
	df = pd.read_csv("../data/Train_knight.csv")
	df.columns = df.columns.str.strip()
	df["knight"] = df["knight"].map({"Jedi": 1, "Sith": 0})

	features = [col for col in df.columns]
	corr = df[features].corrwith(df["knight"]).sort_values(ascending=False)
	# Make a Heatmap to see the Correlation Coefficient between the data
	plt.figure(figsize=(10, 8))
	custom_cmap = LinearSegmentedColormap.from_list(
	"custom", [ "black", "red", "white"]
    )
	sns.heatmap(df[features].corr(), annot=False, cmap=custom_cmap, cbar_kws={'label': 'Correlation Coefficient'})
	plt.show()

if __name__ == "__main__":
	main()