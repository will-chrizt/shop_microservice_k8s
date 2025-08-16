# app.py for Cart Service
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple in-memory storage for carts (for demonstration purposes only)
# In a real application, use a database or Redis
carts = {}

@app.route('/carts/<string:user_id>', methods=['GET'])
def get_cart(user_id):
    """Returns the cart for a specific user."""
    cart = carts.get(user_id, [])
    return jsonify({"user_id": user_id, "items": cart})

@app.route('/carts/<string:user_id>', methods=['POST'])
def add_to_cart(user_id):
    """Adds an item to a user's cart."""
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({"message": "product_id is required"}), 400

    if user_id not in carts:
        carts[user_id] = []

    # Check if item already exists in cart and update quantity
    found = False
    for item in carts[user_id]:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            found = True
            break
    if not found:
        carts[user_id].append({"product_id": product_id, "quantity": quantity})

    return jsonify({"message": "Item added to cart", "cart": carts[user_id]}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes."""
    return jsonify({"status": "Cart Service is healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

