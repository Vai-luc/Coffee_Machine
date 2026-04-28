from flask import Flask, request, jsonify, render_template
from controllers import order_controller
from [services.menu](http://services.menu) import Menu
import logging
logging.basicConfig(
    level=[logging.INFO](http://logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s"
)
app = Flask(__name__, static_folder="static", template_folder="templates")
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
    return jsonify(result)
@app.route("/session")
def session_summary():
    return jsonify({
        "status": "success",
        "orders": 0,
        "total_spent": 0,
        "recent_orders": []
    })
if __name__ == "__main__":
    [app.run](http://app.run)()
 "site is live just one issue my order history suppy tracker isnt working
