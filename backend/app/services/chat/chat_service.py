from google import genai
from app.config import settings


class ChatService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def answer(self, context: str, question: str):

        prompt = f"""
You are an AI assistant for YouTube videos.

Answer ONLY from the provided context.

If the answer is not present, say:
"I couldn't find that information in this video."

Context:
{context}

Question:
{question}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text