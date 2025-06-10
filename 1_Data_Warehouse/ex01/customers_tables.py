import psycopg2


def create_customers_table(conn):
    """
    Create a 'customers' table by merging data from existing tables.
    """
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

        print("Création index sur customers.product_id...")
        cur.execute(
            "CREATE INDEX IF NOT EXISTS " +
            "idx_customers_product_id ON customers(product_id);"
        )
        print("Ajout de l'index sur customers(event_time)...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_customers_event_time
            ON customers(event_time);
        """)
        print("Ajout de l'index sur customers...")
        cur.execute("""
            CREATE INDEX idx_event_type_product_price
            ON customers (event_type, product_id, price);
        """)
        conn.commit()
        print("Table 'customers' created and populated successfully.")


def main():
    """
    Main function to connect to PostgreSQL and create the 'customers' table.
    """
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
