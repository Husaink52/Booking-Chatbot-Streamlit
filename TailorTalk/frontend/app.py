import streamlit as st
import requests

st.set_page_config(page_title="Appointment Chatbot")

st.title(" Appointment Chatbot")
st.markdown("Ask anything or book an appointment!")

# Session to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
user_input = st.text_input("You:", key="input")

# Send to backend on input
if user_input:
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": user_input}
        )
        reply = response.json()["response"]

        # Append to chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", reply))

    except Exception as e:
        st.error(f" Backend error: {e}")

# Display history
for sender, message in st.session_state.chat_history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(message)
