import streamlit as st
import os
import backend
import json
from langchain.memory import ConversationBufferMemory

# ✅ Load chat history from a file
def load_chat_history():
    try:
        with open("chat_memory.json", "r") as file:
            content = file.read().strip()
            if not content:
                return []
            history = json.loads(content)
            return history if isinstance(history, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# ✅ Save chat history to a file
def save_chat_history(history):
    with open("chat_memory.json", "w") as file:
        json.dump(history, file)

# ✅ Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

# ✅ Load chat history
if "messages" not in st.session_state:
    stored_history = load_chat_history()
    formatted_history = [{"role": msg["role"], "content": msg["content"]} for msg in stored_history]
    st.session_state.messages = formatted_history

# ✅ Store user name when introduced
if "user_name" not in st.session_state:
    st.session_state.user_name = None  

st.title("Butt Karahi AI Agent")

# ✅ Display full chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Handle user input
if prompt := st.chat_input("Ask Something About Butt Karahi?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # ✅ Detect name introduction
    if "my name is" in prompt.lower():
        st.session_state.user_name = prompt.split("my name is")[-1].strip()

    # ✅ Generate response using full chat history
    chat_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    response = backend.GenerateResponse(f"{chat_context}\nUser: {prompt}")

    # ✅ If user asks for their name
    if "what is my name" in prompt.lower() and st.session_state.user_name:
        response = f"Your name is {st.session_state.user_name}!"

    # ✅ Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)

    # ✅ Save conversation to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.memory.save_context({"input": prompt}, {"output": response})
    save_chat_history(st.session_state.messages)
def clear_chat_history():
    if os.path.exists("chat_history.json"):
        os.remove("chat_history.json")  # Delete the JSON file

if st.button("🔄 Refresh Chat"):
    st.session_state.messages = []  # Clear session state
    clear_chat_history()  # Remove stored chat history
    st.rerun()  # Refresh UI