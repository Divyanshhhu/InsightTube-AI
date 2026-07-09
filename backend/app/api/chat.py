from fastapi import APIRouter

from app.services.rag.retriever import RetrieverService
from app.services.chat.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/")
def chat(question: str):

    retriever = RetrieverService()

    results = retriever.retrieve(question)

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    print("=" * 80)
    print(context[:3000])
    print("=" * 80)

    chat_service = ChatService()

    answer = chat_service.answer(
        context=context,
        question=question
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