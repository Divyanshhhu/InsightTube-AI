from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.schemas.pdf import PDFRequest
from app.services.notes.notes_service import NotesService
from app.services.pdf.pdf_service import PDFService
from app.services.rag.vectordb import VectorDBService

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)


@router.post("/")
def generate_pdf(request: PDFRequest):

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

    pdf_path = PDFService.create_pdf(
        notes,
        request.video_id
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{request.video_id}.pdf"
    )