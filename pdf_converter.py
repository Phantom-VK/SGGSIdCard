from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from PIL import Image
import os

def convert_to_pdf(front_image_path, back_image_path, name, output_path=None):
    # Get the Downloads folder path
    if os.name == 'nt':
        downloads_folder = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    else:
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Define the default output path if not provided
    if output_path is None:
        output_path = os.path.join(downloads_folder, f"{name}IDCard.pdf")

    # Create a canvas with the dimensions of the first image
    front_image = Image.open(front_image_path)
    front_width, front_height = front_image.size

    c = canvas.Canvas(output_path, pagesize=(front_width, front_height))

    # Draw the front image on the first page
    c.drawImage(front_image_path, 0, 0, width=front_width, height=front_height)
    c.showPage()  # End the current page

    # Draw the back image on the second page
    back_image = Image.open(back_image_path)
    back_width, back_height = back_image.size

    c.setPageSize((back_width, back_height))  # Set the page size to the back image dimensions
    c.drawImage(back_image_path, 0, 0, width=back_width, height=back_height)
    c.save()
