from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def convert_to_pdf(image_path):
    pdf_path = image_path.replace(".png", ".pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawImage(image_path, 100, 400, width=400, height=300)
    c.save()
