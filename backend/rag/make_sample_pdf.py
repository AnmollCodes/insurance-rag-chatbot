from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os

# Get absolute path to the data directory (assuming structure: backend/rag/make_sample_pdf.py -> backend/data)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DEFAULT_PATH = os.path.join(DATA_DIR, "knowledge.pdf")

def make_pdf(path=DEFAULT_PATH):

    c = canvas.Canvas(path, pagesize=letter)
    text = c.beginText(40, 750)
    lines = [
        "Insurance Agency Customer Care Knowledge Base",
        "",
        "Q: How do I file a claim?",
        "A: Call our claims line or submit through the portal. Keep photos and receipts.",
        "",
        "Q: What is a deductible?",
        "A: The amount you pay out of pocket before insurance starts paying.",
        "",
        "Q: How do I add a driver to my auto policy?",
        "A: Provide name, DOB, license number, and effective date. We’ll send a quote.",
        "",
        "Q: What documents do you need for a new policy?",
        "A: ID proof, address proof, vehicle or home details, and prior insurance history.",
    ]
    for line in lines:
        text.textLine(line)
    c.drawText(text)
    c.showPage()
    c.save()

if __name__ == "__main__":
    make_pdf()
