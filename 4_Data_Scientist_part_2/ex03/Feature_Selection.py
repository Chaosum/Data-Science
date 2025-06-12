import pandas as pd
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor



def compute_vif(df):
    vif_data = pd.DataFrame()
    vif_data["feature"] = df.columns
    # Calcul du VIF pour chaque feature
    vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(df.shape[1])]
    # tolerance = 1 / vif car VIF = 1 / tolerance et tolerance = 1 - Ri^2
    # R^2 mesure à quel point une variable peut être prédite par les autres — plus il est proche de 1, plus cette variable est redondante
    vif_data["Tolerance"] = 1 / vif_data["VIF"]
    return vif_data

def drop_high_vif_features(df, threshold=5.0):
    while True or df.shape[1] < 1:
        # Étape 1 : Calcul du VIF pour les colonnes actuelles
        vif = compute_vif(df)

        # Étape 2 : Identifier le plus gros VIF
        max_vif = vif["VIF"].max()

        # Étape 3 : Si ce VIF dépasse le seuil, on élimine la colonne correspondante
        if max_vif > threshold:
            max_feature = vif.loc[vif["VIF"].idxmax(), "feature"]
            df = df.drop(columns=[max_feature])

        # Étape 4 : Sinon, on a terminé
        else:
            break

    # Retourne le dataframe filtré et les VIFs finaux
    return compute_vif(df)


def main():
    """
    VIF = 1 / (1 - Ri^2)
    Ri^2 measures how much the variable Xi can be explained by the other features.
    The higher Ri^2, the higher the VIF.
    A very high VIF → Ri^2 close to 1 → multicollinearity → should be avoided.
    VIF measures multicollinearity: whether a feature is redundant with the others.
    """
    # Chargement du dataset
    df = pd.read_csv("../data/Train_knight.csv")

    # Séparation des features
    X = df.drop(columns=["knight"])

    # Standardisation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_df = pd.DataFrame(X_scaled, columns=X.columns)

    raw_vif = compute_vif(X_df)
    print("pre filter")
    print(f"{'':>15}{'VIF':>15}{'Tolerance':>15}")
    for row in raw_vif.sort_values("VIF", ascending=False).itertuples(index=False):
        print(f"{row.feature:15}{row.VIF:15.6f}{row.Tolerance:15.6f}")
    print()
    # Étape 2-3 : VIF - filtering
    final_vif = drop_high_vif_features(X_df)
    print("filtered")
    print(f"{'':>15}{'VIF':>15}{'Tolerance':>15}")
    for row in final_vif.sort_values("VIF", ascending=False).itertuples(index=False):
        print(f"{row.feature:15}{row.VIF:15.6f}{row.Tolerance:15.6f}")



if __name__ == "__main__":
    main()