from datetime import datetime
from flask import Flask, request, jsonify, render_template
from controllers import order_controller
from services.menu import Menu
#from services import persistence
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
        return jsonify({"status": "error", "message": "Quantity must be 1 to 10."}), 400

    try:
        amount_paid = float(amount_paid)
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Invalid payment amount."}), 400

    result = order_controller.process_order(
        choice,
        amount_paid=amount_paid,
        size=size,
        quantity=quantity
    )

    if result.get("status") == "error":
        return jsonify(result), 400

    return jsonify({
        "status": "success",
        "drink": result["drink"],
        "size": result["size"],
        "quantity": result["quantity"],
        "total": result["total"],
        "change": result["change"],
        "resources": order_controller.coffee_maker.report(),
        "recent_orders": []
    }), 200


@app.route("/session")
def session_summary():
    return jsonify({
        "status": "success",
        "orders": 0,
        "total_spent": 0,
        "recent_orders": [],
        "resources": order_controller.coffee_maker.report()
    })


if __name__ == "__main__":
    app.run(debug=True)
