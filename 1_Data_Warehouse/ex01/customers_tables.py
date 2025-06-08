import psycopg2


def create_customers_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT tablename FROM pg_tables
            WHERE tablename LIKE 'data_202%' AND schemaname = 'public';
        """)
        tables = [row[0] for row in cur.fetchall()]

        if not tables:
            print("No table to merge found.")
            return

        print(
            f"Creating 'customers' table from the structure of '{tables[0]}'"
        )
        cur.execute('DROP TABLE IF EXISTS customers;')
        cur.execute(
            f'CREATE TABLE customers AS TABLE "{tables[0]}" WITH NO DATA;'
        )

        for table in tables:
            print(f"Inserting data from {table}...")
            cur.execute(f'INSERT INTO customers SELECT * FROM "{table}";')

        conn.commit()
        print("Table 'customers' created and populated successfully.")


def main():

    # Connexion à la base de données PostgreSQL
    postgre_connexion = {
        'host': 'localhost',
        'port': 5432,
        'dbname': 'piscineds',
        'user': 'mservage',
        'password': 'mysecretpassword'
    }
    try:
        connexion = psycopg2.connect(**postgre_connexion)
        create_customers_table(connexion)

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == '__main__':
    main()
