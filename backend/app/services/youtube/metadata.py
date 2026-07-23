import requests


class YouTubeMetadataService:

    @staticmethod
    def get_metadata(video_url: str, video_id: str):

        response = requests.get(
            "https://www.youtube.com/oembed",
            params={
                "url": video_url,
                "format": "json"
            }
        )

        response.raise_for_status()

        data = response.json()

        return {
            "title": data["title"],
            "channel": data["author_name"],
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        }