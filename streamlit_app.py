
import streamlit as st
import requests

st.set_page_config(page_title="AI Discovery Interview", layout="wide")
st.title("🤖 AI Discovery Interview Tool")
st.markdown("This tool conducts a structured interview to uncover AI opportunities in your organization.")

# Configuration
#API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_URL = "https://openrouter.ai/api/v1"

MODEL = "deepseek/deepseek-chat-v3-0324:free"

# Ask user for API key securely
api_key = st.sidebar.text_input("Enter your OpenRouter API Key", type="password")

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": (
                "You are a human AI expert conducting a discovery interview with a company representative. "
                "Your job is to understand their organization, operations, workflows, and challenges. "
                "Ask one insightful question at a time. Start broad — identify the type of organization and its functions — then go deeper into specific departments, tasks, tools, inefficiencies, and data flows. "
                "Speak naturally, like a human professional. Don’t mention AI, don’t say you're starting, and don’t ask about the format. "
                "Avoid phrases like 'How should we proceed?' or 'Understood.' Don’t reveal the goal is to find AI opportunities — just collect detailed information through intelligent, flowing questions. "
                "Begin now with the first question."
            ),
        }
    ]

def ask_openrouter(prompt, history):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": history + [{"role": "user", "content": prompt}],
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    # Validate response
    if response.status_code != 200:
        st.error(f"API request failed: {response.status_code} - {response.text}")
        st.stop()

    try:
        result = response.json()
        message = result["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Failed to parse response: {e}\nFull response: {response.text}")
        st.stop()



    return message

# Display chat history
for message in st.session_state.chat_history[1:]:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])
    elif message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])

# Start interview with first question
if len(st.session_state.chat_history) == 1:
    if api_key:
        with st.spinner("Thinking..."):
            question = ask_openrouter("", st.session_state.chat_history)
            if question:
                st.session_state.chat_history.append({"role": "assistant", "content": question})
                st.rerun()
    else:
        st.warning("Please enter your OpenRouter API key in the sidebar.")

# User input
if api_key and len(st.session_state.chat_history) > 1:
    user_input = st.chat_input("Your response")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            reply = ask_openrouter("", st.session_state.chat_history)
            if reply:
                st.session_state.chat_history.append({'role': 'assistant', 'content': reply})
                st.rerun()
