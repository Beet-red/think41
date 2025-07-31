import psycopg2
from psycopg2 import sql
import pandas as pd

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 't41_db',
    'user': 'postgres',
    'password': 'admin',
    'port': 5432,
}

# Original CSV paths
CSV_PATHS = {
    'distribution_centers': 'C:/Project/think41/data/distribution_centers.csv',
    'products': 'C:/Project/think41/data/products_normalized.csv',  # Using normalized products CSV
    'inventory_items': 'C:/Project/think41/data/inventory_items.csv',
    'users': 'C:/Project/think41/data/users.csv',
    'orders': 'C:/Project/think41/data/orders.csv',
    'order_items': 'C:/Project/think41/data/order_items.csv',
}

# Paths for cleaned CSV files
CLEANED_USERS_CSV = 'C:/Project/think41/data/users_clean.csv'
CLEANED_ORDERS_CSV = 'C:/Project/think41/data/orders_clean.csv'
CLEANED_ORDER_ITEMS_CSV = 'C:/Project/think41/data/order_items_clean.csv'


def clean_users_csv():
    """
    Load users.csv, drop duplicate emails, and save to users_clean.csv.
    """
    print(f"Reading original users CSV from {CSV_PATHS['users']}...")
    df = pd.read_csv(CSV_PATHS['users'])
    print(f"Original users count: {len(df)}")

    df_clean = df.drop_duplicates(subset=['email'])
    print(f"Users count after dropping duplicates: {len(df_clean)}")

    df_clean.to_csv(CLEANED_USERS_CSV, index=False)
    print(f"Cleaned users CSV saved to {CLEANED_USERS_CSV}")


def clean_orders_csv(users_csv_path, orders_csv_path, output_orders_clean_path):
    """
    Filter orders.csv so that only orders with user_id present in users_clean.csv are kept.
    """
    print(f"Reading cleaned users CSV from {users_csv_path} for user ids...")
    users_df = pd.read_csv(users_csv_path)
    valid_user_ids = set(users_df['id'])
    print(f"Total users available: {len(valid_user_ids)}")

    print(f"Reading original orders CSV from {orders_csv_path}...")
    orders_df = pd.read_csv(orders_csv_path)
    print(f"Original orders count: {len(orders_df)}")

    orders_clean_df = orders_df[orders_df['user_id'].isin(valid_user_ids)]
    print(f"Orders count after filtering invalid user_ids: {len(orders_clean_df)}")

    orders_clean_df.to_csv(output_orders_clean_path, index=False)
    print(f"Cleaned orders CSV saved to {output_orders_clean_path}")


def clean_order_items_csv(users_csv_path, orders_csv_path, order_items_path, cleaned_order_items_path, expected_columns=11):
    """
    Filter order_items.csv to keep only rows whose user_id and order_id exist
    in cleaned users and cleaned orders CSV respectively.
    Also trims extra columns if any.
    """
    print(f"Reading cleaned users CSV from {users_csv_path} for user ids...")
    users_df = pd.read_csv(users_csv_path)
    valid_user_ids = set(users_df['id'])
    print(f"Total users available: {len(valid_user_ids)}")

    print(f"Reading cleaned orders CSV from {orders_csv_path} for order ids...")
    orders_df = pd.read_csv(orders_csv_path)
    valid_order_ids = set(orders_df['order_id'])
    print(f"Total orders available: {len(valid_order_ids)}")

    print(f"Reading original order_items CSV from {order_items_path}...")
    df = pd.read_csv(order_items_path)
    original_col_count = len(df.columns)
    print(f"Original order_items columns count: {original_col_count}")

    df_filtered = df[(df['user_id'].isin(valid_user_ids)) & (df['order_id'].isin(valid_order_ids))]

    if original_col_count > expected_columns:
        print(f"Trimming order_items CSV from {original_col_count} to {expected_columns} columns.")
        df_filtered = df_filtered.iloc[:, :expected_columns]

    print(f"order_items count after filtering invalid user_id/order_id: {len(df_filtered)}")
    df_filtered.to_csv(cleaned_order_items_path, index=False)
    print(f"Cleaned order_items CSV saved to {cleaned_order_items_path}")


def truncate_table(cursor, table_name):
    """
    Truncates the given table, resets identity sequences and cascades to dependent tables.
    """
    cursor.execute(sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE;").format(sql.Identifier(table_name)))
    print(f"Truncated table {table_name}")


# Mapping of table names to CSV file paths to load,
# Use cleaned CSVs for users, orders, and order_items
TABLE_CSV_MAP = {
    'distribution_centers': CSV_PATHS['distribution_centers'],
    'products': CSV_PATHS['products'],           # Using normalized products CSV
    'inventory_items': CSV_PATHS['inventory_items'],
    'users': CLEANED_USERS_CSV,
    'orders': CLEANED_ORDERS_CSV,
    'order_items': CLEANED_ORDER_ITEMS_CSV,
}


def load_csv_to_table(cursor, table_name, csv_file_path):
    """
    Loads a CSV file's data into the specified table using COPY.
    Assumes CSV header matches table columns exactly.
    """
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        next(f)  # Skip the header row
        print(f'Loading data from {csv_file_path} into {table_name}...')
        cursor.copy_expert(sql.SQL("""
            COPY {} FROM STDIN WITH CSV
        """).format(sql.Identifier(table_name)), f)
        print(f'Successfully loaded data from {csv_file_path} into {table_name}.')


def main():
    conn = None
    cursor = None
    try:
        # Step 1: Clean users CSV to remove duplicate emails
        clean_users_csv()

        # Step 2: Clean orders CSV to remove orders with invalid user_ids
        clean_orders_csv(CLEANED_USERS_CSV, CSV_PATHS['orders'], CLEANED_ORDERS_CSV)

        # Step 3: Clean order_items CSV to keep only valid user_id and order_id, trim extra columns
        clean_order_items_csv(CLEANED_USERS_CSV, CLEANED_ORDERS_CSV, CSV_PATHS['order_items'], CLEANED_ORDER_ITEMS_CSV, expected_columns=11)

        # Step 4: Connect to DB
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        cursor = conn.cursor()

        # Step 5: Truncate tables before loading to avoid duplicate key errors
        for table_name in TABLE_CSV_MAP.keys():
            truncate_table(cursor, table_name)

        # Step 6: Load CSV files to tables
        for table_name, csv_file in TABLE_CSV_MAP.items():
            load_csv_to_table(cursor, table_name, csv_file)

        conn.commit()
        print("All data loaded successfully!")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error occurred: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
