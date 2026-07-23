from google import genai
from app.config import settings


class NotesService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate_notes(self, context: str):

        prompt = f"""
You are an expert note maker.

Create clean and well-structured notes from the following transcript.

Rules:
- Use headings.
- Use bullet points.
- Keep important concepts.
- Do not add information not present in the transcript.
- Make the notes easy to revise.

Transcript:

{context}
"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text