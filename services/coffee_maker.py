class CoffeeMaker:
    """Models the machine that makes the coffee"""

    def __init__(self, resources=None):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }
        if resources is not None:
            self.resources.update(resources)

    def report(self):
        return {
            "water": self.resources["water"],
            "milk": self.resources["milk"],
            "coffee": self.resources["coffee"]
        }

    def is_resource_sufficient(self, drink, quantity=1):
        for item, required in drink.ingredients.items():
            if required * quantity > self.resources.get(item, 0):
                return False
        return True

    def make_coffee(self, order, quantity=1):
        for item, required in order.ingredients.items():
            self.resources[item] -= required * quantity
