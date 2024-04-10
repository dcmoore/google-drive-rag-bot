<h1 align="center">
Google Drive RAG Bot
</h1>

## 💻 Running Locally

Start by cloning the repository

```bash
git clone https://github.com/dcmoore/google-drive-rag-bot.git
```

### Run with Docker

Then build the image

```bash
DOCKER_BUILDKIT=1 docker build --target=runtime . -t gdrag-bot:latest
```

You can then run the container alongside the project's dependent containers

```bash
docker-compose up
```

**IMPORTANT** Before using the application, make sure to download the Llama2:chat LLM. This step may take a few minutes.

```bash
docker exec -it google-drive-rag-bot-ollama-container-1 ollama run llama2:chat
```

After that, everything should work as expected.

### Run without Docker

Alternatively you can install dependencies locally with [Poetry](https://python-poetry.org/) and activate virtual environment

```bash
poetry install
poetry shell
```

You then need to download [Ollama](https://ollama.com/) (if on mac you can run `brew install ollama`). Then you need to start the ollama server

```bash
ollama serve
```

Then in a new terminal, install and run the llama2:chat LLM

```bash
ollama run llama2:chat
```

Then you will be able to run the Streamlit server

```bash
streamlit run app/main.py
```
