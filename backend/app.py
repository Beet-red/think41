from flask import Flask, jsonify, abort
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'dbname': 't41_db',
    'user': 'postgres',
    'password': 'admin',
    'port': 5432,
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# -------------------------------
# PRODUCTS ENDPOINTS
# -------------------------------

# GET /api/products (all products with department name)
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT p.id, p.cost, p.category, p.name, p.brand, p.retail_price,
                   d.name AS department_name, p.sku, p.distribution_center_id
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            ORDER BY p.id;
        """)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        products = [dict(zip(columns, row)) for row in rows]
    finally:
        cur.close()
        conn.close()
    return jsonify({'products': products})

# GET /api/products/<id> (single product with department name)
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT p.id, p.cost, p.category, p.name, p.brand, p.retail_price,
                   d.name AS department_name, p.sku, p.distribution_center_id
            FROM products p
            LEFT JOIN departments d ON p.department_id = d.id
            WHERE p.id = %s;
        """, (product_id,))
        row = cur.fetchone()
        if row is None:
            abort(404, description="Product not found")
        columns = [desc[0] for desc in cur.description]
        product = dict(zip(columns, row))
    finally:
        cur.close()
        conn.close()
    return jsonify(product)

# -------------------------------
# DEPARTMENT ENDPOINTS (Milestone 5)
# -------------------------------

# GET /api/departments (list all departments with product counts)
@app.route('/api/departments', methods=['GET'])
def get_departments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.id, d.name, COUNT(p.id) AS product_count
        FROM departments d
        LEFT JOIN products p ON p.department_id = d.id
        GROUP BY d.id, d.name
        ORDER BY d.id
    """)
    departments = [
        {"id": row[0], "name": row[1], "product_count": row[2]}
        for row in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return jsonify({"departments": departments})

# GET /api/departments/<id> (get department details)
@app.route('/api/departments/<int:dept_id>', methods=['GET'])
def get_department(dept_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name FROM departments WHERE id = %s", (dept_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"error": "Department not found"}), 404
    return jsonify({"id": row[0], "name": row[1]})

# GET /api/departments/<id>/products (products in this department)
@app.route('/api/departments/<int:dept_id>/products', methods=['GET'])
def get_department_products(dept_id):
    conn = get_db_connection()
    cur = conn.cursor()
    # First, get department name (for pretty JSON key)
    cur.execute(
        "SELECT name FROM departments WHERE id = %s", (dept_id,)
    )
    dept_row = cur.fetchone()
    if not dept_row:
        cur.close()
        conn.close()
        return jsonify({"error": "Department not found"}), 404
    department_name = dept_row[0]
    # Now, get products in this department
    cur.execute(
        """
        SELECT p.id, p.cost, p.category, p.name, p.brand, p.retail_price,
               p.sku, p.distribution_center_id
        FROM products p
        WHERE p.department_id = %s
        ORDER BY p.id
        """,
        (dept_id,)
    )
    products = [
        {
            "id": row[0],
            "cost": row[1],
            "category": row[2],
            "name": row[3],
            "brand": row[4],
            "retail_price": row[5],
            "sku": row[6],
            "distribution_center_id": row[7],
        }
        for row in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return jsonify({"department": department_name, "products": products})

# -------------------------------
# ERROR HANDLERS
# -------------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': error.description or 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
