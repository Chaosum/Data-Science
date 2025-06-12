import os
import sys
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt

def load_data(train_path, test_path):
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    try:
        X_train = train.drop(columns=['knight']).values
        y_train = train['knight'].values
    except Exception as e:
        raise Exception(f"Wrong train file format, {e}")
    X_test = test.drop(columns=['knight']).values if 'knight' in test.columns else test.values
    y_test = test['knight'].values if 'knight' in test.columns else None

    return X_train, y_train, X_test, y_test


def euclidean_distance(x1, x2):
    # calcule la somme de toutes les erreurs au carré entre les deux vecteurs
    # puis prend la racine carrée de cette somme
    # x1 represente un point de test
    # x2 represente un point d'entrainement
    return np.sqrt(np.sum((x1 - x2) ** 2))


def predict_one(x, X_train, y_train, k):
    # x : point à prédire (une observation du dataset de test)
    # X_train : l'ensemble des points d'entraînement (features uniquement, sans les labels)
    # y_train : les classes associées à chaque point de X_train (ex: "Jedi" ou "Sith")
    # k : le nombre de voisins les plus proches à considérer
    distances = [euclidean_distance(x, x_train) for x_train in X_train]
     # On trie les distances et on garde les indices des k plus petits (donc les k plus proches voisins)
    k_indices = np.argsort(distances)[:k]
    k_labels = [y_train[i] for i in k_indices]
    return Counter(k_labels).most_common(1)[0][0] # jedi ou sith


def predict(X_test, X_train, y_train, k):
    # pour chaque point de test, on prédit sa classe en utilisant les k plus proches voisins
    return [predict_one(x, X_train, y_train, k) for x in X_test]


def evaluate_knn(X_val, y_val, X_train, y_train, k_values):
    f1_scores = []
    for k in k_values:
        y_pred = predict(X_val, X_train, y_train, k)
        score = f1_score(y_val, y_pred, pos_label="Jedi")
        f1_scores.append(score)
        print(f"k={k} -> F1-score: {score:.4f}")
    return f1_scores


def main():
    if len(sys.argv) != 3:
        print("Usage: python tree.py Train_knight.csv Test_knight.csv")
        return
    if not sys.argv[1].endswith('.csv') or not sys.argv[2].endswith('.csv'):
        print("Both arguments must be CSV files.")
        return
    if os.path.isfile(sys.argv[1]) == False or os.path.isfile(sys.argv[2]) == False:
        print("Both files must exist.")
        return

    try:
        X_train, y_train, X_test, y_test = load_data(sys.argv[1], sys.argv[2])

        # Choix du meilleur k
        # k impair pour éviter les égalités lors du count des voisins
        k_values = list(range(1, 20, 2))
        if y_test is not None:
            f1_scores = evaluate_knn(X_test, y_test, X_train, y_train, k_values)
            best_k = k_values[np.argmax(f1_scores)]
            print(f"Best k: {best_k}")
            plt.plot(k_values, f1_scores, marker='o')
            plt.xlabel("k")
            plt.ylabel("F1-score")
            plt.title("F1-score selon k (Validation Set)")
            plt.grid(True)
            plt.xticks(k_values)
            plt.show()
        else:
            # valeur par défaut si pas de y_test (test sans labels)
            # 13 est le nombre qu'on trouve avec le plus de précision
            print("No y_test provided, using default k=13")
            best_k = 13
        predictions = predict(X_test, X_train, y_train, best_k)
        with open("KNN.txt", "w") as f:
            for pred in predictions:
                f.write(pred + "\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        return

if __name__ == "__main__":
    main()