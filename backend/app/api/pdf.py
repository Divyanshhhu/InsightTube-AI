from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.schemas.pdf import PDFRequest
from app.services.pdf.pdf_service import PDFService

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)


@router.post("/")
def generate_pdf(request: PDFRequest):

    pdf_path = PDFService.create_pdf(
    request.notes,
    request.video_id
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{request.video_id}.pdf"
    )