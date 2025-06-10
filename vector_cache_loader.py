import os
from rag.hashing import compute_pdf_hash
from rag.embedder import VectorStore
def load_or_build_index(pdf_path, vectorstore_cache_dir="vector_cache/"):
    from rag.loader_chunker import extract_text_from_pdf, chunk_text  # adjust as needed

    file_hash = compute_pdf_hash(pdf_path)
    cache_path = os.path.join(vectorstore_cache_dir, f"{file_hash}.pkl")

    vector_store = VectorStore()

    if os.path.exists(cache_path):
        vector_store.load(cache_path)
    else:
        full_text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(full_text)
        vector_store.build_index(chunks)
        vector_store.save(cache_path)

    return vector_store
