from os import path
from csv import reader as csv_reader
from re import fullmatch
from psycopg2 import connect
from datetime import datetime
from tqdm import tqdm


def get_postgre_type(value):
    """Determine the type of a value for PostgreSQL.
    Returns a string representing the PostgreSQL type.
    """
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S %Z"):
        try:
            datetime.strptime(value, fmt)
            return 'TIMESTAMP'
        except Exception:
            continue
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return 'DATE'
    except Exception:
        pass
    try:
        num = int(value)
        if abs(num) > 2_147_483_647:
            return 'BIGINT'
        return 'INTEGER'
    except Exception:
        pass
    try:
        float(value)
        return 'NUMERIC(10, 2)'
    except Exception:
        pass
    if value.lower() in ['true', 'false']:
        return 'BOOLEAN'
    if fullmatch(
            r'[a-fA-F0-9]{8}-([a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}',
            value
            ):
        return 'UUID'
    if len(value) == 1:
        return 'CHAR(1)'
    if '@' in value and '.' in value:
        return 'VARCHAR(255)'
    if len(value) > 255:
        return 'TEXT'
    return 'VARCHAR(255)'


def get_column_types(sample_row):
    """Get the types of each column in a sample row.
    Returns a list of types corresponding to each column.
    """
    types = []
    for v in sample_row:
        types.append(get_postgre_type(v))
    return types


def ensure_n_types(types, n):
    """Ensure that there are at least n unique types in the list.
    If there are not enough unique types, replace some with predefined types.
    Returns a list of types with at least n unique types.
    """
    unique = set(types)
    if len(unique) >= n:
        return types

    replacements = {
        'INTEGER': 'BIGINT',
        'VARCHAR(255)': 'TEXT',
        'NUMERIC(10, 2)': 'FLOAT',
        'UUID': 'CHAR(36)'
    }

    updated_types = types.copy()
    type_encountered = set()
    for i, t in enumerate(updated_types):
        if len(set(updated_types)) >= n:
            break

        if t in type_encountered and t in replacements:
            updated_types[i] = replacements[t]
            unique = set(updated_types)
        else:
            type_encountered.add(t)

    return updated_types


def create_table_from_csv(csv_path, conn):
    """Create a PostgreSQL table from a CSV file.
    The table name is derived from the CSV file name.
    The columns are created based on the headers and sample row types.
    """
    table_name = "items"
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv_reader(f)
        headers = next(reader)
        sample_row = next(reader)
        types = get_column_types(sample_row)
        types = ensure_n_types(types, 3)

        columns = ', '.join([f'"{h}" {t}' for h, t in zip(headers, types)])
        create_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns});'
        with conn.cursor() as cur:
            print(f"Dropping table '{table_name}' if it exists...")
            cur.execute(f'DROP TABLE IF EXISTS "{table_name}";')
            print(f"Creating table '{table_name}'...")
            cur.execute(create_sql)
        conn.commit()


def add_values_to_table(csv_path, conn):
    """Insert values from a CSV file into a PostgreSQL table.
    The table name is derived from the CSV file name.
    The values are inserted row by row, with None for empty strings.
    """
    table_name = "items"

    # Compter les lignes (moins l'entête)
    with open(csv_path, newline='', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f) - 1

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv_reader(f)
        headers = next(reader)
        placeholders = ', '.join(['%s'] * len(headers))
        insert_sql = f'INSERT INTO "{table_name}" \
            ({", ".join(headers)}) VALUES ({placeholders});'

        with conn.cursor() as cur:
            for row in tqdm(
                reader, total=total_lines,
                desc=f"Inserting into {table_name}"
            ):
                cleaned_row = [v if v.strip() != '' else None for v in row]
                try:
                    cur.execute(insert_sql, cleaned_row)
                except Exception as e:
                    print(f"Error inserting row: {cleaned_row} {e}")
        conn.commit()


def main():
    """Main function to connect to PostgreSQL and process the CSV file.
    Connects to the database, creates a table from the CSV file,
    and inserts the values into the table.
    """
    postgre_connexion = {
        'host': 'localhost',
        'port': 5432,
        'dbname': 'piscineds',
        'user': 'mservage',
        'password': 'mysecretpassword'
    }
    csv_folder = "../item"
    # ** unpack the dictionary to pass as keyword arguments*
    # **postgre_connexion reviens a host=localhost, port=5432, ...
    conn = connect(**postgre_connexion)
    full_path = path.join(csv_folder, "item.csv")
    if not path.isfile(full_path):
        print("Erreur file doesn't exist")
        return
    create_table_from_csv(full_path, conn)
    add_values_to_table(full_path, conn)
    conn.close()


if __name__ == '__main__':
    main()
