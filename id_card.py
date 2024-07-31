from PIL import Image, ImageDraw, ImageFont
from pdf_converter import convert_to_pdf


def create_id_card(details):
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
    photo = Image.open(details["photo_path"]).resize((100, 120))
    image.paste(photo, (150, 140))

    # Add student details
    y = 280
    details_list = [
        ("Name:", details["name"]),
        ("Reg. No.:", details["reg_no"]),
        ("Branch:", details["branch"]),
        ("DOB:", details["dob"]),
        ("Mob. No.:", details["mob_no"])
    ]

    for label, value in details_list:
        draw.text((20, y), label, fill="black", font=font_regular)
        draw.text((150, y), value, fill="black", font=font_regular)
        y += 40

    # Add signatures
    draw.text((20, 460), "Student Sign.", fill="black", font=font_small)
    draw.text((300, 460), "Director Sign.", fill="black", font=font_small)

    # Save the image
    image_path = f"{details['name']}_id_card.png"
    image.save(image_path)

    # Convert the image to a PDF
    convert_to_pdf(image_path)
