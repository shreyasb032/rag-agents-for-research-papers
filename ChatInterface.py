import streamlit as st

st.set_page_config(page_title="AI Chat Demo", layout="centered")

st.title("🤖 AI Chat Demo")
st.markdown("Chat with your AI agent below. (No backend yet, just a demo!)")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state.messages:
    if msg["sender"] == "user":
        st.markdown(f'<div style="text-align: right; color: #1976d2;">**You:** {msg["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left; color: #444;">**AI:** {msg["text"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("Type your message...")

if user_input and user_input.strip() != "":
    # Add user message
    st.session_state.messages.append({"sender": "user", "text": user_input.strip()})
    # Trigger a placeholder AI response
    st.session_state.messages.append({"sender": "ai", "text": "AI agent response..."})
    # Clear the input field
    st.session_state['input_text'] = ""
    st.rerun()

