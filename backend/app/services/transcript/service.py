from youtube_transcript_api import YouTubeTranscriptApi


class TranscriptService:

    @staticmethod
    def get_transcript(video_id: str):

        api = YouTubeTranscriptApi()

        transcript_list = api.list(video_id)

        try:
            transcript = transcript_list.find_transcript(
                ["en", "hi"]
            )
        except:
            transcript = transcript_list.find_generated_transcript(
                ["en", "hi"]
            )

        return transcript.fetch().to_raw_data()