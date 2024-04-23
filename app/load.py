import os

from util import read_secret
from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres.vectorstores import PGVector

def load_database():
  ollama_host = os.getenv("OLLAMA_HOST", "localhost")
  embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://{}:11434".format(ollama_host), show_progress=True, temperature=0.8)

  loader = DirectoryLoader(
    os.path.abspath("../data/source_docs"),
    glob="**/*.docx",
    use_multithreading=True,
    show_progress=True,
    max_concurrency=50,
    loader_cls=Docx2txtLoader,
  )

  docs = loader.load()

  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
  )

  chunks = text_splitter.split_documents(docs)

  PGVector.from_documents(
    documents=chunks,
    embedding=embeddings,
    connection=f"postgresql+psycopg://{read_secret('postgres_user')}:{read_secret('postgres_password')}@gdrag-bot-db:5432/{read_secret('postgres_db')}",
    pre_delete_collection=True,
  )
