import os
import requests
import streamlit as st
import uuid

# ✅ Set API URL
API_URL = "http://127.0.0.1:8000/query"

# ✅ Generate or retrieve session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("💬 ProRail RAG Chatbot with Memory & Streaming")
st.markdown("Ask me anything about ProRail's business activities 📚")

# ✅ Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ User input
user_input = st.chat_input("Type your question...")

if user_input:
    # ✅ Display user input in UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ✅ Display assistant response in UI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # ✅ Stream response from API
        response = requests.post(API_URL, json={"session_id": st.session_state.session_id, "question": user_input}, stream=True)
        full_response = ""

        for chunk in response.iter_lines():
            if chunk:
                decoded_chunk = chunk.decode("utf-8")
                full_response += decoded_chunk
                message_placeholder.markdown(full_response)

        # ✅ Store full response in chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
