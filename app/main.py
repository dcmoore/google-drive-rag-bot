"""Python file to serve as the frontend"""
import os

from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_experimental.text_splitter import SemanticChunker
from langchain_postgres.vectorstores import PGVector

import streamlit as st

def read_secret(secret_name):
    secret_path = f"/run/secrets/{secret_name}"
    if os.path.exists(secret_path):
        with open(secret_path, 'r') as secret_file:
            return secret_file.read().strip()
    return os.getenv(secret_name.upper())

ollama_host = os.getenv("OLLAMA_HOST", "localhost")
llm = Ollama(model="llama2:chat", base_url="http://{}:11434".format(ollama_host), verbose=True, temperature=0.8)
embeddings = OllamaEmbeddings(model="llama2:7b", base_url="http://{}:11434".format(ollama_host), show_progress=True, temperature=0.8)

loader = DirectoryLoader(
    os.path.abspath("../data/source_docs"),
    glob="**/*.docx",
    use_multithreading=True,
    show_progress=True,
    max_concurrency=50,
    loader_cls=Docx2txtLoader,
    sample_size=2, # while testing
)
docs = loader.load()

text_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="standard_deviation",
    breakpoint_threshold_amount=1.0,
)

chunks = text_splitter.split_documents(docs)

PGVector.from_documents(
    documents=chunks,
    embedding=embeddings,
    connection=f"postgresql+psycopg://{read_secret('postgres_user')}:{read_secret('postgres_password')}@gdrag-bot-db:5432/{read_secret('postgres_db')}",
    pre_delete_collection=True,
)

print(f"Loaded {len(chunks)} chunks")

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
