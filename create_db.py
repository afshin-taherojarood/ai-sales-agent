import pandas as pd

products = [
    {"نام": "ایسوس", "قیمت": 450, "موجودی": 5, "مشخصات": "RTX 3050, 16GB RAM"},
    {"نام": "لنوو", "قیمت": 480, "موجودی": 2, "مشخصات": "RTX 3060, 16GB RAM"},
    {"نام": "اچ پی", "قیمت": 500, "موجودی": 0, "مشخصات": "RTX 3050Ti, 8GB RAM"},
    {"نام": "دل", "قیمت": 520, "موجودی": 3, "مشخصات": "RTX 3060Ti, 32GB RAM"},
    {"نام": "مایکروسافت", "قیمت": 600, "موجودی": 1, "مشخصات": "Intel Iris Xe, 16GB RAM"},
]

df = pd.DataFrame(products)
df.to_excel("products.xlsx", index=False)
print("✅ فایل products.xlsx ساخته شد!")