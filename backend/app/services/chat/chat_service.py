from google import genai
from app.config import settings


class ChatService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def answer(self, context: str, question: str):

        prompt = f"""
You are InsightTube AI, an assistant that answers questions only using the provided YouTube transcript.

Rules:
1. Answer ONLY from the provided context.
2. If the answer is not present, reply:
   "I couldn't find that information in this video."
3. Keep the answer concise.
4. Use bullet points whenever appropriate.
5. Do not make up information.

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