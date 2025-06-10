# utils/reference_loader.py

import os
from rag.loader_chunker import extract_text_from_pdf, chunk_text
from utils.wiki_fetcher import fetch_wikipedia_summary
from rag.embedder import VectorStore
from rag.retriever import ReferenceRetriever

# def get_reference_data(input_type: str, input_value: str, query: str = "") -> str:
#     """
#     input_type: one of ['text', 'pdf', 'wiki']
#     input_value: text directly, or pdf path, or wiki query
#     """
#     if input_type == "text":
#         return input_value.strip()

#     elif input_type == "pdf":
#         if not os.path.exists(input_value):
#             raise FileNotFoundError(f"PDF file not found: {input_value}")
        
#         full_text = extract_text_from_pdf(input_value)
#         chunks = chunk_text(full_text)

#         vector_store = VectorStore()
#         vector_store.build_index(chunks)

#         retriever = ReferenceRetriever(vector_store)
#         reference_data = retriever.retrieve_references(query)

#         return reference_data
#         #return extract_text_from_pdf(input_value)

#     elif input_type == "wiki":
#         return fetch_wikipedia_summary(input_value)

#     else:
#         raise ValueError("Invalid reference input type. Use 'text', 'pdf', or 'wiki'.")
import os
from rag.loader_chunker import extract_text_from_pdf, chunk_text
from rag.embedder import VectorStore
from rag.vector_cache_loader import load_or_build_index
from rag.retriever import ReferenceRetriever
from utils.wiki_fetcher import fetch_wikipedia_summary  # assuming you have this
import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url: str) -> str:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    return ' '.join(soup.stripped_strings)

def get_reference_data(input_type: str, input_value: str, query: str = "") -> str:
    """
    input_type: one of ['text', 'pdf', 'wiki']
    input_value: text directly, or pdf path, or wiki query
    """
    if input_type == "text":
        return input_value.strip()

    elif input_type == "pdf":
        if not os.path.exists(input_value):
            raise FileNotFoundError(f"PDF file not found: {input_value}")
        
        # Use cached version for large PDFs
        vector_store = load_or_build_index(input_value)
        retriever = ReferenceRetriever(vector_store)
        return retriever.retrieve_references(query)

    elif input_type == "wiki":
        return fetch_wikipedia_summary(input_value)
    
    elif input_type == "url":
        raw_text = extract_text_from_url(input_value)
        chunks = chunk_text(raw_text)
        vector_store = VectorStore()
        vector_store.build_index(chunks)
        retriever = ReferenceRetriever(vector_store)
        reference_data = retriever.retrieve_references(query)
        return reference_data

    else:
        raise ValueError("Invalid reference input type. Use 'text', 'pdf', or 'wiki'.")
