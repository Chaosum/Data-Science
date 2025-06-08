from os import listdir, path
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


def ensure_six_types(types):
    """Ensure that the list of types contains at least six unique types.
    If there are fewer than six unique types, replace some types
    with predefined types to ensure diversity.
    Returns a list of types with at least six unique types.
    """
    unique = set(types)
    if len(unique) >= 6:
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
        if len(set(updated_types)) >= 6:
            break

        if t in type_encountered and t in replacements:
            updated_types[i] = replacements[t]
            unique = set(updated_types)
        else:
            type_encountered.add(t)

    return updated_types


def create_table_from_csv(csv_path, conn):
    """Create a PostgreSQL table from a CSV file.
    Drops the table if it exists and creates a \
    new one based on the CSV headers.
    """
    table_name = path.splitext(path.basename(csv_path))[0]
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv_reader(f)
        headers = next(reader)
        sample_row = next(reader)
        types = get_column_types(sample_row)
        types = ensure_six_types(types)

        columns = ', '.join([f'"{h}" {t}' for h, t in zip(headers, types)])
        create_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns});'
        with conn.cursor() as cur:
            print(f"Dropping table '{table_name}' if it exists...")
            cur.execute(f'DROP TABLE IF EXISTS "{table_name}";')
            print(f"Creating table '{table_name}'...")
            cur.execute(create_sql)
        conn.commit()


def add_values_to_table(csv_path, conn):
    """
Inserts data from a CSV file into a PostgreSQL table.
The table name is inferred from the CSV file name (without extension).
Assumes the table already exists in the database and matches the CSV structure.
Skips the header row of the CSV file.
Args:
    csv_path (str): Path to the CSV file containing the data to insert.
    conn (psycopg2.connection): Active connection to the PostgreSQL database.
Raises:
    psycopg2.DatabaseError: If an error occurs during the database operation.
    FileNotFoundError: If the specified CSV file does not exist.
    """

    table_name = path.splitext(path.basename(csv_path))[0]
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            next(f)  # skip header
            with conn.cursor() as cur:
                cur.copy_expert(f"""
                    COPY "{table_name}" \
    FROM STDIN WITH (FORMAT csv, HEADER false, NULL '', DELIMITER ',')
                """, f)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function to process CSV files and create PostgreSQL tables.
    Connects to PostgreSQL, reads CSV files from a folder,
    creates tables, and inserts values.
    """
    postgre_connexion = {
        'host': 'localhost',
        'port': 5432,
        'dbname': 'piscineds',
        'user': 'mservage',
        'password': 'mysecretpassword'
    }
    csv_folder = '../customer'
    # ** unpack the dictionary to pass as keyword arguments*
    # **postgre_connexion reviens a host=localhost, port=5432, ...
    conn = connect(**postgre_connexion)
    for file in listdir(csv_folder):
        full_path = path.join(csv_folder, file)
        if not path.isfile(full_path) or not file.endswith('.csv'):
            continue
        create_table_from_csv(full_path, conn)
        add_values_to_table(full_path, conn)
    conn.close()


if __name__ == '__main__':
    main()
