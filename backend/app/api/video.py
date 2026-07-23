from fastapi import APIRouter, HTTPException

from app.schemas.video import VideoRequest
from app.utils.youtube import extract_video_id
import traceback
from app.services.transcript.service import TranscriptService
from app.services.transcript.processor import TranscriptProcessor

from app.services.rag.chunker import ChunkService
from app.services.rag.embedder import EmbeddingService
from app.services.rag.vectordb import VectorDBService

from app.services.youtube.metadata import YouTubeMetadataService
from app.services.rag.retriever import RetrieverService

router = APIRouter(
    prefix="/video",
    tags=["Video"]
)


@router.post("/index")
def index_video(request: VideoRequest):
    try:
        # Extract video ID
        video_id = extract_video_id(request.url)

        metadata = YouTubeMetadataService.get_metadata(
            request.url,
            video_id
            )

        # Fetch transcript
        transcript = TranscriptService.get_transcript(video_id)

        # Convert transcript into plain text
        text = TranscriptProcessor.to_text(transcript)

        # Split transcript into chunks
        documents = ChunkService.split(text)

        # Extract text from documents
        texts = [doc.page_content for doc in documents]

        # Generate embeddings
        embedding_service = EmbeddingService()
        embeddings = embedding_service.embed_documents(texts)

        # Store in ChromaDB
        vector_db = VectorDBService()
        vector_db.add_documents(
            documents=documents,
            embeddings=embeddings,
            video_id=video_id
        )

        vector_db.save_video_metadata(
            video_id=video_id,
            title=metadata["title"],
            thumbnail=metadata["thumbnail"],
            channel=metadata["channel"]
        )

        return {
            "status": "indexed",
            "video_id": video_id,
            "title": metadata["title"],
            "thumbnail": metadata["thumbnail"],
            "channel": metadata["channel"],
            "chunks": len(documents)
        }
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/test-search")
def test_search(question: str):

    retriever = RetrieverService()

    results = retriever.retrieve(question)

    return {
        "results": results
    }

@router.get("/debug/metadata")
def debug_metadata():

    vector_db = VectorDBService()

    return vector_db.metadata_collection.get()


@router.get("/history")
def get_history():

    vector_db = VectorDBService()

    data = vector_db.get_all_metadata()

    history = []

    ids = data.get("ids", [])
    metadatas = data.get("metadatas", [])

    for i in range(len(ids)):

        metadata = metadatas[i]

        history.append({
            "video_id": metadata["video_id"],
            "title": metadata["title"],
            "thumbnail": metadata["thumbnail"],
            "channel": metadata["channel"],
            "indexed_at": metadata["indexed_at"]
        })

    history.sort(
        key=lambda x: x["indexed_at"],
        reverse=True
    )

    return history


@router.delete("/history/{video_id}")
async def delete_video(video_id: str):
    try:
        vector_db = VectorDBService()
        vector_db.delete_video(video_id)

        return {
            "status": "success",
            "message": "Video deleted successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/metadata/{video_id}")
def get_metadata(video_id: str):

    vector_db = VectorDBService()

    metadata = vector_db.get_video_metadata(video_id)

    if metadata is None:
        raise HTTPException(status_code=404, detail="Not found")

    return metadata