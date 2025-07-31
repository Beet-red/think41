from flask import Flask, jsonify, request, abort
import psycopg2
import os

app = Flask(__name__)

# You may want to load these from environment variables in production
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
    """List products with optional pagination."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Get total number of products (for pagination info)
        cur.execute('SELECT COUNT(*) FROM products')
        total = cur.fetchone()[0]
        
        cur.execute('SELECT * FROM products ORDER BY id LIMIT %s OFFSET %s', (per_page, offset))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        products = [dict(zip(columns, row)) for row in rows]
    finally:
        cur.close()
        conn.close()

    return jsonify({
        'products': products,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': -(-total // per_page)  # ceiling division
        }
    })

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Fetch a product by ID."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
        row = cur.fetchone()
        if not row:
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
