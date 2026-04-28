class MenuItem:
    def __init__(self, name, display_name, water, milk, coffee, cost, description, accent):
        self.name = name
        self.display_name = display_name
        self.cost = cost
        self.description = description
        self.accent = accent
        self.ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee
        }


class Menu:
    sizes = [
        {"key": "tall", "label": "Tall", "multiplier": 1.0},
        {"key": "grande", "label": "Grande", "multiplier": 1.25},
        {"key": "venti", "label": "Venti", "multiplier": 1.5},
    ]

    def __init__(self):
        self.menu = [
            MenuItem(
                name="latte",
                display_name="Latte",
                water=200,
                milk=150,
                coffee=24,
                cost=3.25,
                description="Smooth espresso finished with steamed milk and a velvety foam.",
                accent="latte"
            ),
            MenuItem(
                name="espresso",
                display_name="Espresso",
                water=50,
                milk=0,
                coffee=18,
                cost=2.25,
                description="Bold espresso shot with a rich crema and caramel notes.",
                accent="espresso"
            ),
            MenuItem(
                name="cappuccino",
                display_name="Cappuccino",
                water=250,
                milk=50,
                coffee=24,
                cost=3.75,
                description="Classic cappuccino layered with espresso, steamed milk and foam.",
                accent="cappuccino"
            ),
        ]

    def get_items(self):
        return [
            {
                "id": item.name,
                "name": item.display_name,
                "base_cost": item.cost,
                "description": item.description,
                "accent": item.accent,
                "ingredients": item.ingredients
            }
            for item in self.menu
        ]

    def find_drink(self, order_name):
        for item in self.menu:
            if item.name == order_name:
                return item
        return None

    def get_size_multiplier(self, size_key):
        normalized = size_key.lower()
        for option in self.sizes:
            if option["key"] == normalized:
                return option["multiplier"]
        return None
