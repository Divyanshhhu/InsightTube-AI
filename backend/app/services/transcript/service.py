from youtube_transcript_api import YouTubeTranscriptApi


class TranscriptService:

    @staticmethod
    def get_transcript(video_id: str):
        api = YouTubeTranscriptApi()

        transcript_list = api.list(video_id)

        # Try manually created transcripts first
        try:
            transcript = transcript_list.find_transcript([
                "en",
                "en-US",
                "en-GB",
                "hi"
            ])
        except:
            # Fall back to generated transcripts
            transcript = transcript_list.find_generated_transcript([
                "en",
                "en-US",
                "en-GB",
                "hi"
            ])

        return transcript.fetch().to_raw_data()