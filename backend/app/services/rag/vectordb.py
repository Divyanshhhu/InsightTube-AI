import chromadb


class VectorDBService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="youtube_videos"
        )

    def add_documents(
        self,
        documents,
        embeddings,
        video_id
    ):

        self.collection.add(
            ids=[
                f"{video_id}_{i}"
                for i in range(len(documents))
            ],
            documents=[
                doc.page_content
                for doc in documents
            ],
            embeddings=embeddings,
            metadatas=[
                {
                    "video_id": video_id,
                    "chunk": i
                }
                for i in range(len(documents))
            ]
        )