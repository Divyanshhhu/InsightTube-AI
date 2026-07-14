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

    # 1. Check if notes already exist
    existing_notes = vector_db.get_notes(request.video_id)

    if existing_notes:

        return {
            "notes": existing_notes,
            "cached": True
        }

    # 2. Fetch transcript
    results = vector_db.collection.get(
        where={
            "video_id": request.video_id
        }
    )

    documents = results["documents"]

    transcript = "\n\n".join(documents)

    # 3. Generate notes
    notes_service = NotesService()

    notes = notes_service.generate_notes(transcript)

    # 4. Save notes
    vector_db.save_notes(
        request.video_id,
        notes
    )

    return {
        "notes": notes,
        "cached": False
    }