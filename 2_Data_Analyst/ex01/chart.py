from matplotlib import dates
from pandas import isna, read_sql, to_datetime
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


def main():
    """Affiche un graphique circulaire de la répartition des activités
    des utilisateurs dans la table 'customers'.
    """
    engine = create_engine(
        "postgresql://mservage:mysecretpassword@localhost:5432/piscineds"
    )
    query = """
    SELECT event_time, user_id, product_id, price
    FROM customers
    WHERE event_type = 'purchase'
    AND product_id IS NOT NULL
    AND price IS NOT NULL
    AND event_time BETWEEN '2022-10-01' AND '2023-02-28';
    """

    df = read_sql(query, engine)
    df["event_time"] = to_datetime(df["event_time"])
    df = df.set_index("event_time")

    # 📈 Graphique 1 : courbe du nombre de clients par jour
    customers_per_day = df.resample("D")["user_id"].nunique()
    plt.figure()
    customers_per_day.plot(
        figsize=(10, 4)
        )

    # Remplace %b sur tous les jours par une tick par mois
    plt.gca().xaxis.set_major_locator(dates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%b'))
    plt.xlabel("")
    plt.ylabel("Number of customers")
    plt.grid(True)
    plt.tight_layout()

    # 📊 Graphique 2 : barres — total des ventes par mois en millions ₳
    monthly_df = df.resample("ME")["price"].sum() / 1_000_000

    # On crée un DataFrame pour pouvoir relabel proprement
    monthly_df.index = monthly_df.index.strftime('%b')  # 'Oct', 'Nov', ...

    plt.figure()
    monthly_df.plot(
        kind="bar",
        figsize=(10, 4)
    )
    plt.xlabel("Month")
    plt.ylabel("Total sales in million of ₳")
    plt.grid(axis="y")
    plt.tight_layout()

    # 🌈 Graphique 3 : courbe avec remplissage — prix moyen par jour
    start = to_datetime("2022-10-01")
    end = to_datetime("2023-02-28")

    # 1. Resample
    avg_price_per_day = df.resample("D")["price"].mean()

    # 2. Troncature stricte à gauche et à droite
    avg_price_per_day = avg_price_per_day.loc[
        (avg_price_per_day.index >= start) & (avg_price_per_day.index <= end)
    ]

    # 3. Tracé
    plt.figure(figsize=(10, 4))
    plt.fill_between(
        avg_price_per_day.index,
        avg_price_per_day.values,
        where=~isna(avg_price_per_day.values),
        interpolate=True,
        alpha=0.4,
        color="steelblue"
    )

    # 4. Axe X — MAINTENANT on verrouille
    plt.xlim(start, end)

    # 5. Mois bien formatés
    plt.gca().xaxis.set_major_locator(dates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%b'))
    plt.xlim(start, to_datetime("2023-02-26 23:59:59"))

    plt.ylabel("Average spend/customers in ₳")
    plt.grid(True)
    plt.tight_layout()

    # Affichage de tous les graphiques
    plt.show()


if __name__ == "__main__":
    main()
