import sqlite3
import pandas as pd


def get_connection():
    """اتصال به دیتابیس"""
    return sqlite3.connect("shop.db")


def init_db():
    """ساخت جداول دیتابیس"""
    conn = get_connection()
    cursor = conn.cursor()

    # جدول محصولات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            stock INTEGER NOT NULL,
            specs TEXT NOT NULL
        )
    """)

    # جدول سفارشات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            product_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ دیتابیس ساخته شد!")


def seed_products():
    """اضافه کردن محصولات اولیه"""
    conn = get_connection()
    cursor = conn.cursor()

    # چک کن قبلاً داده داره یا نه
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] > 0:
        print("⚠️ محصولات قبلاً اضافه شدن")
        conn.close()
        return

    products = [
        ("ایسوس", 450, 5, "RTX 3050, 16GB RAM"),
        ("لنوو", 480, 2, "RTX 3060, 16GB RAM"),
        ("اچ پی", 500, 0, "RTX 3050Ti, 8GB RAM"),
        ("دل", 520, 3, "RTX 3060Ti, 32GB RAM"),
        ("مایکروسافت", 600, 1, "Intel Iris Xe, 16GB RAM"),
    ]

    cursor.executemany(
        "INSERT INTO products (name, price, stock, specs) VALUES (?, ?, ?, ?)",
        products
    )

    conn.commit()
    conn.close()
    print("✅ محصولات اضافه شدن!")


if __name__ == "__main__":
    init_db()
    seed_products()