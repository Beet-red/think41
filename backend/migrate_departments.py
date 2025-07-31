import pandas as pd
import psycopg2

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'dbname': 't41_db',
    'user': 'postgres',
    'password': 'admin',
    'port': 5432,
}

PRODUCTS_CSV = '../data/products.csv'                   # path to your input products.csv
OUTPUT_PRODUCTS_CSV = '../data/products_normalized.csv' # path for output products with department_id

def main():
    # Step 1: Read products.csv
    print("Reading products CSV...")
    products_df = pd.read_csv(PRODUCTS_CSV)

    # Step 2: Extract unique departments from CSV
    unique_departments = products_df['department'].dropna().unique()
    print(f"Found {len(unique_departments)} unique departments:", unique_departments)
    department_map = {}

    # Step 3: Connect to DB and insert departments
    print("Connecting to database...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # To avoid duplicates/deadlocks on repeated runs, get existing departments first
    cur.execute('SELECT id, name FROM departments')
    existing = dict(cur.fetchall())

    # Insert new departments, skip if exists
    for dept in unique_departments:
        if dept in existing.values():
            # Find the id of the existing department name
            dept_id = [k for k, v in existing.items() if v == dept][0]
            department_map[dept] = dept_id
            continue
        cur.execute('INSERT INTO departments (name) VALUES (%s) RETURNING id;', (dept,))
        dept_id = cur.fetchone()[0]
        department_map[dept] = dept_id
        print(f"Inserted department: {dept} (id={dept_id})")

    conn.commit()
    print("Departments table updated.")

    # Step 4: Map department name in products_df to department_id
    products_df['department_id'] = products_df['department'].map(department_map)
    products_df = products_df.drop(columns=['department'])

    # Step 5: Save new products CSV
    products_df.to_csv(OUTPUT_PRODUCTS_CSV, index=False)
    print(f"New normalized products CSV with department_id saved to {OUTPUT_PRODUCTS_CSV}")

    # Optional: update existing products table if required
    # for idx, row in products_df.iterrows():
    #     cur.execute(
    #         "UPDATE products SET department_id=%s WHERE id=%s",
    #         (int(row['department_id']), int(row['id']))
    #     )
    # conn.commit()
    # print("Products table updated with department_id.")

    cur.close()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    main()
