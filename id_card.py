import barcode
from PIL import Image, ImageDraw, ImageFont
from barcode.writer import ImageWriter
import segno


def create_id_card(student_details):
    # Load the template
    id_card_front = Image.open("idcard_front.png")
    front_draw = ImageDraw.Draw(id_card_front)

    id_card_back = Image.open("idcard_back.png")
    back_draw = ImageDraw.Draw(id_card_back)

    # Load a font
    font = ImageFont.truetype("arial.ttf", 40)
    font2 = ImageFont.truetype("arial.ttf", 30)
    # getting details
    name = student_details["name"]
    reg_no = student_details["reg_no"]
    branch = student_details["branch"]
    dob = student_details["dob"]
    parent_mob_no = student_details["parent_mob_no"]
    mob_no = student_details["mob_no"]
    address = student_details["address"]

    name_width = font.getlength(name)

    # Calculate the x position to center the text
    card_width = 817
    x_position_student_name = (card_width - name_width) // 2
    x_position_other_details = 294

    # Draw name on ID card
    front_draw.text((x_position_student_name, 730), f"{name}", font=font, fill="red")
    front_draw.text((x_position_other_details, 805), f"{reg_no}", font=font2, fill="black")
    front_draw.text((x_position_other_details, 860), f"{branch}", font=font2, fill="black")
    front_draw.text((x_position_other_details, 995), f"{dob}", font=font2, fill="black")
    front_draw.text((x_position_other_details, 1058), f"{mob_no}", font=font2, fill="black")

    # ID Card Back side content

    # Generating barcode
    barcode_img = Image.open(generate_barcode(reg_no))

    # generating qrcode
    # qrcode_img = Image.open(generate_qr_code(name.upper()+".Mobile.-"+mob_no+".Parent Mob.-"+parent_mob_no+"Address : "+address))
    # Adding barcode on back side of id card png
    id_card_back.paste(barcode_img, ((card_width - barcode_img.width) // 2, 610))
    # id_card_back.paste(qrcode_img, ((card_width - barcode_img.width) // 2, 700))

    address_lines = address.split(",")

    back_draw.text((60, 80),
                   f"Address:{','.join(address_lines[:len(address_lines) // 2])}\n{','.join(address_lines[len(address_lines) // 2:])}",
                   font=font2, fill="black")

    # Save the result
    output_path_front = f"output/{reg_no}id_card_front.png"
    id_card_front.save(output_path_front)
    output_path_back = f"output/{reg_no}id_card_back.png"
    id_card_back.save(output_path_back)

    return output_path_front, output_path_back


def generate_barcode(alphanum_string):
    options = {
        'module_width': 0.3,  # Width of each module (bar)
        'module_height': 7.0,  # Height of each module (bar)
        'quiet_zone': 1.0,  # Width of the quiet zone on each side
        'font_size': 0,  # Font size for the text below the barcode (0 to remove text)
        'text_distance': 0.0,  # Distance between the barcode and the text
        'background': 'white',  # Background color
        'foreground': 'black',  # Foreground color
        'write_text': False  # Whether to write the text below the barcode
    }

    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(alphanum_string, writer=ImageWriter())

    return barcode_instance.save("barcode", options=options)


# def generate_qr_code(alphanum_string):
#     qrcode = segno.make_qr(alphanum_string)
#     return qrcode.save("qrcode.png")


# example details
details = {
    "name": "Vikramaditya Khupse",
    "reg_no": "2022BIT052",
    "branch": "Information Technology",
    "dob": "25/05/2004",
    "mob_no": "853029251",
    "parent_mob_no": "9960515228",
    "address": "Shivram Nagar, Basmat Road,"
               "Parbhani, Parbhani, Parbhani 431 401"
}
create_id_card(details)
