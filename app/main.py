"""Python file to serve as the frontend"""
import os
import streamlit as st

from load import load_database
from util import read_secret
from langchain.chains import RetrievalQA
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_postgres.vectorstores import PGVector

# Load the Ollama model and the embeddings with vector store data
if 'qa' not in st.session_state:
    print("Loading database")
    load_database()

    ollama_host = os.getenv("OLLAMA_HOST", "localhost")
    llm = Ollama(model="llama2:chat", base_url="http://{}:11434".format(ollama_host), verbose=True, temperature=0.8)
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://{}:11434".format(ollama_host), show_progress=True, temperature=0.8)
    vector_store = PGVector(
        embeddings=embeddings,
        connection=f"postgresql+psycopg://{read_secret('postgres_user')}:{read_secret('postgres_password')}@gdrag-bot-db:5432/{read_secret('postgres_db')}",
    )

    st.session_state.qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True,
        verbose=True
    )


# Streamlit frontend
st.title("Chat with an AI engineering leader.")
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm an AI engineering leader. Ask me a question as if I were a real engineering leader and I'll do my best to share perspective that's been loaded into my system."}
    ]

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_prompt = "You are an engineering leader who responds concisely and has been asked the following question: " + prompt
            response = st.session_state.qa.invoke(full_prompt).get("result", "I don't know")
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
