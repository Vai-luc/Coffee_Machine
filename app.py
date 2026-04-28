from datetime import datetime
from flask import Flask, request, jsonify, render_template
from controllers import order_controller
from services.menu import Menu
from services import persistence
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__, static_folder='static', template_folder='templates')
menu = Menu()


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

    logging.info(f"Order attempt: drink={choice}, size={size}, quantity={quantity}, amount={amount_paid}")

    if not choice:
        logging.warning("Order failed: no drink selected")
        return jsonify({"status": "error", "message": "Choose a drink to continue."}), 400

    try:
        quantity = int(quantity)
        if quantity < 1 or quantity > 10:
            raise ValueError
    except (TypeError, ValueError):
        logging.warning(f"Order failed: invalid quantity {quantity}")
        return jsonify({"status": "error", "message": "Quantity must be a whole number between 1 and 10."}), 400

    try:
        amount_paid = float(amount_paid)
    except (TypeError, ValueError):
        logging.warning(f"Order failed: invalid payment amount {amount_paid}")
        return jsonify({"status": "error", "message": "Invalid payment amount."}), 400

    result = order_controller.process_order(choice, amount_paid=amount_paid, size=size, quantity=quantity)

    if result.get("status") == "error":
        logging.warning(f"Order failed: {result.get('message')}")
        return jsonify(result), 400

    logging.info(f"Order successful: {result['drink']} x{result['quantity']} - Total: ${result['total']}, Change: ${result['change']}")
    return jsonify({
        "status": "success",
        "drink": result["drink"],
        "size": result["size"],
        "quantity": result["quantity"],
        "total": result["total"],
        "change": result["change"],
        "resources": order_controller.coffee_maker.report(),
        "recent_orders": persistence.get_recent_orders(5)
    }), 200


@app.route("/session")
def session_summary():
    stats = persistence.get_order_stats()
    return jsonify({
        "status": "success",
        "orders": stats["orders"],
        "total_spent": stats["total_spent"],
        "recent_orders": persistence.get_recent_orders(5),
        "resources": order_controller.coffee_maker.report()
    })


if __name__ == "__main__":
    app.run(debug=True)
