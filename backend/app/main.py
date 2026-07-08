from fastapi import FastAPI
from app.api.video import router as video_router
from app.api import chat

app = FastAPI(
    title="InsightTube AI",
    version="1.0.0"
)

app.include_router(video_router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {
        "message": "InsightTube AI Backend Running 🚀"
    }