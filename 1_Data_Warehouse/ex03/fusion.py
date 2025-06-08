from psycopg2 import connect


def main():
    """Fusion des données de la table 'items' dans 'customers'.
    Cette fonction ajoute les colonnes manquantes dans 'customers'
    si elles n'existent pas,
    puis copie les données de 'items' dans 'customers' en fonction
    de la correspondance
    des 'product_id'. Les colonnes ajoutées sont 'category_id',
    'category_code' et 'brand'.
    """
    conn = connect(
        dbname="piscineds",
        user="mservage",  # remplace par ton login si besoin
        password="mysecretpassword",
        host="localhost"
    )
    cur = conn.cursor()

    print("Ajout des colonnes manquantes dans 'customers'...")
    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                            WHERE table_name='customers'
                            AND column_name='category_id') THEN
                ALTER TABLE customers ADD COLUMN category_id BIGINT;
            END IF;
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                           WHERE table_name='customers'
                           AND column_name='category_code') THEN
                ALTER TABLE customers ADD COLUMN category_code VARCHAR;
            END IF;
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                            WHERE table_name='customers'
                            AND column_name='brand') THEN
                ALTER TABLE customers ADD COLUMN brand VARCHAR;
            END IF;
        END
        $$;
    """)

    print("Fusion des données depuis 'items' dans 'customers'...")
    cur.execute("""
        UPDATE customers
        SET category_id = items.category_id,
            category_code = items.category_code,
            brand = items.brand
        FROM items
        WHERE customers.product_id = items.product_id;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Fusion réussie : colonnes ajoutées et données copiées.")


if __name__ == "__main__":
    main()
