from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag.retriever import RetrieverService
from app.services.chat.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    video_id: str
    question: str
    temperature: float = 0.7
    system_prompt: str = ""

@router.post("/")
def chat(request: ChatRequest):

    retriever = RetrieverService()

    results = retriever.retrieve(
        question=request.question,
        video_id=request.video_id
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    chat_service = ChatService()

    answer = chat_service.answer(
        context=context,
        question=request.question,
        temperature=request.temperature,
        system_prompt=request.system_prompt
    )

    return {
        "answer": answer,
        "sources": [
            {
                "chunk": metadata["chunk"],
                "score": round(distance, 3)
            }
            for metadata, distance in zip(
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    }