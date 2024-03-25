# RAG Demo

The code was copied from [`PromptEngineer48 / Ollama`](https://github.com/PromptEngineer48/Ollama)


## Running with `docker compose`

01. Download and install [Ollama](https://ollama.ai/) on your machine

01. Pull the `mistral` model to your machine

		ollama pull mistral

01. Start Ollama with

		OLLAMA_HOST=0.0.0.0 ollama serve

01. Create a sub-folder named `db` and a sub-folder named `source_documents` in the same folder as this `README` - `db` will be used by the vector database while `source_documents` will be used to contain the documents you want to search

01. Start the frontend

		docker compose -f yaml/docker-compose.yaml up

01. Copy the documents you want to index into `source_documents`

01. Access the frontend at <http://localhost:8080>

	*   Ingest the documents to the vector database
	*   After the document ingestion process has completed, click on the `Refresh Database` button - this forces the query engine to refresh its connection to the vector database

01. Run your queries at <http://localhost:8080/query.html>


## Resources

*   Download embeddings

		EMBEDDINGS_MODEL="all-MiniLM-L6-v2"

		python3 -c "from langchain.embeddings import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='$EMBEDDINGS_MODEL')"

*   Download NLTK resources

		python3 -m nltk.downloader all
