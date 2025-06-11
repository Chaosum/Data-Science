from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():

    df = pd.read_csv("../data/Train_knight.csv")
    X = df.drop(columns=["knight"])

    # 2. Standardisation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. PCA
    pca = PCA()
    pca.fit(X_scaled)

    # 4. Récupérer les variances (pourcentages)
    explained_variance = pca.explained_variance_ratio_ * 100

    # 5. Afficher
    print("Variances (Percentage):")
    print(np.round(explained_variance, 8))
    print("\nCumulative Variance (Percentage):")
    cumulative_variance = np.cumsum(explained_variance)
    print(np.round(cumulative_variance, 8))

    # Graph
    plt.plot(cumulative_variance)
    plt.xlabel("Number of components")
    plt.ylabel("Cumulative variance (%)")
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    main()
