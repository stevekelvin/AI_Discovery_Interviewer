import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="AI Discovery Interview Assistant")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False

# OpenRouter + DeepSeek API Setup
OPENROUTER_API_KEY = "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"
LLM_MODEL = "deepseek-chat"  # you can also try "mistral", "openchat", etc.

# Function to query OpenRouter API with DeepSeek
def get_llm_response(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        #"HTTP-Referer": "https://yourdomain.com",  # Replace with your site or GitHub repo
        "HTTP-Referer": "https://github.com/stevekelvin/AI_Discovery_Interviewer",  # Replace with your site or GitHub repo
        
    }
    body = {
        "model": LLM_MODEL,
        "messages": messages,
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Start the conversation with first question if not started
if not st.session_state.conversation_started:
    system_prompt = {
        "role": "system",
        "content": (
            "You are an AI Discovery Interview Assistant. "
            "Your job is to ask structured, intelligent questions to a company representative. "
            "The goal is to understand their operations, workflows, and pain points — especially to find opportunities to apply AI. "
            "Begin by asking your first discovery question about how their operations or teams work."
        )
    }
    st.session_state.chat_history.append(system_prompt)

    first_response = get_llm_response(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": first_response})
    st.session_state.conversation_started = True

# Display chat messages
st.title("🤖 AI Discovery Interview Tool")
st.subheader("Smart interview to uncover automation & AI opportunities")

for msg in st.session_state.chat_history:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input box
user_input = st.chat_input("Your answer or clarification...")

if user_input:
    # Append user input
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get next AI question or follow-up
    bot_reply = get_llm_response(st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

    # Show latest exchange
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

