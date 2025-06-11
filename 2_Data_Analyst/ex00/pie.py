from pandas import read_sql
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


def main():
    """Affiche un graphique circulaire de la répartition des activités
    des utilisateurs dans la table 'customers'.
    Le graphique montre la proportion de chaque type d'événement
    """
    engine = create_engine(
        "postgresql://mservage:mysecretpassword@localhost:5432/piscineds"
    )

    query = """
    SELECT event_type, COUNT(*) AS count
    FROM customers
    GROUP BY event_type;
    """

    df = read_sql(query, engine)
    plt.figure(figsize=(8, 8))
    plt.pie(
        df["count"], labels=df["event_type"],
        autopct='%1.1f%%',
        startangle=140
    )
    plt.title("Répartition des activités des utilisateurs")
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    main()
