from fastapi import APIRouter

from app.schemas.notes import NotesRequest
from app.services.notes.notes_service import NotesService
from app.services.rag.vectordb import VectorDBService

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


@router.post("/")
def generate_notes(request: NotesRequest):

    vector_db = VectorDBService()

    results = vector_db.collection.get(
        where={
            "video_id": request.video_id
        }
    )

    documents = results["documents"]

    transcript = "\n\n".join(documents)

    notes_service = NotesService()

    notes = notes_service.generate_notes(transcript)

    return {
        "notes": notes
    }