import uuid
from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain.embeddings import OllamaEmbeddings

def store_embeddings(summaries, elements, config):
    store = InMemoryStore()
    id_key = "doc_id"
    vectorstore = Chroma(
        collection_name="financials",
        embedding_function=OllamaEmbeddings(model="mxbai-embed-large"),
        persist_directory=config["VECTORSTORE_DIR"],
    )
    doc_ids = [str(uuid.uuid4()) for _ in elements]
    summary_docs = [Document(page_content=s, metadata={id_key: doc_ids[i]}) for i, s in enumerate(summaries)]
    vectorstore.add_documents(summary_docs)
    store.mset(list(zip(doc_ids, elements)))
    return vectorstore, store