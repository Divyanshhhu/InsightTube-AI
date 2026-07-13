from fastapi import APIRouter
from app.services.rag.vectordb import VectorDBService

router = APIRouter(prefix="/video", tags=["Video"])

vector_db = VectorDBService()


@router.get("/status/{video_id}")
def check_status(video_id: str):

    results = vector_db.collection.get(
        where={"video_id": video_id}
    )

    return {
        "indexed": len(results["ids"]) > 0
    }