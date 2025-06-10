from rag.embedder import VectorStore

class ReferenceRetriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve_references(self, query: str, top_k: int = 5):
        """
        Retrieve top-k relevant chunks from the vector store.
        
        Args:
            query (str): User query for evaluation context.
            top_k (int): Number of reference chunks to return.

        Returns:
            str: Concatenated top-k relevant chunks.
        """
        top_chunks = self.vector_store.search(query, top_k=top_k)
        return "\n\n".join(top_chunks)
