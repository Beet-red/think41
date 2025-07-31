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

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': error.description or 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
