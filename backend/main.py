from fastapi import FastAPI, File, UploadFile
from backend.config import load_config
from backend.document_processor import process_pdf
from backend.summarization_pipeline import summarize_content
from backend.vector_store_manager import store_embeddings
from backend.rag_pipeline import run_rag_pipeline
import io

app = FastAPI()

# Store embeddings in memory
vector_store = None

@app.post("/process_pdf")
async def process_pdf_endpoint(file: UploadFile = File(...)):
    global vector_store
    config = load_config()
    content = await file.read()
    pdf_stream = io.BytesIO(content)
    
    elements = process_pdf(pdf_stream, config)
    summaries = summarize_content(elements)
    vector_store, _ = store_embeddings(summaries, elements, config)
    
    return {"message": "PDF processed successfully"}

@app.post("/query")
async def query_endpoint(query: dict):
    global vector_store
    if vector_store is None:
        return {"error": "No PDF has been processed yet."}
    
    user_query = query.get("query")
    response = run_rag_pipeline(user_query, vector_store.as_retriever())
    return {"answer": response}
