from PIL import Image, ImageDraw, ImageFont


def create_id_card(details):
    # Load the template
    template = Image.open("SGGSIdCard.png")
    draw = ImageDraw.Draw(template)

    # Load a font
    font = ImageFont.truetype("arial.ttf", 40)
    font2 = ImageFont.truetype("arial.ttf", 30)
    # getting details
    name = details["name"]
    reg_no = details["reg_no"]
    branch = details["branch"]
    dob = details["dob"]
    mob_no = details["mob_no"]

    name_width = font.getlength(name)

    # Calculate the x position to center the text
    card_width = 817
    x_position_student_name = (card_width - name_width) // 2
    x_position_other_details = 294

    # Draw name on ID card
    draw.text((x_position_student_name, 730), f"{name}", font=font, fill="red")
    draw.text((x_position_other_details, 805), f"{reg_no}", font=font2, fill="black")
    draw.text((x_position_other_details, 860), f"{branch}", font=font2, fill="black")
    draw.text((x_position_other_details, 995), f"{dob}", font=font2, fill="black")
    draw.text((x_position_other_details, 1058), f"{mob_no}", font=font2, fill="black")
    # Save the result
    output_path = f"output/{name}id_card.png"
    template.save(output_path)

    return output_path

# test_student_details = {
#     "name": "Vikramaditya Khupse",
#     "reg_no": "2023XYZ123",
#     "branch": "Computer Science",
#     "dob": "15/08/2000",
#     "mob_no": "9876543210"
# }
#
# # Usage example
# image_path = create_id_card(test_student_details)
# print(f"ID Card created at: {image_path}")
