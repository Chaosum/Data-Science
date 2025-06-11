import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import LinearSegmentedColormap



def plot_confusion_matrix(tp, fn, fp, tn):
    matrix = np.array([[tp, fn],
                       [fp, tn]])

    labels = ["0", "1"]

    plt.figure(figsize=(5, 4))
    custom_cmap = LinearSegmentedColormap.from_list(
        "custom", ["purple", "blue","green","yellow"]
    )
    sns.heatmap(matrix, annot=True, fmt="d", cmap=custom_cmap, 
                xticklabels=labels, yticklabels=labels)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.show()


def read_labels(path):
    with open(path, "r") as file:
        return [line.strip() for line in file.readlines()]

def main():

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for truthline, predictedline in zip(read_labels("../data/truth.txt"), read_labels("../data/predictions.txt")):
        TP += 1 if truthline == predictedline and truthline == "Jedi" else 0
        TN += 1 if truthline == predictedline and truthline == "Sith" else 0
        FP += 1 if truthline != predictedline and predictedline == "Jedi" else 0
        FN += 1 if truthline != predictedline and predictedline == "Sith" else 0


    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_jedi = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    precision_sith = TN / (TN + FN) if (TN + FN) > 0 else 0
    recall_sith = TN / (TN + FP) if (TN + FP) > 0 else 0
    f1_sith = 2 * precision_sith * recall_sith / (precision_sith + recall_sith) if (precision_sith + recall_sith) > 0 else 0

    accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0

    print(f"{'':<10} {'precision':>10} {'recall':>10} {'f1-score':>10} {'total':>10}")
    print(f"{'Jedi':<10} {precision:>10.2f} {recall:>10.2f} {f1_jedi:>10.2f} {TP + FN:>10.2f}")
    print(f"{'Sith':<10} {precision_sith:>10.2f} {recall_sith:>10.2f} {f1_sith:>10.2f} {TN + FP:>10.2f}")
    print()
    print(f"{'accuracy':<10} {'':>10} {'':>10} {accuracy:>10} {TP + TN + FP + FN:>10}")

    print(f"\nConfusion Matrix:")
    print(f"[[{TP} {FN}]")
    print(f" [{FP} {TN}]]")

    plot_confusion_matrix(TP, FN, FP, TN)

if __name__ == "__main__":
    main()
