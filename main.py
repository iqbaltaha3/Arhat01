import streamlit as st

# Must be the first Streamlit call
st.set_page_config(page_title="Arhat: The Path to Enlightenment", page_icon="🕉️", layout="wide")

import openai
import os
from dotenv import load_dotenv

# Load environment variables (from .env locally or Streamlit Cloud secrets)
load_dotenv()

# Retrieve the API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("Please set your OPENAI_API_KEY in your environment or via Streamlit Cloud secrets.")
    st.stop()

# Set the API key globally
openai.api_key = OPENAI_API_KEY

# (Optional) Debug: show the OpenAI library version
st.write("OpenAI Python library version:", openai.__version__)

# Custom CSS for a calm, philosophical look
st.markdown(
    """
    <style>
    body {
        background-color: #FDF6E3;
        color: #073642;
        font-family: 'Georgia', serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title and description
st.title("Arhat: The Path to Enlightenment 🕉️")
st.write(
    """
    Welcome to **Arhat**, a philosophical chatbot inspired by the Buddhist concept of the enlightened one.
    Engage in thoughtful dialogue and explore deep insights on your journey toward enlightenment.
    """
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get a response from OpenAI's API using the new interface
def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("Share your thoughts or ask for guidance...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
    bot_response = get_openai_response(messages)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)






