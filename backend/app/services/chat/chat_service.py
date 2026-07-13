from google import genai
from app.config import settings


class ChatService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def answer(self, context: str, question: str):

        prompt = f"""
You are InsightTube AI.

Answer ONLY using the provided transcript.

Rules:
- Do not use outside knowledge.
- If the answer is not in the transcript, say:
  "I couldn't find that information in this video."
- Be concise and clear.
- Use markdown.
- Use bullet points whenever appropriate.
- If explaining a concept, explain it simply.
- Do not say "Based on the provided transcript".
- Do not mention the context or transcript.
- Answer as if you watched the video yourself.

Transcript:
{context}

Question:
{question}
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text