
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load private API key
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# Page configuration
st.set_page_config(
    page_title="MBZ AI",
    page_icon="🤖",
    layout="centered"
)

# AI client
if not API_KEY:
    st.error("API key not found. Check your .env file.")
    st.stop()

client = Groq(api_key=API_KEY)

# MBZ AI branding
st.title("🤖 MBZ AI")
st.caption("Your personal AI assistant")

# AI personality
SYSTEM_PROMPT = """
You are MBZ AI, a helpful, intelligent and friendly
AI assistant.

Your goals:
- Answer questions clearly.
- Explain difficult topics simply.
- Help with programming and technology.
- Be friendly and respectful.
- Give detailed answers when necessary.
"""

# Initialize conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Message MBZ AI...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            with st.spinner("MBZ is thinking..."):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        *st.session_state.messages
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )

                answer = response.choices[0].message.content
                st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Something went wrong: {e}")
