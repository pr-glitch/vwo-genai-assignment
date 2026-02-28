import numpy as np
import requests
from langchain_community.document_loaders import PyPDFLoader
from crewai_tools import SerperDevTool

# =====================================
# External Search Tool
# =====================================

# Make sure SERPER_API_KEY is set
search_tool = SerperDevTool()

# =====================================
# Ollama Embedding Endpoint
# =====================================

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"

# =====================================
# Extract PDF Text
# =====================================

def extract_pdf_text(path: str) -> str:
    docs = PyPDFLoader(file_path=path).load()
    full_text = ""

    for page in docs:
        content = page.page_content.strip()
        if content:
            full_text += content + "\n"

    return full_text


# =====================================
# Chunk Text
# =====================================

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# =====================================
# Generate Embedding (Ollama)
# =====================================

def get_embedding(text: str):
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    response.raise_for_status()
    return np.array(response.json()["embedding"])


# =====================================
# Retrieve Relevant Chunks
# =====================================

def retrieve_relevant_chunks(chunks, chunk_embeddings, query, top_k=2):

    query_embedding = get_embedding(query)
    chunk_embeddings = np.array(chunk_embeddings)

    similarities = np.dot(chunk_embeddings, query_embedding) / (
        np.linalg.norm(chunk_embeddings, axis=1) *
        np.linalg.norm(query_embedding)
    )

    top_indices = similarities.argsort()[-top_k:][::-1]

    return [chunks[i] for i in top_indices]

    

