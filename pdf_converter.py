from reportlab.pdfgen import canvas


def convert_to_pdf(image_path, output_path="output/id_card.pdf"):
    c = canvas.Canvas(output_path)
    c.drawImage(image_path, 100, 400, width=400, height=300)
    c.save()
