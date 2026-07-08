from app.services.rag.embedder import EmbeddingService
from app.services.rag.vectordb import VectorDBService


class RetrieverService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_db = VectorDBService()

    def retrieve(self, question: str, n_results: int = 5):

        # Convert question into embedding
        query_embedding = self.embedding_service.embed_query(question)

        # Search ChromaDB
        results = self.vector_db.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results