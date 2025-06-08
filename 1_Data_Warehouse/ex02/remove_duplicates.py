from pandas import read_sql
from sqlalchemy import create_engine
from psycopg2 import connect
from os import remove


def main():
    """    Nettoyage des doublons dans la table 'customers' de PostgreSQL.
    Cette fonction lit les données de la table, supprime les doublons exacts,
    puis supprime les doublons basés sur les colonnes 'product_id','event_type'
    et 'event_time' si elles sont identiques à ±1 seconde.
    Les données nettoyées sont ensuite insérées dans la table 'customers' en
    utilisant la méthode COPY de psycopg2 pour une insertion efficace.
    """

    engine = create_engine(
        "postgresql://mservage:mysecretpassword@localhost:5432/piscineds"
    )

    print("Lecture de la table 'customers'...")
    df = read_sql("SELECT * FROM customers", engine)
    print(f"Lignes initiales : {len(df)}")

    df = df.drop_duplicates()

    df = df.sort_values("event_time").reset_index(drop=True)
    cols = [col for col in df.columns if col != "event_time"]
    same_values = (df[cols] == df[cols].shift(1)).all(axis=1)
    time_close = (
        df["event_time"] - df["event_time"].shift(1)
        ).dt.total_seconds().abs() <= 1
    mask = same_values & time_close
    removed = mask.sum()

    df = df[~mask].reset_index(drop=True)
    print(f"Lignes supprimées à ±1s : {removed}")
    print(f"Lignes finales : {len(df)}")
    df.to_csv("temp_customers.csv", index=False, header=False)
    with connect(
        host='localhost',
        port=5432,
        dbname='piscineds',
        user='mservage',
        password='mysecretpassword'
    ) as connexion:
        with connexion.cursor() as cur:
            print("TRUNCATE + COPY dans PostgreSQL...")
            cur.execute("TRUNCATE TABLE customers;")
            with open("temp_customers.csv", 'r', encoding='utf-8') as f:
                cur.copy_expert("""
                    COPY customers FROM STDIN WITH (FORMAT CSV, HEADER false)
                """, f)
            connexion.commit()
    remove("temp_customers.csv")
    print("✅ Données nettoyées et insérées avec succès.")


if __name__ == '__main__':
    main()
