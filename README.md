# RAG Demo

The code was copied from [`PromptEngineer48 / Ollama`](https://github.com/PromptEngineer48/Ollama)


## Deploying on OpenShift

01. Provision an OpenShift cluster on `demo.redhat.com` from the `NVIDIA GPU Operator OCP4 Workshop` catalog item

01. Login with `oc login`

01. Deploy the NFD and Nvidia GPU operators

		make deploy-nvidia

01. Deploy ollama and the frontend to OpenShift

		make deploy
	
	When the application has been deployed, it should output the URLs of the file browser and the frontend

01. Access the file browser and upload the documents you want to index

01. Access the frontend and click on the link to ingest documents to the vector database

01. After the document ingestion process has completed, click on the `Refresh Database` button - this forces the query engine to refresh its connection to the vector database

01. Access the front page of the frontend again and click on the link to run your queries

01. Type your query into the prompt text field and click the `Query` button


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

	If you encounter any connection errors, try removing or commenting out the following in `yaml/docker-compose.yaml`

		extra_hosts:
		- host.docker.internal:host-gateway


## Resources

*   Download embeddings

		EMBEDDINGS_MODEL="all-MiniLM-L6-v2"

		python3 -c "from langchain.embeddings import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='$EMBEDDINGS_MODEL')"

*   Download NLTK resources

		python3 -m nltk.downloader all
