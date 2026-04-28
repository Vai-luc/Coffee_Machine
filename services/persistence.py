import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get("DATABASE_URL")


def _connect():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    with _connect() as conn:
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


def load_resources():
    with _connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT water, milk, coffee, profit FROM resources WHERE id = 1')
            row = cursor.fetchone()
            if row is None:
                return {'water': 300, 'milk': 200, 'coffee': 100, 'profit': 0}
            return dict(row)


def save_resources(resources, profit):
    with _connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'UPDATE resources SET water = %s, milk = %s, coffee = %s, profit = %s WHERE id = 1',
                (resources['water'], resources['milk'], resources['coffee'], profit)
            )
        conn.commit()


def save_order(order):
    with _connect() as conn:
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


def get_recent_orders(limit=5):
    with _connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT drink, size, quantity, total, change, amount_paid, timestamp FROM orders ORDER BY id DESC LIMIT %s',
                (limit,)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]


def get_order_stats():
    with _connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT COUNT(*), SUM(total) FROM orders')
            row = cursor.fetchone()
            return {
                'orders': int(row['count'] or 0),
                'total_spent': round(float(row['sum'] or 0), 2)
            }


def reset_db():
    with _connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM orders')
            cursor.execute('UPDATE resources SET water = 300, milk = 200, coffee = 100, profit = 0 WHERE id = 1')
        conn.commit()
