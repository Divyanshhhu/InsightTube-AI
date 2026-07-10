from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.video import router as video_router
from app.api import chat
from app.api import notes
from app.api import pdf

app = FastAPI(
    title="InsightTube AI",
    version="1.0.0"
)

# Allow Chrome Extension and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_router)
app.include_router(chat.router)
app.include_router(notes.router)
app.include_router(pdf.router)


@app.get("/")
def root():
    return {
        "message": "InsightTube AI Backend Running 🚀"
    }