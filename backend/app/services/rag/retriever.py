from app.services.rag.embedder import EmbeddingService
from app.services.rag.vectordb import VectorDBService


class RetrieverService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_db = VectorDBService()

    def retrieve(
        self,
        question: str,
        video_id: str,
        n_results: int = 5
    ):

        # Embed the user's question
        query_embedding = self.embedding_service.embed_query(question)

        # Search only inside the current video's chunks
        results = self.vector_db.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={
                "video_id": video_id
            }
        )

        return results