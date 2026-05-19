import pandas as pd

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