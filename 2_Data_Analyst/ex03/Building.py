import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy as sa

def main():
    # Connexion à la base PostgreSQL
    engine = sa.create_engine("postgresql://mservage:mysecretpassword@localhost:5432/piscineds")

    # On récupère uniquement les achats
    query = """
    SELECT user_id, product_id, price
    FROM customers
    WHERE event_type = 'purchase';
    """
    df = pd.read_sql(query, engine)

    # --------- Bar Chart 1 : Fréquence des achats par tranche ---------

    # Nombre d’achats par utilisateur
    order_counts = df.groupby("user_id")["price"].size()
    step = 10
    max_value = 40
    bins = list(range(0, max_value + step, step))
    binned = pd.cut(order_counts, bins=bins, right=False)
    counts_per_bin = binned.value_counts().sort_index()
    left_edges = bins[:-1]  # [0, 10, 20, 30]
    heights = counts_per_bin.values
    width = step
    sns.set_style("darkgrid")
    plt.figure(figsize=(8, 5))
    ax = plt.gca()
    ax.set_facecolor("#f0f0f0")

    plt.bar(left_edges, heights, width=width, align='edge', color="#4C72B0", alpha=0.4, edgecolor='white')
    plt.xticks(bins)
    plt.grid(True, axis='y', color='white', linewidth=1.5)

    plt.xlabel("Nombre d’achats")
    plt.ylabel("Nombre de clients")
    plt.title("Répartition des clients selon leur nombre d’achats")
    plt.tight_layout()
    plt.show()

    # --------- Bar Chart 2 : Montant total dépensé par tranche ---------

    spent_per_user = df.groupby("user_id")["price"].sum()
    # Définir les bins centrés : -25 à 225 → centres à 0, 50, 100, ...
    bins = [-25, 25, 75, 125, 175, 225]
    binned = pd.cut(spent_per_user, bins=bins, right=False)
    counts = binned.value_counts().sort_index()

    # Calcul des centres des bins pour placer les barres
    centers = [(interval.left + interval.right) / 2 for interval in counts.index]

    # Affichage
    sns.set_style("darkgrid")
    plt.figure(figsize=(8, 5))
    ax = plt.gca()
    ax.set_facecolor("#f0f0f0")

    # Barres centrées
    plt.bar(centers, counts.values, width=50, color="#4C72B0", alpha=0.4, edgecolor='white')

    # Ticks bien positionnés
    plt.xticks(centers)

    # Grille blanche
    plt.grid(True, axis='y', color='white', linewidth=1.5)

    # Étiquettes
    plt.xlabel("monetary value in ₳")
    plt.ylabel("customers")
    plt.title("")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
