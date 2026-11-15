

import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="College AI Chatbot",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e1b4b, #312e81);
}
[data-testid="stChatMessage"] {
    background-color: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(129, 140, 248, 0.3);
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 12px;
}
[data-testid="stChatInput"] {
    border: 1px solid #6366f1;
    border-radius: 15px;
}
h1, h2, h3 {
    color: #c7d2fe;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1e1b4b);
}
.stButton button {
    border-radius: 12px;
    border: 1px solid #6366f1;
}
.stButton button:hover {
    background-color: #4338ca;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 College AI Chatbot")
st.caption("Your smart assistant for college information")

if not API_KEY:
    st.error("API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 1

if "delete_chat" not in st.session_state:
    st.session_state.delete_chat = None

if "clear_all_confirm" not in st.session_state:
    st.session_state.clear_all_confirm = False

if st.session_state.current_chat is None:
    st.session_state.chat_counter += 1
    st.session_state.current_chat = (
        f"Chat {st.session_state.chat_counter}"
    )
    st.session_state.messages = []
    st.session_state.chats[st.session_state.current_chat] = []

if st.session_state.current_chat not in st.session_state.chats:
    st.session_state.chats[st.session_state.current_chat] = []

st.session_state.chats[st.session_state.current_chat] = (
    st.session_state.messages.copy()
)

with st.sidebar:
    st.title("💬 Chat History")
    st.caption("Your conversations")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.chat_counter += 1
        new_name = f"Chat {st.session_state.chat_counter}"
        st.session_state.current_chat = new_name
        st.session_state.messages = []
        st.session_state.chats[new_name] = []
        st.session_state.clear_all_confirm = False
        st.rerun()

    st.divider()

    if st.button("🗑️ Clear All Chats", use_container_width=True):
        st.session_state.clear_all_confirm = True

    if st.session_state.clear_all_confirm:
        st.warning("Delete ALL conversations?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes, Delete", key="confirm_clear"):
                st.session_state.chats = {}
                st.session_state.messages = []
                st.session_state.chat_counter += 1

                new_name = f"Chat {st.session_state.chat_counter}"
                st.session_state.current_chat = new_name
                st.session_state.chats[new_name] = []

                st.session_state.delete_chat = None
                st.session_state.clear_all_confirm = False
                st.success("All chats deleted!")
                st.rerun()

        with col2:
            if st.button("Cancel", key="cancel_clear"):
                st.session_state.clear_all_confirm = False
                st.rerun()

    st.divider()

    for chat_name in list(st.session_state.chats):
        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button(
                f"💬 {chat_name}",
                key=f"open_{chat_name}",
                use_container_width=True
            ):
                st.session_state.current_chat = chat_name
                st.session_state.messages = (
                    st.session_state.chats[chat_name].copy()
                )
                st.session_state.delete_chat = None
                st.rerun()

        with col2:
            if st.button("🗑️", key=f"delete_{chat_name}"):
                st.session_state.delete_chat = chat_name

    if st.session_state.delete_chat:
        chat_to_delete = st.session_state.delete_chat

        st.warning(f"Delete {chat_to_delete}?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Yes", key="delete_yes"):
                if chat_to_delete in st.session_state.chats:
                    del st.session_state.chats[chat_to_delete]

                if st.session_state.current_chat == chat_to_delete:
                    st.session_state.messages = []
                    st.session_state.current_chat = None

                st.session_state.delete_chat = None
                st.rerun()

        with col2:
            if st.button("Cancel", key="delete_cancel"):
                st.session_state.delete_chat = None
                st.rerun()

    st.divider()

    with st.expander("ℹ️ About Project"):
        st.write("🎓 College AI Chatbot")
        st.write(
            "An AI-powered chatbot that helps users "
            "ask questions and receive intelligent responses."
        )

        st.write("🛠️ Technologies Used")
        st.write("- Python")
        st.write("- Streamlit")
        st.write("- Google Gemini AI")

    with st.expander("👨‍💻 Developer"):
        st.write("Developed by: Vinay Chowdhary")
        st.write("B.Tech CSE (AI & ML)")
        st.write("Mohan Babu University")

    st.markdown(
        "<center><small>✨ Powered by Gemini AI</small></center>",
        unsafe_allow_html=True
    )

if not st.session_state.messages:
    st.markdown("""
    <div style="
        text-align:center;
        padding:45px 15px;
        background:rgba(99,102,241,0.10);
        border:1px solid rgba(129,140,248,0.25);
        border-radius:25px;
        margin-top:25px;
    ">
        <div style="font-size:65px;">🎓</div>
        <h2 style="color:#c7d2fe;">Welcome to College AI</h2>
        <p style="color:#e0e7ff;font-size:18px;">
            Your smart assistant for college information
        </p>
        <p style="color:#a5b4fc;">
            Ask about admissions, courses, fees and more!
        </p>
        <p style="color:#818cf8;font-size:14px;">
            Start a conversation below 👇
        </p>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("✨ Ask your question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        answer = None

        for attempt in range(3):
            with st.spinner("🤖 Gemini is thinking..."):
                try:
                    conversation = []

                    for message in st.session_state.messages:
                        role = message["role"]

                        if role == "assistant":
                            role = "model"

                        conversation.append({
                            "role": role,
                            "parts": [{"text": message["content"]}]
                        })

                    response = client.models.generate_content(
                        model="gemini-4-hydrogen",
                        contents=conversation
                    )

                    answer = response.text
                    st.write(answer)
                    break

                except Exception as e:
                    error_message = str(e)

                    if "503" in error_message and attempt < 2:
                        time.sleep(3)
                    else:
                        answer = (
                            "Gemini is temporarily unavailable. "
                            "Please try again later."
                        )
                        st.error(answer)
                        st.caption(error_message)
                        break

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.session_state.chats[st.session_state.current_chat] = (
        st.session_state.messages.copy()
    )
