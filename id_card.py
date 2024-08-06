import barcode
from PIL import Image, ImageDraw, ImageFont
from barcode.writer import ImageWriter
import segno


def create_id_card(student_details):
    """
    Creates an ID card with the student's details, barcode, and QR code.

    Parameters:
        student_details (dict): Dictionary containing student's information.

    Returns:
        tuple: Paths to the saved front and back images of the ID card.
    """
    # Load the front and back template images
    id_card_front = Image.open("idcard_front.png")
    front_draw = ImageDraw.Draw(id_card_front)
    id_card_back = Image.open("idcard_back.png")
    back_draw = ImageDraw.Draw(id_card_back)

    # Load the font
    font = ImageFont.truetype("arial.ttf", 40)
    font2 = ImageFont.truetype("arial.ttf", 30)

    # Extract student details
    name = student_details["name"]
    reg_no = student_details["reg_no"]
    branch = student_details["branch"]
    dob = student_details["dob"]
    parent_mob_no = student_details["parent_mob_no"]
    mob_no = student_details["mob_no"]
    address = student_details["address"]

    # Calculate the width of the name text and position to center it
    name_width = font.getlength(name)
    card_width = 817
    x_position_student_name = (card_width - name_width) // 2
    x_position_other_details = 294

    # Draw text on the front of the ID card
    front_draw.text((x_position_student_name, 730), name, font=font, fill="red")
    front_draw.text((x_position_other_details, 805), reg_no, font=font2, fill="black")
    front_draw.text((x_position_other_details, 860), branch, font=font2, fill="black")
    front_draw.text((x_position_other_details, 995), dob, font=font2, fill="black")
    front_draw.text((x_position_other_details, 1058), mob_no, font=font2, fill="black")

    # Generate and add barcode and QR code to the back of the ID card
    barcode_path = generate_barcode(reg_no)
    barcode_img = Image.open(barcode_path)
    qrcode_path = generate_qr_code(f"{name.upper()}.Mobile.-{mob_no}.Parent Mob.-{parent_mob_no}.Address : {address}")
    qrcode_img = Image.open(qrcode_path)
    qrcode_img = qrcode_img.resize((300, 300))

    # Position the barcode and QR code on the back of the ID card
    id_card_back.paste(barcode_img, ((card_width - barcode_img.width) // 2, 610))
    id_card_back.paste(qrcode_img, ((card_width - qrcode_img.width) // 2, 750))

    # Format the address text and draw it on the back of the ID card
    address_lines = address.split(",")
    formatted_address = f"Address: {', '.join(address_lines[:len(address_lines) // 2])}\n{', '.join(address_lines[len(address_lines) // 2:])}"
    back_draw.text((60, 80), formatted_address, font=font2, fill="black")

    # Save the ID card images
    output_path_front = f"output/{reg_no}_id_card_front.png"
    id_card_front.save(output_path_front)
    output_path_back = f"output/{reg_no}_id_card_back.png"
    id_card_back.save(output_path_back)

    return output_path_front, output_path_back


def generate_barcode(data):
    """
    Generates a barcode for the given data.

    Parameters:
        data (str): The data to encode in the barcode.

    Returns:
        str: Path to the saved barcode image.
    """
    options = {
        'module_width': 0.3,
        'module_height': 7.0,
        'quiet_zone': 1.0,
        'font_size': 0,
        'text_distance': 0.0,
        'background': 'white',
        'foreground': 'black',
        'write_text': False
    }

    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(data, writer=ImageWriter())

    return barcode_instance.save("barcode", options=options)


def generate_qr_code(data):
    """
    Generates a QR code for the given data.

    Parameters:
        data (str): The data to encode in the QR code.

    Returns:
        str: Path to the saved QR code image.
    """
    qrcode = segno.make_qr(data)
    qrcode.save("qrcode.png")
    return "qrcode.png"


# Example usage
details = {
    "name": "Vikramaditya Khupse",
    "reg_no": "2022BIT052",
    "branch": "Information Technology",
    "dob": "25/05/2004",
    "mob_no": "853029251",
    "parent_mob_no": "9960515228",
    "address": "Shivram Nagar, Basmat Road, Parbhani, Parbhani, Parbhani 431 401"
}

create_id_card(details)
