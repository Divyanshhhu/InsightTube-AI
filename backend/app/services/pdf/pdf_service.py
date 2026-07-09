import os
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFService:

    @staticmethod
    def create_pdf(notes: str, video_id: str):

        os.makedirs("generated_pdfs", exist_ok=True)

        file_path = f"generated_pdfs/{video_id}.pdf"

        doc = SimpleDocTemplate(file_path)

        styles = getSampleStyleSheet()

        story = []

        for line in notes.split("\n"):

            if line.strip():

                line = escape(line)
                
                story.append(
                    Paragraph(line, styles["BodyText"])
                )

        doc.build(story)

        return file_path