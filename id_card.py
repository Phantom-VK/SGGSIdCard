from PIL import Image, ImageDraw, ImageFont


def create_id_card(details):
    # Load the template
    template = Image.open("student_photo.png")
    draw = ImageDraw.Draw(template)

    # Load a font
    font = ImageFont.truetype("arial.ttf", 16)

    # Details positions
    details_list = [
        ("Name:", details["name"]),
        ("Reg. No.:", details["reg_no"]),
        ("Branch:", details["branch"]),
        ("DOB:", details["dob"]),
        ("Mob. No.:", details["mob_no"])
    ]

    # Draw details on the template
    x, y = 100, 400
    for label, value in details_list:
        draw.text((x, y), f"{label} {value}", font=font, fill="black")
        y += 30

    # Save the result
    output_path = "output/id_card.png"
    template.save(output_path)

    return output_path
