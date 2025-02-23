import streamlit as st

# st.set_page_config MUST be the first Streamlit call.
st.set_page_config(page_title="Arhat: The Path to Enlightenment", page_icon="🕉️", layout="wide")

import openai
import os
from dotenv import load_dotenv

# Load environment variables (local .env or Streamlit Cloud secrets)
load_dotenv()

# Retrieve the API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("Please set your OPENAI_API_KEY in your environment or via Streamlit Cloud secrets.")
    st.stop()

# Set the API key globally for the openai library
openai.api_key = OPENAI_API_KEY

# Debug: Show the OpenAI Python library version (should be 1.64.0 or later)
st.write("OpenAI Python library version:", openai.__version__)

# Custom CSS for a serene, philosophical look
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

# Function to get a response from OpenAI's API using the new interface
def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt
        )
        # Accessing response using dictionary keys as per the new interface
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input for the chatbot
user_input = st.chat_input("Share your thoughts or ask for guidance...")
if user_input:
    # Append the user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Prepare conversation history and get the bot's response
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
    bot_response = get_openai_response(messages)
    
    # Append and display the assistant's response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)





