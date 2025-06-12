import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    filePath = "./data/Train_knight.csv"
    if not os.path.isfile(filePath):
        print("Files not found in the data folder.")
        return
    try:
        df = pd.read_csv(filePath)
        # X = df.drop(columns=["knight"])
        df["knight"] = df["knight"].apply(lambda x: 1 if x == "Jedi" else 0)
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df)
        # Le PCA (Principal Component Analysis) est une méthode de réduction de dimension
        # qui transforme les données pour garder l'information la plus importante (la variance),
        # tout en supprimant les redondances.
        pca = PCA()
        pca.fit(df_scaled)

        explained_variance = pca.explained_variance_ratio_ * 100

        print("Variances (Percentage):")
        print(np.round(explained_variance, 8))
        print("\nCumulative Variance (Percentage):")
        cumulative_variance = np.cumsum(explained_variance)
        print(np.round(cumulative_variance, 8))
        # Ici on peut représenter les données en 7 dimensions au lieu de 30,
        # tout en gardant 90% de l’information initiale.

        # Graph
        plt.plot(cumulative_variance)
        plt.xlabel("Number of components")
        plt.ylabel("explained variance (%)")
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    main()
