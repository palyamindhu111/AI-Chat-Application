
import streamlit as st
import ollama

st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Chat Assistant")
st.caption("Powered by Ollama - Llama 3.2")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                response = ollama.chat(
                    model="llama3.2:1b",
                    messages=st.session_state.messages
                )

                answer = response["message"]["content"]
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Error: {e}")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
