from typing import Tuple
import math
from random import choices as random_choices
from PIL import Image


def get_min_image_size(text: bytes) -> Tuple[int, int]:
    data_bytes = len(text) + 1  # Consider padding information byte
    pixel_bytes = data_bytes + data_bytes % 3

    short_side = math.floor(math.sqrt(pixel_bytes))
    long_side = math.ceil(pixel_bytes / short_side)
    return short_side, long_side


def bytes_to_image(text: bytes) -> Image:
    short_side, long_side = get_min_image_size(text)
    padding_bytes = short_side * long_side * 3 - len(text) - 1

    if padding_bytes > 2**8 - 1:
        raise ValueError("Text is too long to be encoded in an image")

    # Add padding information in front of text data
    data_bytes = bytes(chr(padding_bytes), "ascii") + text
    # Add padding behind text data
    pad_bytes = random_choices(text, k=padding_bytes)
    for pad_byte in pad_bytes:
        data_bytes += bytes(chr(pad_byte), "ascii")

    image = Image.frombytes("RGB", (short_side, long_side), data_bytes)
    return image


def image_to_bytes(image: Image) -> bytes:
    data_pixels = list(image.getdata())
    data_bytes = b''
    for pixel in data_pixels:
        for band in pixel:
            data_bytes += bytes(chr(band), "ascii")

    padding = data_bytes[0]
    if padding:
        data_bytes = data_bytes[1:-padding]
    else:
        data_bytes = data_bytes[1:]

    return data_bytes
