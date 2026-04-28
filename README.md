# Daily Brew — Coffeehouse Ordering 

A polished Flask-based ordering experience built as an entry-level portfolio project. The app demonstrates a clean separation between backend APIs and a responsive frontend with live pricing, drink customization, order history, and resource tracking.

## Features

- Modern coffeehouse-inspired UI with dark green / cream palette
- Drink selection with descriptions and placeholder drink accents
- Size options: Tall, Grande, Venti
- Quantity selection with validation
- Live item and order total updates
- JSON API endpoints for menu, orders, session, and reset
- Persistent order history stored in SQLite across app restarts
- Resource tracker for water, milk, and coffee ingredients
- Mobile-first responsive layout with accessibility support

## Project structure

- `app.py` — Flask app entry point and REST endpoints
- `controllers/order_controller.py` — business logic for order validation and processing
- `services/menu.py` — menu data, drink metadata, and size multipliers
- `services/coffee_maker.py` — resource tracking and inventory logic
- `services/money_machine.py` — payment validation
- `templates/index.html` — app shell and frontend entrypoint
- `static/css/styles.css` — responsive theme and coffeehouse-inspired UI styling
- `static/js/app.js` — modular frontend logic, API integration, and state management

## How to run

### Local Development

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Run the app:

   ```powershell
   python app.py
   ```

4. Open your browser at `http://127.0.0.1:5000`

### Using Docker

1. Build the Docker image:

   ```bash
   docker build -t coffee-machine .
   ```

2. Run the container:

   ```bash
   docker run -p 5000:5000 coffee-machine
   ```

3. Open your browser at `http://127.0.0.1:5000`

### Testing

Run the test suite:

```bash
pytest tests/
```

Or run API tests manually:

```bash
python test_api.py
```

## Run tests

```powershell
pytest
```

## Backend architecture

- `app.py` exposes a lightweight API for frontend integration
- `/menu` returns drink and size metadata
- `/order` accepts JSON payloads with `drink`, `size`, `quantity`, and `amount`
- `/session` returns current order counts, persistent recent orders, and resource state
- Order history and resources are persisted to SQLite for demo durability

## Frontend architecture

- Semantic HTML structure with `main`, `section`, `aside`, and ARIA labels
- CSS variables and responsive grid layout for mobile-first design
- `static/js/app.js` handles menu loading, order state, live pricing, and order submission
- Minimal dependency approach: vanilla JS with fetch API

## Notes for interview discussions

- The app is intentionally kept simple and maintainable
- Backend logic is separated into controllers and services for testability
- The frontend communicates using JSON, making the app integration-ready
- The project is a strong portfolio example because it demonstrates UI polish, API-driven interaction, and clean structure

## Related portfolio work

This project pairs well with a standalone Python graphics demo such as a `turtle` sporograph. Use the coffee ordering app to show web application design, API integration, and responsive UI, while the turtle sporograph can showcase algorithmic creativity and Python scripting skills.

Suggested talking points:

- The coffee app demonstrates system design, frontend/backend separation, and real-world order handling.
- The sporograph highlights problem solving, creative code, and familiarity with Python standard libraries.
- Together they form a balanced portfolio narrative for both UI-driven and algorithmic Python work.
