from google import genai
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

models = [
    "models/gemini-flash-latest",
    "models/gemini-3.5-flash",
    "models/gemini-3.1-flash-lite",
    "models/gemini-2.5-flash-lite",
    "models/gemini-2.0-flash",
]

for model in models:
    try:
        print(f"\nTrying: {model}")
        response = client.models.generate_content(
            model=model,
            contents="Say hello."
        )
        print("SUCCESS:", response.text)
        break
    except Exception as e:
        print("FAILED:", e)