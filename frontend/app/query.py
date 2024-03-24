#!/usr/bin/env python3
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import BaseCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import Ollama

import os
import threading
import queue
from typing import Any, Generator

# Copied from https://github.com/langchain-ai/langchain/issues/4950#issuecomment-1790074587
class QueueCallbackHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.queue.put(token)

    def on_llm_end(self, *args, **kwargs) -> Any:
        return self.queue.empty()

def stream(cb: Any, llm_queue: queue.Queue) -> Generator:
    job_done = object()

    def task(res):
        cb(res)
        llm_queue.put(job_done)

    res = dict()
    t = threading.Thread(target=task, args=(res,))
    t.start()

    while True:
        try:
            item = llm_queue.get(True, timeout=5)
            if item is job_done:
                break
            yield(item)
        except queue.Empty:
            continue

    t.join()
    if res is not None and res.get('source_documents') is not None:
        yield('\n==========\n')
        yield('Sources\n')
        for doc in res['source_documents']:
            yield('----------\n')
            yield('→ ' + doc.metadata['source'] + ':\n')
            yield(doc.page_content)
            yield('\n\n')


base_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
model = os.environ.get("MODEL", "mistral")
# For embeddings model, the example uses a sentence-transformers model
# https://www.sbert.net/docs/pretrained_models.html 
# "The all-mpnet-base-v2 model provides the best quality, while all-MiniLM-L6-v2 is 5 times faster and still offers good quality."
embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME", "all-MiniLM-L6-v2")
persist_directory = os.environ.get("PERSIST_DIRECTORY", "db")
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS',4))
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
output_queue = queue.Queue()
llm = Ollama(model=model, callbacks=[QueueCallbackHandler(output_queue)], base_url=base_url)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
lock = threading.Lock()

def ollama_query(prompt: str):
    def cb(output):
        res = qa(prompt)
        if res.get('source_documents') is not None:
            output['source_documents'] = res['source_documents']
    lock.acquire()
    yield from stream(cb, output_queue)
    lock.release()

#if __name__ == "__main__":
#    main()