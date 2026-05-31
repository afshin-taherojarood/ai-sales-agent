from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from database import get_connection
import datetime
import os

load_dotenv()


# ─── تعریف Tools با LangChain ───

@tool
def check_price(product_name: str) -> str:
    """چک کردن قیمت محصول"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products")
    products = cursor.fetchall()
    conn.close()

    for p in products:
        if p[0] in product_name or product_name in p[0]:
            return f"قیمت {p[0]}: {p[1]} دلار"
    return "محصول پیدا نشد"


@tool
def check_inventory(product_name: str) -> str:
    """چک کردن موجودی محصول"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, stock FROM products")
    products = cursor.fetchall()
    conn.close()

    for p in products:
        if p[0] in product_name or product_name in p[0]:
            if p[1] > 0:
                return f"{p[0]} موجود است. تعداد: {p[1]} عدد"
            return f"{p[0]} ناموجود است"
    return "محصول پیدا نشد"


@tool
def list_products() -> str:
    """نمایش لیست همه محصولات موجود"""
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


@tool
def register_order(customer_name: str, phone: str, address: str, product_name: str) -> str:
    """ثبت سفارش مشتری"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, stock FROM products")
    products = cursor.fetchall()

    product = None
    for p in products:
        if p[1] in product_name or product_name in p[1]:
            product = p
            break

    if not product:
        conn.close()
        return "محصول پیدا نشد"
    if product[3] == 0:
        conn.close()
        return f"{product[1]} موجود نیست"

    order_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute("""
        INSERT INTO orders 
        (order_number, customer_name, phone, address, product_name, price, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order_number, customer_name, phone, address, product[1], product[2], created_at))

    cursor.execute("UPDATE products SET stock = stock - 1 WHERE id = ?", (product[0],))
    conn.commit()
    conn.close()

    return f"✅ سفارش ثبت شد! شماره سفارش: {order_number}"


# ─── ساخت Agent ───

llm = ChatOpenAI(
    model="google/gemini-2.0-flash-001",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY")
)

tools = [check_price, check_inventory, list_products, register_order]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="تو یک دستیار فروش هوشمند هستی. برای هر اطلاعاتی از tools استفاده کن."
)


class LangChainAgent:
    def __init__(self):
        self.history = []

    def chat(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})

        result = agent.invoke({"messages": self.history})

        response = result["messages"][-1].content
        self.history.append({"role": "assistant", "content": response})

        return response