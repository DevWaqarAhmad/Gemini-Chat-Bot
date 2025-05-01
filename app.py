import streamlit as st
import os
import uuid
import backend


st.set_page_config(
    page_title="Butt Karahi AI Agent",
    layout="wide"
)
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "language" not in st.session_state:
    st.session_state.language = "Auto-Detect"

user_id = st.session_state.user_id
language_options = ["Auto-Detect"] + [lang["name"] for lang in backend.SUPPORTED_LANGUAGES.values()]

st.title("Butt Karahi AI Agent")

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    st.session_state.language = st.selectbox(
        "🌐 Select Language",
        language_options,
        index=language_options.index(st.session_state.language)
    )
    
    if st.button("🔄 Refresh Chat"):
        st.session_state.messages = []
        st.rerun()

# Initial greeting
if not st.session_state.messages:
    lang_code = "en" if st.session_state.language == "Auto-Detect" else next(
        (code for code, val in backend.SUPPORTED_LANGUAGES.items() if val["name"] == st.session_state.language),
        "en"
    )
    
    greeting = backend.SUPPORTED_LANGUAGES.get(lang_code, backend.SUPPORTED_LANGUAGES["en"])["greeting"]
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask Something About Butt Karahi?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Detect if user shares their name
    if "my name is" in prompt.lower():
        st.session_state.user_name = prompt.split("my name is")[-1].strip()

    # Special case for remembering name
    if "what is my name" in prompt.lower() and st.session_state.user_name:
        response = f"Your name is {st.session_state.user_name}!"
    else:
        # Call backend generate_response function with entire chat history context
        full_chat = "\n".join([message["content"] for message in st.session_state.messages])
        response = backend.generate_response(prompt, st.session_state.language, context=full_chat)

    # Show assistant reply
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save assistant's response in memory (handled by LangChain's memory)
    st.session_state.messages.append({"role": "assistant", "content": response})
