from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from PIL import Image
import os


def convert_to_pdf(image_path, name, output_path=None):
    # Get the Downloads folder path
    if os.name == 'nt':
        downloads_folder = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    else:
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Define the default output path if not provided
    if output_path is None:
        output_path = os.path.join(downloads_folder, f"{name}IDCard.pdf")

    # Open the image to get its dimensions
    image = Image.open(image_path)
    width, height = image.size

    # Create a canvas with the dimensions of the image
    c = canvas.Canvas(output_path, pagesize=(width, height))
    c.drawImage(image_path, 0, 0, width=width, height=height)
    c.save()


# Example usage:
# convert_to_pdf("path/to/your/image.png")
