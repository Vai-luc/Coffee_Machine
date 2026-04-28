from controllers.order_controller import process_order
from services.menu import Menu

menu = Menu()

def main():
    is_on = True

    while is_on:
        try:
            choice = input(f"What would you like? ({menu.get_items()}): ").strip().lower()

            if not choice:
                print("Please enter a valid option.")
                continue

            if choice == "off":
                print("Shutting down...")
                break

            result = process_order(choice)

            if not isinstance(result, dict):
                print("Unexpected response format.")
                continue

            if "error" in result:
                print(result["error"])

            elif "message" in result:
                print(result["message"])

            elif "coffee" in result:
                coffee = result["coffee"]
                print(f"Water: {coffee['water']}ml")
                print(f"Milk: {coffee['milk']}ml")
                print(f"Coffee: {coffee['coffee']}g")
                print(f"Money: ${result['money']}")

            else:
                print("Unknown response:", result)

        except (KeyboardInterrupt, EOFError):
            print("\nProgram interrupted. Exiting safely.")
            break

        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()