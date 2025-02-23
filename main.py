import streamlit as st
import os
import time
import requests
from dotenv import load_dotenv

# Set the page configuration as the very first Streamlit command
st.set_page_config(page_title="Arhat: The Path to Enlightenment", page_icon="🕉️", layout="wide")

# Load environment variables (from .env locally or via Streamlit Cloud secrets)
load_dotenv()

# Retrieve your API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("Please set your OPENAI_API_KEY in your environment or via Streamlit Cloud secrets.")
    st.stop()

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

# App Title and Description
st.title("Arhat: The Path to Enlightenment 🕉️")
st.write(
    """
    Welcome to **Arhat**, a philosophical chatbot inspired by the Buddhist concept of the enlightened one.
    Engage in thoughtful dialogue and explore deep insights on your journey toward enlightenment.
    """
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get a response from OpenAI using direct HTTP requests with retry logic
def get_openai_response(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": prompt,
        "temperature": 0.7
    }
    retries = 3      # Number of retries
    backoff = 2      # Initial wait time in seconds
    for attempt in range(retries):
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 429:
            st.warning("Rate limit exceeded, waiting before retrying...")
            time.sleep(backoff)
            backoff *= 2  # Exponential backoff
            continue
        try:
            response.raise_for_status()  # Raise an error for other bad status codes
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error: {str(e)}"
    return "Error: Too many requests, please try again later."

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input for the chatbot
user_input = st.chat_input("Share your thoughts or ask for guidance...")
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Prepare conversation history and get the assistant's response
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
    bot_response = get_openai_response(messages)
    
    # Append and display the assistant's response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)








