from google import genai
from app.config import settings


class EmbeddingService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def embed_documents(self, texts):

        embeddings = []

        for text in texts:

            response = self.client.models.embed_content(
                model="gemini-embedding-001",
                contents=text
            )

            embeddings.append(response.embeddings[0].values)

        return embeddings

    def embed_query(self, text):

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values