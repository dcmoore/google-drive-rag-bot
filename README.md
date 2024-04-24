<h1 align="center">
AI Eng Leader Bot
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
ollama pull llama2:chat
ollama pull nomic-embed-text
docker-compose up
```

To run ollama inside a docker container, follow the steps below:

```bash
docker-compose -f docker-compose-ollama.yml up
docker exec -it google-drive-rag-bot-ollama-container-1 ollama pull llama2:chat
docker exec -it google-drive-rag-bot-ollama-container-1 ollama pull nomic-embed-text
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
ollama pull llama2:chat
ollama pull nomic-embed-text
```

Then you will be able to run the Streamlit server

```bash
poetry run streamlit run app/main.py
```

## Re-Seeding the Database

If you want to add/remove transcripts from the database, start by creating an empty ./data/source_docs/ directory. Then download whatever google doc files you want in .docx format to that directory. Then re-build your app's docker image with docker build, start up your containers with docker-compose, then run the following command to embed the source_docs into the database in vector format:

```bash
docker exec -it google-drive-rag-bot-gdrag-bot-app-1 python3 app/load.py
```

If you want to commit those changes, you can update the seed file with the following command:

```bash
docker exec -i google-drive-rag-bot-gdrag-bot-db-1 /bin/bash -c "PGPASSWORD=<insert password> pg_dump --username <insert user> <insert db name>" > data/pgvector/seed.sql
```

The seed.sql file gets loaded into the database whenever the database container is created.
