from pydantic import BaseModel


class NotesRequest(BaseModel):
    video_id: str