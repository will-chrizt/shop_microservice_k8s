# app.py for Order Service
from flask import Flask, request, jsonify
import uuid
import datetime

app = Flask(__name__)

# Simple in-memory storage for orders
orders = []

@app.route('/orders', methods=['POST'])
def create_order():
    """Creates a new order."""
    data = request.json
    user_id = data.get('user_id')
    cart_items = data.get('items') # Expects a list of {"product_id": "...", "quantity": ...}

    if not user_id or not cart_items:
        return jsonify({"message": "user_id and items are required"}), 400

    order_id = str(uuid.uuid4())
    order_date = datetime.datetime.now().isoformat()
    total_amount = sum(item.get('price', 0) * item.get('quantity', 1) for item in cart_items) # Assuming price comes from the frontend or product service

    new_order = {
        "order_id": order_id,
        "user_id": user_id,
        "items": cart_items,
        "order_date": order_date,
        "total_amount": total_amount,
        "status": "pending"
    }
    orders.append(new_order)
    return jsonify({"message": "Order created successfully", "order": new_order}), 201

@app.route('/orders/<string:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Returns all orders for a specific user."""
    user_orders = [order for order in orders if order['user_id'] == user_id]
    return jsonify(user_orders)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes."""
    return jsonify({"status": "Order Service is healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)

