import os

from util import read_secret
from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_postgres.vectorstores import PGVector

def load_database():
  ollama_host = os.getenv("OLLAMA_HOST", "localhost")
  embeddings = OllamaEmbeddings(model="llama2:7b", base_url="http://{}:11434".format(ollama_host), show_progress=True, temperature=0.8)

  loader = DirectoryLoader(
      os.path.abspath("../data/source_docs"),
      glob="**/*.docx",
      use_multithreading=True,
      show_progress=True,
      max_concurrency=50,
      loader_cls=Docx2txtLoader,
      sample_size=1, # while testing
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
