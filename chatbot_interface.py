import streamlit as st
from chatbot_core import ChatbotCore

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatbotCore()

for msg in st.session_state.chatbot.get_history():
    st.chat_message("user" if msg.type == "human" else "assistant").write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    response = st.session_state.chatbot.send_message(prompt)
    st.chat_message("assistant").write(response)