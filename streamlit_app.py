import streamlit as st
import requests

# Configuration
st.set_page_config(page_title="AI Discovery Interview Tool", layout="centered")
st.title("🤖 AI Discovery Interview Assistant")

# Session State Setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are an expert in AI transformation. Ask smart discovery questions to uncover operations and processes in an organization where AI or automation could be applied. Ask one question at a time. Wait for a response. Based on the answer, ask follow-up questions if needed. Continue until you have enough understanding to suggest AI opportunities."}
    ]
if "current_question" not in st.session_state:
    st.session_state.current_question = ""

# OpenRouter + DeepSeek API Setup
#OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "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")  # Replace with your key or use Streamlit secrets
OPENROUTER_API_KEY = "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"
MODEL = "deepseek-chat"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_llm(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # Can be localhost or your deployed domain
        "X-Title": "AI Discovery Tool"
    }

    body = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        st.error(f"Error from OpenRouter: {response.status_code} {response.text}")
        return ""

# Show chat history
st.subheader("📋 Interview Transcript")
for msg in st.session_state.chat_history[1:]:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input for organization rep
with st.chat_message("user"):
    user_input = st.text_input("Your answer (or ask a question):", key="user_input")

if st.button("Submit Answer") and user_input.strip():
    # Add user's response to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Ask next question using LLM
    with st.spinner("Thinking..."):
        response = ask_llm(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    st.experimental_rerun()

# Show raw transcript at the bottom
if st.checkbox("Show raw chat history"):
    st.write(st.session_state.chat_history)
