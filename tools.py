import pandas as pd
import datetime


def load_products():
    df = pd.read_excel("products.xlsx")
    return df

def find_product(name):
    df = load_products()
    for _, row in df.iterrows():
        if row["نام"] in name or name in row["نام"] or name in str(row["مشخصات"]):
            return row
    return None

def check_price(product_name):
    product = find_product(product_name)
    if product is not None:
        return f"قیمت {product['نام']}: {product['قیمت']} دلار"
    return "محصول پیدا نشد"

def check_inventory(product_name):
    product = find_product(product_name)
    if product is not None:
        if product["موجودی"] > 0:
            return f"{product['نام']} موجود است. تعداد: {product['موجودی']} عدد"
        return f"{product['نام']} ناموجود است"
    return "محصول پیدا نشد"

def get_specs(product_name):
    product = find_product(product_name)
    if product is not None:
        return f"مشخصات {product['نام']}: {product['مشخصات']}"
    return "محصول پیدا نشد"

def list_products():
    df = load_products()
    result = "محصولات موجود:\n"
    for _, row in df.iterrows():
        result += f"- {row['نام']}: {row['مشخصات']} | قیمت: {row['قیمت']} دلار\n"
    return result


def register_order(customer_name, phone, address, product_name):
    """ثبت سفارش مشتری داخل فایل Excel"""

    # چک کن محصول موجوده
    product = find_product(product_name)
    if product is None:
        return "محصول پیدا نشد"
    if product["موجودی"] == 0:
        return f"{product['نام']} موجود نیست"

    # ساخت سفارش جدید
    order = {
        "شماره سفارش": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "نام مشتری": customer_name,
        "تلفن": phone,
        "آدرس": address,
        "محصول": product["نام"],
        "قیمت": product["قیمت"],
        "تاریخ": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    # ذخیره داخل Excel
    try:
        df = pd.read_excel("orders.xlsx")
    except:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([order])], ignore_index=True)
    df.to_excel("orders.xlsx", index=False)

    return f"✅ سفارش شما ثبت شد! شماره سفارش: {order['شماره سفارش']}"
