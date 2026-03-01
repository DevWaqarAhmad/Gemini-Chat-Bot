import streamlit as st
import uuid
import backend

# ==============================
# Page Configuration
# ==============================
st.set_page_config(
    page_title="Butt Karahi AI Agent",
    page_icon="",
    layout="wide"
)

st.title("Butt Karahi AI Agent")

# ==============================
# Session State Initialization
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "language" not in st.session_state:
    st.session_state.language = "Auto-Detect"

# ==============================
# Greetings per language
# ==============================
GREETINGS = {
    "Auto-Detect": "Hello! Welcome to Butt Karahi. How can I assist you today? 🍽️",
    "en": "Hello! Welcome to Butt Karahi. How can I assist you today? 🍽️",
    "ur": "!خوش آمدید! Butt Karahi میں آپ کا استقبال ہے۔ میں آپ کی کس طرح مدد کر سکتا ہوں؟ 🍽️",
    "ar": "!مرحبًا! أهلاً بك في Butt Karahi. كيف يمكنني مساعدتك اليوم؟ 🍽️",
    "hi": "नमस्ते! Butt Karahi में आपका स्वागत है। मैं आपकी कैसे मदद कर सकता हूँ? 🍽️",
}

# ==============================
# Sidebar
# ==============================
with st.sidebar:
    st.header("⚙️ Settings")

    language_options = ["Auto-Detect"] + list(backend.SUPPORTED_LANGUAGES.keys())

    selected_lang = st.selectbox(
        "🌐 Select Language",
        language_options,
        index=language_options.index(st.session_state.language)
    )

    # If language changed, reset chat
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.session_state.messages = []
        st.session_state.user_name = None
        st.rerun()

    if st.button("🔄 New Chat"):
        st.session_state.messages = []
        st.session_state.user_name = None
        st.rerun()

    st.divider()
    st.markdown("**📍 Our Locations:**")
    st.markdown("🏬 Mississauga: 3015 Winston Churchill Blvd")
    st.markdown("🏬 Pickering: 820 Kingston Rd")

# ==============================
# Initial Greeting
# ==============================
if not st.session_state.messages:
    greeting = GREETINGS.get(st.session_state.language, GREETINGS["en"])
    st.session_state.messages.append({
        "role": "assistant",
        "content": greeting
    })

# ==============================
# Display Chat History
# ==============================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================
# Handle User Input
# ==============================
if prompt := st.chat_input("Ask something about Butt Karahi..."):

    # Save and show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Detect and store name
    if "my name is" in prompt.lower():
        name = prompt.lower().split("my name is")[-1].strip().title()
        st.session_state.user_name = name

    # Name recall
    if "what is my name" in prompt.lower() and st.session_state.user_name:
        response = f"Your name is **{st.session_state.user_name}**! 😊"
    else:
        # Show spinner while generating
        with st.spinner("Thinking..."):
            response = backend.generate_response(prompt)

    # Display and save assistant reply
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})