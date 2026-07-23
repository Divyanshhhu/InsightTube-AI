import chromadb
from datetime import datetime

class VectorDBService:

    def __init__(self):
        
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="youtube_videos"
        )

        self.notes_collection = self.client.get_or_create_collection(
            name="video_notes"
        )

        self.metadata_collection = self.client.get_or_create_collection(
            name="video_metadata"
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

    def save_notes(self, video_id: str, notes: str):

    # Remove old notes if they exist
        try:
            self.notes_collection.delete(ids=[video_id])
        except Exception:
            pass

        self.notes_collection.add(
            ids=[video_id],
            documents=[notes],
            metadatas=[{"video_id": video_id}]
        )


    def get_notes(self, video_id: str):

        result = self.notes_collection.get(
            ids=[video_id]
        )

        if result["documents"]:
            return result["documents"][0]

        return None
    
    def save_video_metadata(
        self,
        video_id: str,
        title: str,
        thumbnail: str,
        channel: str
    ):

        try:
            self.metadata_collection.delete(ids=[video_id])
        except Exception:
            pass

        self.metadata_collection.add(
            ids=[video_id],
            documents=[title],
            metadatas=[{
                "video_id": video_id,
                "title": title,
                "thumbnail": thumbnail,
                "channel": channel,
                "indexed_at": datetime.now().isoformat()
            }]
        )

    def get_all_metadata(self):
        return self.metadata_collection.get()


    def delete_video(self, video_id: str):
        """
        Delete a video's embeddings, notes, and metadata.
        """

        # Delete transcript embeddings
        self.collection.delete(
            where={"video_id": video_id}
        )

        # Delete cached notes
        self.notes_collection.delete(
            ids=[video_id]
        )

        # Delete metadata
        self.metadata_collection.delete(
            ids=[video_id]
        )

        return True

    def get_video_metadata(self, video_id):

        result = self.metadata_collection.get(
            ids=[video_id]
        )

        if len(result["metadatas"]) == 0:
            return None

        return result["metadatas"][0]