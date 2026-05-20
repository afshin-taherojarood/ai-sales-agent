import datetime
from database import get_connection


def find_product(name):
    """پیدا کردن محصول"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    for p in products:
        if p[1] in name or name in p[1] or name in p[4]:
            return {
                "id": p[0],
                "نام": p[1],
                "قیمت": p[2],
                "موجودی": p[3],
                "مشخصات": p[4]
            }
    return None


def check_price(product_name):
    product = find_product(product_name)
    if product:
        return f"قیمت {product['نام']}: {product['قیمت']} دلار"
    return "محصول پیدا نشد"


def check_inventory(product_name):
    product = find_product(product_name)
    if product:
        if product["موجودی"] > 0:
            return f"{product['نام']} موجود است. تعداد: {product['موجودی']} عدد"
        return f"{product['نام']} ناموجود است"
    return "محصول پیدا نشد"


def get_specs(product_name):
    product = find_product(product_name)
    if product:
        return f"مشخصات {product['نام']}: {product['مشخصات']}"
    return "محصول پیدا نشد"


def list_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, stock, specs FROM products")
    products = cursor.fetchall()
    conn.close()

    result = "محصولات موجود:\n"
    for p in products:
        status = "موجود" if p[2] > 0 else "ناموجود"
        result += f"- {p[0]}: {p[3]} | قیمت: {p[1]} دلار | {status}\n"
    return result


def register_order(customer_name, phone, address, product_name):
    product = find_product(product_name)
    if product is None:
        return "محصول پیدا نشد"
    if product["موجودی"] == 0:
        return f"{product['نام']} موجود نیست"

    order_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = get_connection()
    cursor = conn.cursor()

    # ثبت سفارش
    cursor.execute("""
        INSERT INTO orders 
        (order_number, customer_name, phone, address, product_name, price, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order_number, customer_name, phone, address, product["نام"], product["قیمت"], created_at))

    # کم کردن موجودی
    cursor.execute(
        "UPDATE products SET stock = stock - 1 WHERE id = ?",
        (product["id"],)
    )

    conn.commit()
    conn.close()

    return f"✅ سفارش ثبت شد! شماره سفارش: {order_number}"