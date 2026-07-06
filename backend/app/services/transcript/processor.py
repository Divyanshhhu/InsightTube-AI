class TranscriptProcessor:

    @staticmethod
    def to_text(transcript):

        return " ".join(
            segment["text"]
            for segment in transcript
        )