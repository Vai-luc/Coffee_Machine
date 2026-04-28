from datetime import datetime
from services import persistence
from services.menu import Menu
from services.coffee_maker import CoffeeMaker
from services.money_machine import MoneyMachine

persistence.init_db()
menu = Menu()
initial_state = persistence.load_resources()
coffee_maker = CoffeeMaker(resources={
    "water": initial_state["water"],
    "milk": initial_state["milk"],
    "coffee": initial_state["coffee"]
})
money_machine = MoneyMachine(profit=initial_state["profit"])


def reset_machine_state():
    persistence.reset_db()
    resources = persistence.load_resources()
    coffee_maker.__init__(resources={
        "water": resources["water"],
        "milk": resources["milk"],
        "coffee": resources["coffee"]
    })
    money_machine.__init__(profit=resources["profit"])


def process_order(choice, amount_paid=0, size='tall', quantity=1):
    if choice == "report":
        return {
            "status": "success",
            "coffee": coffee_maker.report(),
            "money": money_machine.report()
        }

    drink = menu.find_drink(choice)
    if not drink:
        return {
            "status": "error",
            "message": "Invalid drink selection."
        }

    size_multiplier = menu.get_size_multiplier(size)
    if size_multiplier is None:
        return {
            "status": "error",
            "message": "Invalid size selection."
        }

    if not coffee_maker.is_resource_sufficient(drink, quantity):
        return {
            "status": "error",
            "message": "Insufficient resources for this order."
        }

    total_cost = round(drink.cost * size_multiplier * quantity, 2)

    if amount_paid < total_cost:
        return {
            "status": "error",
            "message": "Insufficient payment. Add more to complete the order.",
            "amount_paid": amount_paid,
            "amount_due": round(total_cost - amount_paid, 2),
            "total": total_cost
        }

    if not money_machine.make_payment(total_cost, amount_paid):
        return {
            "status": "error",
            "message": "Invalid payment amount.",
            "amount_paid": amount_paid,
            "total": total_cost
        }

    coffee_maker.make_coffee(drink, quantity)
    order_record = {
        "drink": choice,
        "size": size,
        "quantity": quantity,
        "total": total_cost,
        "change": round(amount_paid - total_cost, 2),
        "amount_paid": amount_paid,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    persistence.save_order(order_record)
    persistence.save_resources(coffee_maker.report(), money_machine.report())

    return {
        "status": "success",
        "drink": choice,
        "size": size,
        "quantity": quantity,
        "total": total_cost,
        "amount_paid": amount_paid,
        "change": order_record["change"]
    }
