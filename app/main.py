"""Python file to serve as the frontend"""
import sys
import os

sys.path.append(os.path.abspath('.'))

from langchain_community.llms import Ollama
import streamlit as st

ollama_host = os.getenv("OLLAMA_HOST", "localhost")
llm = Ollama(model="llama2:chat", base_url="http://{}:11434".format(ollama_host), verbose=True)

st.title("Chat with Google Drive Docs")
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question !"}
    ]

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(prompt)
            print(response)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
