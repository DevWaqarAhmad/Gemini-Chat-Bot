import streamlit as st
import random
import time
import backend
from langchain.memory import ConversationBufferMemory

# Initialize LangChain Memory (Stores chat history in RAM)
memory = ConversationBufferMemory()

# Streamed response emulator
def response_generator(prompt):
    response = backend.GenerateResponse(prompt)
    
    # Save conversation in memory
    memory.save_context({"input": prompt}, {"output": response})
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("Butt Karahi AI Agent ")

# Initialize chat history (Using LangChain Memory)
if "messages" not in st.session_state:
    st.session_state.messages = memory.load_memory_variables({}).get("chat_history", [])

# Display chat messages from memory
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask Something About Butt Karahi?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Gemini AI & store it in memory
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Update LangChain memory
    memory.save_context({"input": prompt}, {"output": response})
