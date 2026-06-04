import streamlit as st
from database import init_db, seed_products

# ساخت دیتابیس اگه وجود نداشت
init_db()
seed_products()

st.set_page_config(
    page_title="فروشگاه هوشمند",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 فروشگاه لپ تاپ هوشمند")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_chatbot.py", label="🤖 دستیار فروش", icon="🤖")
    st.caption("با دستیار هوشمند ما لپ تاپ مناسب رو پیدا کن")

with col2:
    st.page_link("pages/2_admin.py", label="🛠️ پنل مدیریت", icon="🛠️")
    st.caption("مدیریت محصولات و سفارشات")