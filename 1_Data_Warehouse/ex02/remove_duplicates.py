from pandas import read_sql
from sqlalchemy import create_engine
from psycopg2 import connect
from os import remove


def main():
    """Remove duplicates from the 'customers' table in PostgreSQL.
    It reads the data,
    removes duplicates based on 'event_time' and other columns,
    and then writes the cleaned data back to the table.
    The script assumes that the 'event_time' column is in datetime format.
    """

    engine = create_engine(
        "postgresql://mservage:mysecretpassword@localhost:5432/piscineds"
    )

    print("Reading data from customers table...")
    query = """
    SELECT *
    FROM customers
    """
    df = read_sql(query, engine)
    print(f"Initial rows: {len(df)}")

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
    print(f"Rows removed within ±1s: {removed}")
    print(f"Final rows: {len(df)}")
    df.to_csv("temp_customers.csv", index=False, header=False)
    with connect(
        host='localhost',
        port=5432,
        dbname='piscineds',
        user='mservage',
        password='mysecretpassword'
    ) as connexion:
        with connexion.cursor() as cur:
            print("TRUNCATE + COPY into PostgreSQL...")
            cur.execute("TRUNCATE TABLE customers;")
            with open("temp_customers.csv", 'r', encoding='utf-8') as f:
                cur.copy_expert("""
                    COPY customers FROM STDIN WITH (FORMAT CSV, HEADER false)
                """, f)
            connexion.commit()
    remove("temp_customers.csv")
    print("✅ Data cleaned and inserted successfully.")


if __name__ == '__main__':
    main()
