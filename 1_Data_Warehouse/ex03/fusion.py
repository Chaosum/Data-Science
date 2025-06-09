from psycopg2 import connect


def main():
    """Merges data from the 'items' table into 'customers'.
    This function adds missing columns to 'customers' if they do not exist,
    then copies data from 'items' to 'customers' based on matching 'product_id'.
    The columns added are 'category_id', 'category_code', and 'brand'.
    """
    conn = connect(
        dbname="piscineds",
        user="mservage",  # remplace par ton login si besoin
        password="mysecretpassword",
        host="localhost"
    )
    cur = conn.cursor()

    print("Adding missing columns to 'customers'...")
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

    print("Fusion of data from 'items' into 'customers'...")
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
    print("Fusion successful: columns added and data copied.")


if __name__ == "__main__":
    main()
