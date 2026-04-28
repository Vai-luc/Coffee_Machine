from datetime import datetime
from flask import Flask, request, jsonify, render_template
from controllers import order_controller
from services.menu import Menu
from services import persistence
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize database
try:
    menu = Menu()
    persistence.init_db()
    logging.info("Database initialized successfully")
except Exception as e:
    logging.warning(f"Database initialization warning: {e}")
    menu = Menu()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    logging.error(f"Server error: {error}")
    return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset():
    order_controller.reset_machine_state()
    return jsonify({"status": "success", "message": "Machine reset"})

@app.route("/menu")
def get_menu():
    return jsonify({
        "menu": menu.get_items(),
        "sizes": menu.sizes
    })

@app.route("/order", methods=["POST"])
def order():
    data = request.get_json() or {}
    choice = data.get("drink")
    size = data.get("size", "tall")
    quantity = data.get("quantity", 1)
    amount_paid = data.get("amount", 0)

    if not choice:
        return jsonify({"status": "error", "message": "Choose a drink to continue."}), 400

    try:
        quantity = int(quantity)
        if quantity < 1 or quantity > 10:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Quantity must be between 1 and 10."}), 400

    try:
        amount_paid = float(amount_paid)
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Invalid payment amount."}), 400

    result = order_controller.process_order(choice, amount_paid=amount_paid, size=size, quantity=quantity)

    if result.get("status") == "error":
        return jsonify(result), 400

    # Get current resources for UI
    resources = persistence.load_resources()
    
    return jsonify({
        "status": "success",
        "drink": result["drink"],
        "size": result["size"],
        "quantity": result["quantity"],
        "total": result["total"],
        "change": result["change"],
        "amount_paid": result["amount_paid"],
        "resources": {
            "water": resources["water"],
            "milk": resources["milk"],
            "coffee": resources["coffee"]
        },
        "recent_orders": persistence.get_recent_orders(5)
    }), 200

@app.route("/session")
def session_summary():
    stats = persistence.get_order_stats()
    resources = persistence.load_resources()
    return jsonify({
        "status": "success",
        "orders": stats["orders"],
        "total_spent": stats["total_spent"],
        "resources": {
            "water": resources["water"],
            "milk": resources["milk"],
            "coffee": resources["coffee"]
        },
        "recent_orders": persistence.get_recent_orders(5)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
