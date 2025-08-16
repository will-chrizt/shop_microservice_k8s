# app.py for Product Service
from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": "1", "name": "Laptop", "price": 1200.00, "description": "Powerful laptop for all your needs."},
    {"id": "2", "name": "Mouse", "price": 25.00, "description": "Ergonomic wireless mouse."},
    {"id": "3", "name": "Keyboard", "price": 75.00, "description": "Mechanical gaming keyboard."},
    {"id": "4", "name": "Monitor", "price": 300.00, "description": "27-inch 4K monitor."},
]

@app.route('/products', methods=['GET'])
def get_products():
    """Returns a list of all products."""
    return jsonify(products)

@app.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    """Returns a single product by ID."""
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"message": "Product not found"}), 404

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes."""
    return jsonify({"status": "Product Service is healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

