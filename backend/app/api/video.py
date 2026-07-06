from fastapi import APIRouter
from app.schemas.video import VideoRequest
from app.utils.youtube import extract_video_id
from app.services.transcript.service import TranscriptService

router = APIRouter(
    prefix="/video",
    tags=["Video"]
)

@router.post("/load")
def load_video(request: VideoRequest):

    video_id = extract_video_id(request.url)

    transcript = TranscriptService.get_transcript(video_id)

    return {
        "video_id": video_id,
        "transcript": transcript
    }