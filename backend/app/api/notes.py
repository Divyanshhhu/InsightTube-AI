from fastapi import APIRouter
from fastapi import HTTPException
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
    print(results)
    
    documents = results["documents"]
    if not documents:
        raise HTTPException(
            status_code=404,
            detail="Video is not indexed. Please index it first."
        )

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

@router.get("/{video_id}")
def get_notes(video_id: str):

    vector_db = VectorDBService()

    notes = vector_db.get_notes(video_id)

    if notes:

        return {
            "exists": True,
            "notes": notes
        }

    return {
        "exists": False
    }