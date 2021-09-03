from PIL import Image, ImageFont, ImageDraw

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

import base64
from io import BytesIO

default_heading = "Certificate for Marriage"
default_lines = [
    "This certifies that",
    "Somesh Kar & Pulkit Garg",
    "were united in marriage",
    "at Marine Drive, Mumbai",
    "on the 19th day of July in the year 2021",
    "by Adolf Hitler"
]
default_qr_link = '2HyPunEH73PUdrFmEKUdaKPJajq11sB9uzzpVoaqkt6LZFthmysHKjRSkfb5icX9CXnKMpTopu9F2vymBWdV2qGt'

heading_font = ImageFont.truetype(
    './fonts/Inter Hinted for Windows/Desktop/Inter-Bold.ttf', 70)
normal_font = ImageFont.truetype(
    './fonts/Inter Hinted for Windows/Desktop/Inter-Regular.ttf', 40)


def make_certi(lines=default_lines, qr_link=default_qr_link, heading=default_heading):
    certi_template = Image.open('./templates/wedding-template.jpeg')
    draw = ImageDraw.Draw(certi_template)

    W, H = certi_template.width, certi_template.height
    # print(W, H)

    heading_w, heading_h = heading_font.getsize(heading)
    draw.text(((W - heading_w) / 2, 90), heading,
              (41, 119, 245), font=heading_font)

    i = 1
    for l in lines:
        w, h = normal_font.getsize(l)
        draw.text(((W - w) / 2, 240 + ((h + 10) * (i - 1))),
                  l, (47, 46, 65), font=normal_font)

        i += 1

    qr = qrcode.QRCode(box_size=3)
    qr.add_data(qr_link)
    img_qr = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(
    ), color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(41, 119, 245)))
    pos = (W - img_qr.width-135, H - img_qr.height-50)
    img_qr = img_qr.resize((150, 150), Image.ANTIALIAS)
    certi_template.paste(img_qr, pos)

    buffered = BytesIO()
    certi_template.save(buffered, format='PNG')

    img_str = base64.b64encode(buffered.getvalue())

    return img_str


test_lines = [
    "This certifies that",
    "Paheli & Boojho",
    "were united in marriage",
    "at Marine Drive, Mumbai",
    "on the 19th day of July in the year 2021",
    "by a cool guy"
]

# make_certi(test_lines)
