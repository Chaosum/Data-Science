import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import sys

def load_data(train_path, test_path):
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    test = test.drop(columns=['knight']) if 'knight' in test.columns else test
    try:
        X_train = train.drop(columns=['knight'])
    except Exception as e:
        raise Exception("Wrong train file format, {e}")
    y_train = train['knight']
    return X_train, y_train, test

def train_decision_tree(X_train, y_train, max_depth=None):
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    return model

def save_predictions(y_pred, filename='Tree.txt'):
    with open(filename, 'w') as f:
        for label in y_pred:
            f.write(f"{label}\n")

def display_tree(model, feature_names):
    plt.figure(figsize=(15, 8))
    plot_tree(model, feature_names=feature_names, filled=True)
    plt.show()

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
        X_train, y_train, X_test = load_data(sys.argv[1], sys.argv[2])

        model = train_decision_tree(X_train, y_train)
        y_pred = model.predict(X_test)

        save_predictions(y_pred)
        f1 = f1_score(y_train, model.predict(X_train), average='weighted')
        print(f"F1 Score on training data: {f1*100:.2f}%")
        display_tree(model, X_train.columns)
        # Calculate and print F1 score
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the file paths are correct.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return


if __name__ == "__main__":
    main()
