import random

from PIL import Image
import numpy as np

white_mask = [[0, 255, 0, 255], [255, 0, 255, 0]]
black_mask = [[0, 255, 255, 0], [255, 0, 0, 255]]


def pix_offset(x: int, y: int, stride: int) -> int:
    return y * stride + x


def encode(img: Image):
    if img.mode not in ['L', '1']:
        raise NotImplementedError("the image must be black and white")

    width, height = img.size
    scaled_width = width * 2
    img_arr = np.array(list(img.getdata()))

    shares = [np.ones(img_arr.size * 2), np.ones(img_arr.size * 2)]

    for x in range(width - 1):
        for y in range(height - 1):
            rnd_float = random.uniform(0, 1)
            offset = pix_offset(x, y, width)
            color = img_arr[offset]
            x_offsets = [x * 2, x * 2 + 1]

            mask_i = 1 if rnd_float > 0.5 else 0
            mask = white_mask[mask_i] if color == 255 else black_mask[mask_i]

            for mask_v, share_i, x_offset in zip(mask, [0, 0, 1, 1], x_offsets * 2):
                shares[share_i][pix_offset(x_offset, y, scaled_width)] = mask_v

    shares = [share.reshape((height, scaled_width)) for share in shares]

    Image.fromarray(shares[0].astype('uint8'), img.mode).save("share1.png", format="PNG")
    Image.fromarray(shares[1].astype('uint8'), img.mode).save("share2.png", format="PNG")


def decode(share1_f: str, share2_f: str, output: str):
    share1 = Image.open(share1_f, "r")
    share2 = Image.open(share2_f, "r")

    width, height = share1.size

    share1_arr = np.array(list(share1.getdata()))
    share2_arr = np.array(list(share2.getdata()))

    descaled_width = int(width / 2)

    img_arr = np.ones(height * descaled_width)

    for x in range(width - 1):
        for y in range(height - 1):
            share_colors = [
                share1_arr[pix_offset(x * 2, y, width)],
                share1_arr[pix_offset(x * 2 + 1, y, width)],
                share2_arr[pix_offset(x * 2, y, width)],
                share2_arr[pix_offset(x * 2 + 1, y, width)],
            ]

            offset = pix_offset(x, y, descaled_width)
            for white, black in zip(white_mask, black_mask):
                if white == share_colors:
                    img_arr[offset] = 255
                if black == share_colors:
                    img_arr[offset] = 0

    img = img_arr.reshape((descaled_width, height))

    Image.fromarray(img.astype('uint8'), share1.mode).save(output, format="PNG")
