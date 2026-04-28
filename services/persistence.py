import os
import json
from pathlib import Path

# Try PostgreSQL first, fallback to JSON file for local development
DATABASE_URL = os.environ.get("DATABASE_URL")
USE_DB = DATABASE_URL is not None

if USE_DB:
    import psycopg2
    from psycopg2.extras import RealDictCursor

DATA_FILE = Path(__file__).parent.parent / "data" / "coffee_machine.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def _get_data():
    """Load data from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"resources": {"water": 300, "milk": 200, "coffee": 100, "profit": 0}, "orders": []}


def _save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def _connect():
    if USE_DB:
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return None


def init_db():
    """Initialize database"""
    if USE_DB:
        try:
            conn = _connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS resources (
                            id INTEGER PRIMARY KEY,
                            water INTEGER NOT NULL,
                            milk INTEGER NOT NULL,
                            coffee INTEGER NOT NULL,
                            profit REAL NOT NULL
                        )
                    ''')
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS orders (
                            id SERIAL PRIMARY KEY,
                            drink TEXT NOT NULL,
                            size TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            total REAL NOT NULL,
                            change REAL NOT NULL,
                            amount_paid REAL NOT NULL,
                            timestamp TEXT NOT NULL
                        )
                    ''')
                    cursor.execute('''
                        INSERT INTO resources (id, water, milk, coffee, profit)
                        VALUES (1, 300, 200, 100, 0)
                        ON CONFLICT (id) DO NOTHING
                    ''')
                conn.commit()
        except Exception as e:
            print(f"Database init error: {e}. Using JSON storage.")
    else:
        # Initialize JSON file if needed
        if not DATA_FILE.exists():
            _save_data({
                "resources": {"water": 300, "milk": 200, "coffee": 100, "profit": 0},
                "orders": []
            })


def load_resources():
    """Load resources from database or file"""
    if USE_DB:
        try:
            conn = _connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT water, milk, coffee, profit FROM resources WHERE id = 1')
                    row = cursor.fetchone()
                    if row is None:
                        return {'water': 300, 'milk': 200, 'coffee': 100, 'profit': 0}
                    return dict(row)
        except Exception:
            pass
    
    # Fallback to JSON
    data = _get_data()
    return data.get("resources", {'water': 300, 'milk': 200, 'coffee': 100, 'profit': 0})


def save_resources(resources, profit):
    """Save resources to database or file"""
    if USE_DB:
        try:
            conn = _connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        'UPDATE resources SET water = %s, milk = %s, coffee = %s, profit = %s WHERE id = 1',
                        (resources['water'], resources['milk'], resources['coffee'], profit)
                    )
                conn.commit()
            return
        except Exception:
            pass
    
    # Fallback to JSON
    data = _get_data()
    data["resources"] = {"water": resources['water'], "milk": resources['milk'], "coffee": resources['coffee'], "profit": profit}
    _save_data(data)


def save_order(order):
    """Save order to database or file"""
    if USE_DB:
        try:
            conn = _connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('''
                        INSERT INTO orders (drink, size, quantity, total, change, amount_paid, timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        order['drink'],
                        order['size'],
                        order['quantity'],
                        order['total'],
                        order['change'],
                        order['amount_paid'],
                        order['timestamp']
                    ))
                conn.commit()
            return
        except Exception:
            pass
    
    # Fallback to JSON
    data = _get_data()
    data["orders"].append(order)
    _save_data(data)


def get_recent_orders(limit=5):
    """Get recent orders from database or file"""
    if USE_DB:
        try:
            conn = _connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        'SELECT drink, size, quantity, total, change, amount_paid, timestamp FROM orders ORDER BY id DESC LIMIT %s',
                        (limit,)
                    )
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception:
            pass
    
    # Fallback to JSON
    data = _get_data()
    orders = data.get("orders", [])
    return sorted(orders, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]


def get_order_stats():
    """Get order statistics from database or file"""
    if USE_DB:
        try:
            conn = _connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT COUNT(*), SUM(total) FROM orders')
                    row = cursor.fetchone()
                    return {
                        'orders': int(row['count'] or 0),
                        'total_spent': round(float(row['sum'] or 0), 2)
                    }
        except Exception:
            pass
    
    # Fallback to JSON
    data = _get_data()
    orders = data.get("orders", [])
    total = sum(float(o.get('total', 0)) for o in orders)
    return {
        'orders': len(orders),
        'total_spent': round(total, 2)
            }


def reset_db():
    """Reset database or file"""
    if USE_DB:
        try:
            conn = _connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM orders')
                    cursor.execute('UPDATE resources SET water = 300, milk = 200, coffee = 100, profit = 0 WHERE id = 1')
                conn.commit()
            return
        except Exception:
            pass
    
    # Fallback to JSON
    _save_data({
        "resources": {"water": 300, "milk": 200, "coffee": 100, "profit": 0},
        "orders": []
    })
