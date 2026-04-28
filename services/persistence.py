import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / 'data'
DB_PATH = DB_DIR / 'coffee.db'


def _connect():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY,
                water INTEGER NOT NULL,
                milk INTEGER NOT NULL,
                coffee INTEGER NOT NULL,
                profit REAL NOT NULL
            )
            '''
        )
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drink TEXT NOT NULL,
                size TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total REAL NOT NULL,
                change REAL NOT NULL,
                amount_paid REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
            '''
        )
        cursor.execute(
            'INSERT OR IGNORE INTO resources (id, water, milk, coffee, profit) VALUES (1, 300, 200, 100, 0)'
        )
        conn.commit()


def load_resources():
    with _connect() as conn:
        row = conn.execute('SELECT water, milk, coffee, profit FROM resources WHERE id = 1').fetchone()
        if row is None:
            return {'water': 300, 'milk': 200, 'coffee': 100, 'profit': 0}
        return {'water': row[0], 'milk': row[1], 'coffee': row[2], 'profit': row[3]}


def save_resources(resources, profit):
    with _connect() as conn:
        conn.execute(
            'UPDATE resources SET water = ?, milk = ?, coffee = ?, profit = ? WHERE id = 1',
            (resources['water'], resources['milk'], resources['coffee'], profit)
        )
        conn.commit()


def save_order(order):
    with _connect() as conn:
        conn.execute(
            '''
            INSERT INTO orders (drink, size, quantity, total, change, amount_paid, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                order['drink'],
                order['size'],
                order['quantity'],
                order['total'],
                order['change'],
                order['amount_paid'],
                order['timestamp']
            )
        )
        conn.commit()


def get_recent_orders(limit=5):
    with _connect() as conn:
        rows = conn.execute(
            'SELECT drink, size, quantity, total, change, amount_paid, timestamp FROM orders ORDER BY id DESC LIMIT ?',
            (limit,)
        ).fetchall()
        orders = []
        for row in rows:
            orders.append({
                'drink': row[0],
                'size': row[1],
                'quantity': row[2],
                'total': row[3],
                'change': row[4],
                'amount_paid': row[5],
                'timestamp': row[6]
            })
        return orders


def get_order_stats():
    with _connect() as conn:
        row = conn.execute('SELECT COUNT(*), SUM(total) FROM orders').fetchone()
        return {
            'orders': int(row[0] or 0),
            'total_spent': round(float(row[1] or 0), 2)
        }


def reset_db():
    with _connect() as conn:
        conn.execute('DELETE FROM orders')
        conn.execute('UPDATE resources SET water = 300, milk = 200, coffee = 100, profit = 0 WHERE id = 1')
        conn.commit()
