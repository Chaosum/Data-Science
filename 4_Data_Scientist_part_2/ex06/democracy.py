import pandas as pd
import os
import sys

from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


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

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, y_train, X_test, y_test


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


        clf1 = KNeighborsClassifier(n_neighbors=13)
        clf2 = DecisionTreeClassifier(max_depth=5, random_state=42)
        clf3 = LogisticRegression(max_iter=1000)
        
        voting_clf = VotingClassifier(estimators=[
            ('knn', clf1),
            ('tree', clf2),
            ('logreg', clf3)
        ], voting='hard')

        voting_clf.fit(X_train, y_train)

        predictions = voting_clf.predict(X_test)

        with open("KNN.txt", "w") as f:
            for pred in predictions:
                f.write(pred + "\n")

        if y_test is not None:
            print(f"F1 score: {f1_score(y_test, predictions, pos_label='Jedi'):.5f}")
        else:
            print("Predictions saved to Voting.txt (no labels provided to compute F1-score).")
    except Exception as e:
        print(f"An error occurred: {e}")
        return

if __name__ == "__main__":
    main()