from dotenv import load_dotenv
import os

load_dotenv(override=True)


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


settings = Settings()
print("Using API Key:", settings.GEMINI_API_KEY[:10])