from typing import Tuple
import math
from random import choices as random_choices
from PIL import Image

padding_info_bytes = 2


def get_min_image_size(data: bytes) -> Tuple[int, int]:
    """ Find the minimum pixels required to create a square from an array.

    Calculates the minimum dimensions used to create a squared RGB image while
    taking into account the necessary padding and the bytes used to store the
    padding information. This function also takes into account the bytes needed
    to complete an RGB pixel if there are "stray" bytes.

    :param data: The array of bytes to calculate the dimensions from.
    :return: A two-value tuple containing the minimum amount of pixels per side.
    """
    data_bytes = len(data) + padding_info_bytes
    # Align to RGB pixel sizes
    pixel_bytes = data_bytes + data_bytes % 3

    short_side = math.floor(math.sqrt(pixel_bytes))
    long_side = math.ceil(pixel_bytes / short_side)
    return short_side, long_side


def bytes_to_image(data_bytes: bytes) -> Image:
    """Convert a bytes object into a PIL Image with RGB format

    This function takes a bytes object and builds an RGB image by assigning a
    byte to a color band of a single pixel: Every 3 bytes of data form a single
    pixel in the image.

    In order to create a (more or less) compact image, the data is rear-padded
    with bytes sampled from the same data, seamlessly merging with the possible
    created colors. This allows for the image to maintain a squared shape and
    make it easier to visualize. So as to keep track of the padded bytes, a
    certain amount of bytes are added to the beginning of the data. The value
    obtained from these bytes indicate how many bytes were added at the end of
    the input data, making it possible to crop accurately when trying to decode.

    The amount of bytes that contain the number of padded bytes is defined at
    the top of this file.

    :param data_bytes: The bytes object to convert.
    :return: A PIL.Image with RGB format.
    """
    # Obtain squared dimensions
    short_side, long_side = get_min_image_size(data_bytes)
    # Calculate necessary padding bytes
    padding_bytes = short_side * long_side * 3 - len(data_bytes) - padding_info_bytes

    # N bytes of padding at most
    if padding_bytes > 2**(7*padding_info_bytes) - 1:
        raise ValueError("Text is too long to be encoded in an image")

    # Add padding behind text data
    pad_bytes = random_choices(data_bytes, k=padding_bytes)
    for pad_byte in pad_bytes:
        data_bytes += bytes(chr(pad_byte), "ascii")

    # Add padding info in front of padded data
    padding_info = []
    # Split padding into N bytes
    for i in range(padding_info_bytes):
        padding_info.append(bytes(chr(padding_bytes & (2**7-1)), "ascii"))
        padding_bytes = padding_bytes >> 7
    # Add LSB to the front iteratively
    for pad_info in padding_info:
        data_bytes = pad_info + data_bytes

    image = Image.frombytes("RGB", (short_side, long_side), data_bytes)
    return image


def image_to_bytes(image: Image) -> bytes:
    """Recover the bytes object used to create a PIL Image with RGB format.

    Follows the procedure defined in bytes_to_image, but in inverse order:
    The padding is removed from the Image object and the bytes are recovered
    through PIL's Image.tobytes() method.

    :param image: The PIL Image.
    :return: The bytes object used to create the input Image.
    """
    data_bytes = image.tobytes()

    # Rebuild padding value from first bytes
    padding = 0
    for i in range(padding_info_bytes):
        padding += data_bytes[i] << (padding_info_bytes - i - 1) * 7

    if padding:
        # Avoid negative zero padding value
        data_bytes = data_bytes[padding_info_bytes:-padding]
    else:
        data_bytes = data_bytes[padding_info_bytes:]

    return data_bytes
