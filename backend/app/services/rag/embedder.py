import time

from google import genai
from app.config import settings


class EmbeddingService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def embed_documents(self, texts):

        embeddings = []

        batch_size = 10

        for i in range(0, len(texts), batch_size):

            batch = texts[i:i + batch_size]

            print(f"Embedding batch {i // batch_size + 1}")

            response = self.client.models.embed_content(
                model="gemini-embedding-001",
                contents=batch
            )

            embeddings.extend(
                embedding.values
                for embedding in response.embeddings
            )

            # Prevent hitting the free-tier rate limit
            time.sleep(1)

        return embeddings

    def embed_query(self, text):

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values