import streamlit as st
from dotenv import load_dotenv
from agent import Agent

load_dotenv()

st.title("🤖 دستیار فروش هوشمند")
st.caption("برای خرید لپ تاپ اینجام!")

# ساخت agent فقط یه بار
if "agent" not in st.session_state:
    st.session_state.agent = Agent()

# نگه داشتن تاریخچه مکالمه
if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش تاریخچه
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# گرفتن input از کاربر
if prompt := st.chat_input("سوال خود را بنویسید..."):
    # نمایش پیام کاربر
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # گرفتن جواب از agent
    with st.chat_message("assistant"):
        with st.spinner("در حال پردازش..."):
            response = st.session_state.agent.chat(prompt)
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})