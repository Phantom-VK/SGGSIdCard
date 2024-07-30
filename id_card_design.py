import os
from tkinter import messagebox

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from id_card_generator import reg_number, entry_name, entry_branch, entry_age, entry_dob, entry_blood_group, \
    entry_mobile_number, entry_address


def generate_id_card():
    registration_number = reg_number.get()
    name = entry_name.get()
    branch = entry_branch.get()
    age = entry_age.get()
    dob = entry_dob.get()
    blood_group = entry_blood_group.get()
    mobile_number = entry_mobile_number.get()
    address = entry_address.get()

    if not all([registration_number, name, branch, age, dob, blood_group, mobile_number, address]):
        messagebox.showerror("Input Error", "Please fill all fields")
        return

    # Create a blank ID card image
    image = Image.new('RGB', (400, 600), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Load fonts
    font_bold = ImageFont.truetype('arialbd.ttf', 20)
    font_regular = ImageFont.truetype('arial.ttf', 16)
    font_small = ImageFont.truetype('arial.ttf', 12)

    # Add Institute Name
    draw.text((20, 10), "SHRI GURU GOBIND SINGHJI", fill="blue", font=font_bold)
    draw.text((20, 40), "INSTITUTE OF ENGINEERING & TECHNOLOGY", fill="red", font=font_bold)

    # Add address
    draw.text((20, 70), "Vishnupuri, Nanded - 431606 (MS)", fill="black", font=font_regular)
    draw.text((20, 90), "Government Aided Autonomous Institute", fill="black", font=font_regular)

    # Add Identity Card title
    draw.text((150, 120), "IDENTITY CARD", fill="blue", font=font_bold)

    # Add student photo
    photo = Image.open("student_photo.png").resize((100, 120))
    image.paste(photo, (150, 140))

    # Add student details
    details = [
            ("Name:", name),
            ("Reg. No.:", registration_number),
            ("Branch:", branch),
            ("DOB:", dob),
            ("Mob. No.:", mobile_number)
    ]

    y = 280
    for label, value in details:
        draw.text((20, y), label, fill="black", font=font_regular)
        draw.text((150, y), value, fill="black", font=font_regular)
        y += 40

    # Add signatures
    draw.text((20, 460), "Student Sign.", fill="black", font=font_small)
    draw.text((300, 460), "Director Sign.", fill="black", font=font_small)

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Save the image as a temporary file
    temp_image_path = f"output/{name}_temp.png"
    image.save(temp_image_path)

    # Save as PDF
    pdf_path = f"output/{name}_id_card.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawImage("id_card.png", 100, 400, width=400, height=300)
    c.save()

    # Remove the temporary image file
    os.remove(temp_image_path)

    messagebox.showinfo("Success", f"ID Card generated and saved as {pdf_path}")
