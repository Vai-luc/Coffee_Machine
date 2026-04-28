from flask import Flask, request, jsonify, render_template
from controllers import order_controller
from services.menu import Menu
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__, static_folder="static", template_folder="templates")
menu = Menu()

order_history = []
total_spent = 0.0

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reset", methods=["POST"])
def reset():
    global order_history, total_spent
    order_history = []
    total_spent = 0.0
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
    global order_history, total_spent
    data = request.get_json(silent=True) or {}
    choice = data.get("drink")
    size = data.get("size", "tall")
    quantity = int(data.get("quantity", 1))
    amount_paid = float(data.get("amount", 0))

    result = order_controller.process_order(
        choice,
        amount_paid=amount_paid,
        size=size,
        quantity=quantity
    )

    if result.get("status") == "success":
        order_history.append({
            "drink": choice,
            "size": size,
            "quantity": quantity,
            "amount": amount_paid
        })
        total_spent += amount_paid

    return jsonify(result)

@app.route("/session")
def session_summary():
    return jsonify({
        "status": "success",
        "orders": len(order_history),
        "total_spent": total_spent,
        "recent_orders": order_history[-5:]
    })

if __name__ == "__main__":
    app.run()
