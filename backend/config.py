import os
from dotenv import load_dotenv, find_dotenv

def load_config():
    load_dotenv(find_dotenv())
    return {
        "UNSTRUCTURED_API_KEY": os.getenv("UNSTRUCTURED_API_KEY"),
        "UNSTRUCTURED_API_URL": os.getenv("UNSTRUCTURED_API_URL"),
        "VECTORSTORE_DIR": "./Data/chroma_data2"
    }