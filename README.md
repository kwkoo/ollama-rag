# RAG Demo

The code was copied from [`PromptEngineer48 / Ollama`](https://github.com/PromptEngineer48/Ollama)


## Running with `docker compose`

01. Download and install [Ollama](https://ollama.ai/) on your machine

01. Pull the `mistral` model to your machine

		ollama pull mistral

01. Start Ollama with

		OLLAMA_HOST=0.0.0.0 ollama serve

01. Start the frontend

		docker compose up

01. Copy the documents you want to index into `source_documents`

01. Access the frontend at <http://localhost:8080>

01. Ingest the documents to the vector database

01. Run your queries


## Resources

*   Download embeddings

		EMBEDDINGS_MODEL="all-MiniLM-L6-v2"

		python3 -c "from langchain.embeddings import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='$EMBEDDINGS_MODEL')"

*   Download NLTK resources

		python3 -m nltk.downloader all
