import streamlit as st
import os
import uuid
import backend
import json
from langchain.memory import ConversationBufferMemory

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

def save_chat_history(history):
    with open("chat_memory.json", "w") as file:
        json.dump(history, file)

# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

# Load chat history
if "messages" not in st.session_state:
    stored_history = load_chat_history()
    formatted_history = [{"role": msg["role"], "content": msg["content"]} for msg in stored_history]
    st.session_state.messages = formatted_history

# Store user name when introduced
if "user_name" not in st.session_state:
    st.session_state.user_name = None  

# Ensure a unique user_id for the session
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())  # Generate a unique user ID for the session

user_id = st.session_state.user_id  # Use the user_id from session state

if "language" not in st.session_state:
    st.session_state.language = "Auto-Detect"
language_options = ["Auto-Detect"] + [lang["name"] for lang in backend.SUPPORTED_LANGUAGES.values()]

st.title("Butt Karahi AI Agent ")

# Language selector in sidebar (NEW)
with st.sidebar:
    st.header("Settings")
    st.session_state.language = st.selectbox(
        "🌐 Select Language for Communicate with us",
        language_options,
        index=language_options.index(st.session_state.language)
    )
    
    if st.button("🔄 Refresh Chat"):
        st.session_state.messages = []
        if os.path.exists("chat_memory.json"):
            os.remove("chat_memory.json")
        st.rerun()

if not st.session_state.messages:
    lang_code = "en"  
    if st.session_state.language != "Auto-Detect":
        lang_code = [code for code, config in backend.SUPPORTED_LANGUAGES.items() 
                    if config["name"] == st.session_state.language][0]
    greeting = backend.SUPPORTED_LANGUAGES[lang_code]["greeting"]
    st.session_state.messages.append({"role": "assistant", "content": greeting})

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

    # Prepare context with language preference (NEW)
    chat_context = {
        "messages": "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]),
        "language": st.session_state.language
    }

    # Generate response (modified for language support)
    response = backend.GenerateResponse(
        f"{chat_context['messages']}\nUser: {prompt}",
        user_id=user_id  # Pass the user_id along with the message
    )

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
