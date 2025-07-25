from os import listdir, path
from csv import reader as csv_reader
import re
from psycopg2 import connect
from datetime import datetime


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
    if re.fullmatch(
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
            cur.execute(f'DROP TABLE IF EXISTS "{table_name}";')
            cur.execute(create_sql)
        conn.commit()


def main():
    try:
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
            break  # according to the subject, we only need to process one CSV file
        conn.close()
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
