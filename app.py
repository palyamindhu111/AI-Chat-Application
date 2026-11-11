

import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖")

st.title("🤖 AI Chat Assistant")
st.caption("Powered by Groq AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask me anything...")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=st.session_state.messages
                )
                answer = response.choices[0].message.content
                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

except Exception as e:
    st.error(f"Please configure your Groq API key in Streamlit Secrets. Error: {e}")
