from pydantic import BaseModel


class PDFRequest(BaseModel):
    video_id: str
    notes: str