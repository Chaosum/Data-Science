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

    # 📈 Graphique 2 : IQR

    prices = df["price"].dropna()

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.boxplot(
        prices,
        vert=False,
        showfliers=False,
        patch_artist=True,
        boxprops=dict(facecolor='mediumseagreen', edgecolor='black'),
        medianprops=dict(color='black', linewidth=1),
        whiskerprops=dict(color='black'),
        capprops=dict(color='black')
    )

    ax.set_xlim(-0.5, 13)
    ax.set_facecolor("#f2f2f2")
    ax.grid(axis='x', color='white', linestyle='-', linewidth=1)
    ax.tick_params(axis='x', bottom=True, labelbottom=True)
    ax.tick_params(axis='y', left=False, labelleft=False)
    ax.set_xlabel("Price")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
