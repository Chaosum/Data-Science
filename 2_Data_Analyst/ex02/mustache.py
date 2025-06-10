from pandas import read_sql
from sqlalchemy import create_engine
from seaborn import boxplot
import matplotlib.pyplot as plt


def main():
    engine = create_engine(
        "postgresql://mservage:mysecretpassword@localhost:5432/piscineds"
    )
    query = """
    SELECT user_id, product_id, price
    FROM customers
    WHERE event_type = 'purchase';
    """

    df = read_sql(query, engine)
    df["price"] = df["price"].astype(float)
    print(f"{'count':<15}{df['price'].count():>12.6f}")
    print(f"{'mean':<15}{df['price'].mean():>12.6f}")
    print(f"{'std':<15}{df['price'].std():>12.6f}")
    print(f"{'median (50%)':<15}{df['price'].median():>12.6f}")
    print(f"{'min':<15}{df['price'].min():>12.6f}")
    print(f"{'25% (Q1)':<15}{df['price'].quantile(0.25):>12.6f}")
    print(f"{'50% (Q2)':<15}{df['price'].quantile(0.5):>12.6f}")
    print(f"{'75% (Q3)':<15}{df['price'].quantile(0.75):>12.6f}")
    print(f"{'max':<15}{df['price'].max():>12.6f}")

    # 📈 Graphique 1 : Boxplot
    flierprops = dict(
        marker='D',
        color='black',
        markerfacecolor='black',
        markersize=4,
        linestyle='none'
    )
    medianprops = dict(color='lightgreen', linewidth=1)
    boxplot(
        x=df["price"],
        flierprops=flierprops,
        medianprops=medianprops,
        linewidth=1,
        color="black"
    )
    plt.gca().set_facecolor("#f2f2f2")
    plt.grid(axis='x', color='white', linestyle='-', linewidth=1)
    plt.tick_params(axis='y', left=False, labelleft=False)
    plt.xlabel("Price")
    plt.tight_layout()
    plt.show()

    # 📈 Graphique 2 : same Boxplot without flier
    boxplot(
        x=df["price"],
        flierprops=None,
        medianprops=dict(color='grey', linewidth=1),
        linewidth=1,
        color="lightgreen",
        showfliers=False
    )
    plt.gca().set_facecolor("#f2f2f2")
    plt.grid(axis='x', color='white', linestyle='-', linewidth=1)
    plt.tick_params(axis='y', left=False, labelleft=False)
    plt.xlabel("Price")
    plt.tight_layout()
    plt.show()

    # 📈 Graphique 3 : Boxplot du prix moyen du panier par utilisateur (avec outliers filtrés)
    avg_basket_per_user = df.groupby("user_id")["price"].mean()
    # Calcul des bornes IQR pour retirer les valeurs trop éloignées (gros paniers aberrants)
    q1 = avg_basket_per_user.quantile(0.25)
    q3 = avg_basket_per_user.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Filtrage
    avg_filtered = avg_basket_per_user[
        (avg_basket_per_user >= lower_bound) & (avg_basket_per_user <= upper_bound)
    ]

    # Boxplot
    boxplot(
        x=avg_filtered,
        flierprops=flierprops,
        medianprops=dict(color='grey', linewidth=1),
        linewidth=1,
        color="lightblue"
    )
    plt.gca().set_facecolor("#f2f2f2")
    plt.grid(axis='x', color='white', linestyle='-', linewidth=1)
    plt.tick_params(axis='y', left=False, labelleft=False)
    plt.xlabel("Average basket price per user (filtered)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
