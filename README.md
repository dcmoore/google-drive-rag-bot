<h1 align="center">
Google Drive RAG Bot
</h1>

## 💻 Running Locally

Start by cloning the repository

```bash
git clone https://github.com/dcmoore/google-drive-rag-bot.git
```

Create ./data/pgvector/local-password.txt and ./data/pgvector/local-user.txt files, then fill them with whatever one word value you want. They will be used to set the user & password of your locally running postgres db.

### Run with Docker

Then build the image

```bash
DOCKER_BUILDKIT=1 docker build --target=runtime . -t gdrag-bot:latest
```

Now you have to make a choice due to a docker/ollama/mac gpu compatibility issue ([details here](https://chariotsolutions.com/blog/post/apple-silicon-gpus-docker-and-ollama-pick-two/)). You can run ollama inside a docker container (which will be really slow for Apple hardware) or you can run ollama on the host machine with GPU acceleration. To run ollama on the host machine, follow the steps below:

```bash
brew install ollama
ollama serve
ollama run llama2:chat
docker-compose up
```

To run ollama inside a docker container, follow the steps below:

```bash
docker-compose -f docker-compose-ollama.yml up
docker exec -it google-drive-rag-bot-ollama-container-1 ollama run llama2:chat
```

After that, everything should work as expected. You can visit the site by going to [http://localhost:8080](http://localhost:8080)

### Run without Docker

Alternatively you can install dependencies locally with [Poetry](https://python-poetry.org/)

```bash
poetry install
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
poetry run streamlit run app/main.py
```
