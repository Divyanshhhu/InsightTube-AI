from fastapi import APIRouter, HTTPException

from app.schemas.video import VideoRequest
from app.utils.youtube import extract_video_id
from app.services.transcript.service import TranscriptService
from app.services.transcript.processor import TranscriptProcessor
from app.services.rag.chunker import ChunkService

router = APIRouter(
    prefix="/video",
    tags=["Video"]
)


@router.post("/index")
def load_video(request: VideoRequest):
    try:
        # Extract video ID
        video_id = extract_video_id(request.url)

        # Fetch transcript
        transcript = TranscriptService.get_transcript(video_id)

        # Convert transcript into plain text
        text = TranscriptProcessor.to_text(transcript)

        # Split into chunks
        documents = ChunkService.split(text)

        return {
            "status": "success",
            "video_id": video_id,
            "total_characters": len(text),
            "total_chunks": len(documents),
            "first_chunk_preview": documents[0].page_content[:300]
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )