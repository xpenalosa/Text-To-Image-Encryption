from typing import Tuple
import math
from random import choices as random_choices
from PIL import Image

padding_info_bytes = 2


def get_min_image_size(data: bytearray) -> Tuple[int, int]:
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


def bytes_to_image(data: bytearray) -> Image:
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

    :param data: The byte array object to convert.
    :return: A PIL.Image with RGB format.
    """
    # Obtain squared dimensions
    short_side, long_side = get_min_image_size(data)
    # Calculate necessary padding bytes
    pad_count = short_side * long_side * 3 - len(data) - padding_info_bytes

    # N bytes of padding at most
    if pad_count > 2**(8*padding_info_bytes) - 1:
        raise ValueError("Text is too long to be encoded in an image")

    # Create padding bytes from sample
    padding = bytearray()
    for byte in random_choices(data, k=pad_count):
        padding.append(byte)

    # Add padding info in front of padded data
    padding_info = bytearray()
    # Split padding into N bytes
    for i in range(padding_info_bytes):
        padding_info.append(pad_count & 255)
        pad_count = pad_count >> 8
    # Decreasing signifiance
    padding_info.reverse()

    # Merge byte arrays
    data = padding_info + data + padding

    image = Image.frombytes("RGB", (short_side, long_side), bytes(data))
    return image


def image_to_bytes(data: Image) -> bytearray:
    """Recover the bytes object used to create a PIL Image with RGB format.

    Follows the procedure defined in bytes_to_image, but in inverse order:
    The padding is removed from the Image object and the bytes are recovered
    through PIL's Image.tobytes() method.

    :param data: The PIL Image.
    :return: The byte array object used to create the input Image.
    """
    data_byte_arr = bytearray(data.tobytes())

    # Rebuild padding value from first bytes
    padding = 0
    for i in range(padding_info_bytes):
        print(data_byte_arr[i])
        padding += data_byte_arr[i] << (padding_info_bytes - i - 1) * 8

    print(padding)
    if padding:
        # Avoid negative zero padding value
        data_bytes = data_byte_arr[padding_info_bytes:-padding]
    else:
        data_bytes = data_byte_arr[padding_info_bytes:]

    return data_bytes
