import streamlit as st
from database import get_connection
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "admin123")

# ─── احراز هویت ───
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔐 ورود به پنل مدیریت")

        username = st.text_input("نام کاربری")
        password = st.text_input("رمز عبور", type="password")

        if st.button("ورود"):
            if username == ADMIN_USER and password == ADMIN_PASS:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباهه!")
        return False
    return True


if not check_password():
    st.stop()

# ─── بقیه کد admin ───
st.set_page_config(page_title="پنل مدیریت", layout="wide")
st.title("🛠️ پنل مدیریت فروشگاه")

tab1, tab2 = st.tabs(["📦 سفارشات", "💻 محصولات"])

# ─── تب سفارشات ───
with tab1:
    st.subheader("لیست سفارشات")
    conn = get_connection()
    orders = pd.read_sql("SELECT * FROM orders ORDER BY created_at DESC", conn)
    conn.close()

    if orders.empty:
        st.info("هنوز سفارشی ثبت نشده")
    else:
        st.dataframe(orders, use_container_width=True)

# ─── تب محصولات ───
with tab2:
    st.subheader("لیست محصولات")
    conn = get_connection()
    products = pd.read_sql("SELECT * FROM products", conn)
    conn.close()

    st.dataframe(products, use_container_width=True)

    st.divider()
    st.subheader("➕ اضافه کردن محصول جدید")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("نام محصول")
        price = st.number_input("قیمت (دلار)", min_value=0)
    with col2:
        stock = st.number_input("موجودی", min_value=0)
        specs = st.text_input("مشخصات")

    if st.button("اضافه کن"):
        if name and specs:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, price, stock, specs) VALUES (?, ?, ?, ?)",
                (name, price, stock, specs)
            )
            conn.commit()
            conn.close()
            st.success(f"✅ {name} اضافه شد!")
            st.rerun()
        else:
            st.error("نام و مشخصات رو پر کن!")