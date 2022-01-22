import numpy as np
from PIL import Image

DELIMITER = "%h0w3"


def get_channels_count_for_mode(mode: str) -> int:
    if mode == 'RGB':
        return 3
    elif mode == 'RGBA':
        return 4
    else:
        raise NotImplementedError("the image must be in RGB or RGBA")


def encode(img: Image, message: str, output: str):
    if ".jpg" in output:
        ValueError("Output type must not be JPG to it's lossy nature")

    width, height = img.size
    img_arr = np.array(list(img.getdata()))
    channels = get_channels_count_for_mode(img.mode)

    message += DELIMITER
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    pixels = img_arr.size // channels
    if req_pixels > pixels:
        ValueError("The image is too small to encode the text")

    i = 0
    for p in range(pixels):
        for q in range(0, 3):
            if i < req_pixels:
                img_arr[p][q] = int(bin(img_arr[p][q])[2:9] + b_message[i], 2)
                i += 1

    img_arr = img_arr.reshape((height, width, channels))
    Image.fromarray(img_arr.astype('uint8'), img.mode).save(output, format="PNG")

    print("Image Encoded Successfully")


def decode(img: Image):
    img_arr = np.array(list(img.getdata()))
    channels = get_channels_count_for_mode(img.mode)

    total_pixels = img_arr.size // channels

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(img_arr[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == DELIMITER:
            break
        else:
            message += chr(int(hidden_bits[i], 2))

    if DELIMITER in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")
