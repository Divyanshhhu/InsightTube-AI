from google import genai
from dotenv import load_dotenv
import os

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Test generation
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello."
    )
    print("Generation works:", response.text)
except Exception as e:
    print("Generation failed:", e)

# Test embeddings
try:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents="Hello world"
    )
    print("Embedding works:", len(response.embeddings[0].values))
except Exception as e:
    print("Embedding failed:", e)