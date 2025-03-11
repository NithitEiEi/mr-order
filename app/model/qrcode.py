import io
from PIL import Image
from pyzbar.pyzbar import decode

def check_qrcode(image):

    img = Image.open(io.BytesIO(image))

    decoded_objects = decode(img)

    if decoded_objects:
        return [obj.data.decode('utf-8') for obj in decoded_objects]
    else:
        return []