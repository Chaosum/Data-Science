from matplotlib import dates
import pandas as pd
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

    df = pd.read_sql(query, engine)
    df["event_time"] = pd.to_datetime(df["event_time"])
    df = df.set_index("event_time")

    # 📈 Graphique 1 : courbe du nombre de clients par jour
    customers_per_day = df.resample("D")["user_id"].nunique()
    plt.figure()
    customers_per_day.plot(
        figsize=(10, 4)
        )

    plt.gca().xaxis.set_major_locator(dates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%b'))
    plt.xlabel("")
    plt.ylabel("Number of customers")
    plt.grid(True)
    plt.tight_layout()

    # 📊 Graphique 2 : barres — total des ventes par mois en millions ₳
    monthly_df = df.resample("ME")["price"].sum() / 1_000_000
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

    # 🌈 Graphique 3 : courbe avec remplissage
    df["date"] = df.index.date
    daily_user_spend = df.groupby(["date", "user_id"])["price"].sum().reset_index()
    avg_basket_per_day = daily_user_spend.groupby("date")["price"].mean()
    avg_basket_per_day.index = pd.to_datetime(avg_basket_per_day.index)
    start = pd.to_datetime("2022-10-01")
    end = pd.to_datetime("2023-02-28")
    avg_basket_per_day = avg_basket_per_day.loc[start:end]
    plt.figure(figsize=(10, 4))
    plt.fill_between(avg_basket_per_day.index, avg_basket_per_day.values, alpha=0.4, color="steelblue")

    plt.xlim(start, end)
    plt.gca().xaxis.set_major_locator(dates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%b'))

    plt.ylabel("Average basket per user in ₳")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
