from fastapi import APIRouter, HTTPException

from app.schemas.video import VideoRequest
from app.utils.youtube import extract_video_id

from app.services.transcript.service import TranscriptService
from app.services.transcript.processor import TranscriptProcessor

from app.services.rag.chunker import ChunkService
from app.services.rag.embedder import EmbeddingService
from app.services.rag.vectordb import VectorDBService

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

        return {
            "status": "indexed",
            "video_id": video_id,
            "chunks": len(documents)
        }
    
    except Exception as e:
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


   