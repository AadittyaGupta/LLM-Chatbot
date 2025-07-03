import streamlit as st
from datetime import datetime
import requests
import json
from olamaFn import get_available_models, get_bot_response
from prompt import promptFn

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm your AI assistant. How can I help you today?",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }]

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "phi3"

if "available_models" not in st.session_state:
    st.session_state.available_models = get_available_models()

# UI
st.title(f"🤖 AI Chatbot ({st.session_state.selected_model.upper()})")
st.markdown("---")

for message in st.session_state.messages:
    st.markdown("**You**" if message["role"] == "user" else "**Bot**")
    if message["role"] == "user":
        st.info(message["content"])
    else:
        st.success(message["content"])

if st.session_state.is_typing:
    st.warning("Generating...")

st.markdown("---")
st.subheader("📝 Your Message")

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Ask me anything...")
    send_button = st.form_submit_button("📤 Send Message")

# MAKING CLEAR AND EXPORT BUTTONS
col1, col2 = st.columns(2)
clear_button = col1.button("🗑️ Clear Chat")
export_button = col2.button("💾 Export Chat")

# HANDLING USER INPUT
if send_button and user_input.strip():
    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip(),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.is_typing = True
    st.rerun()

if st.session_state.is_typing:
    user_message = st.session_state.messages[-1]["content"]
    prompt = f"{promptFn}\nUser: {user_message}\nAssistant:"
    
    response = get_bot_response(prompt, st.session_state.selected_model)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    st.session_state.is_typing = False
    st.rerun()
    
# HANDLING CLEAR BUTTON    
if clear_button:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm your AI assistant. How can I help you today?",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }]
    st.success("Chat cleared!")
    st.rerun()

# HANDLING EXPORT BUTTON 
if export_button and len(st.session_state.messages) > 1:
    chat_content = "CHATBOT CONVERSATION\n" + "="*50 + "\n\n"
    for msg in st.session_state.messages:
        role = "You" if msg["role"] == "user" else "Bot"
        chat_content += f"[{msg['timestamp']}] {role}: {msg['content']}\n\n"

    st.download_button(
        label="📄 Download Chat History",
        data=chat_content,
        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

# SIDEBAR
with st.sidebar:
    st.header("-> Model Selection")

    if st.button("🔄 Refresh Models"):
        st.session_state.available_models = get_available_models()
        st.rerun()

    if st.session_state.available_models:
        selected_model = st.selectbox(
            "Choose Model:",
            st.session_state.available_models,
            index=st.session_state.available_models.index(st.session_state.selected_model)
            if st.session_state.selected_model in st.session_state.available_models else 0
        )

# FOOTER
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.8rem;'>"
    "🤖 Powered by Ollama & Streamlit"
    "</div>", 
    unsafe_allow_html=True
)
