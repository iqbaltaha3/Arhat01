import openai
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get your OpenAI API key from the environment
OPENAI_API_KEY = os.getenv(OPENAI_API_KEY)
if not OPENAI_API_KEY:
    st.error("Please set your OPENAI_API_KEY in your environment or .env file.")
    st.stop()

# Set up the Streamlit page with a custom title and icon
st.set_page_config(page_title="Arhat: The Path to Enlightenment", page_icon="🕉️", layout="wide")

# Custom CSS for a philosophical look: soft background, elegant font, and styled buttons
st.markdown(
    """
    <style>
    body {
        background-color: #FDF6E3;
        color: #073642;
        font-family: 'Georgia', serif;
    }
    .stButton button {
        background-color: #586e75;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
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
    Engage in thoughtful dialogue and explore deep insights and spiritual wisdom as you journey toward enlightenment.
    """
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get response from OpenAI's GPT API
def get_openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            api_key=OPENAI_API_KEY
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input for the chatbot
user_input = st.chat_input("Share your thoughts or ask for guidance...")
if user_input:
    # Add user's message to the conversation
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Prepare the conversation for the API call
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
    # Get the chatbot's response from OpenAI
    bot_response = get_openai_response(messages)
    
    # Append and display the assistant's response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
