import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def main():
	try:
		filePath = "./data/Train_knight.csv"
		if not os.path.isfile(filePath):
			print("Files not found in the data folder.")
			return
		df = pd.read_csv(filePath)
		df.columns = df.columns.str.strip()
		df["knight"] = df["knight"].map({"Jedi": 1, "Sith": 0})

		features = [col for col in df.columns]
		corr = df[features].corrwith(df["knight"]).sort_values(ascending=False)
		# Make a Heatmap to see the Correlation Coefficient between the data
		plt.figure(figsize=(10, 8))
		sns.heatmap(df[features].corr(), annot=False, cmap="inferno")
		plt.show()
	except Exception as e:
		print(f"An error occurred: {e}")

if __name__ == "__main__":
	main()