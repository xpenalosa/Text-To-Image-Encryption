from src import algorithms as algo
from src.utilities import image_conversions
from random import randrange


def encode_text(text: bytes, algorithm_index: int,
                algorithm_list: bytes) -> bytes:
    """Encode a string with the algorithm specified.

    :param text: The text to encode.
    :param algorithm_index: The algorithm list index.
    :param algorithm_list: The list of algorithm identifiers.
    :return: The encoded text.
    """
    algorithm_id = chr(algorithm_list[algorithm_index])
    algorithm_object = algo.algo_dict.get(algorithm_id, algo.algo_dict.get('a'))
    return algorithm_object.encode(
        text, algorithms=algorithm_list, index=algorithm_index)


def encode_file(text_file: str, algorithm_list: bytes) -> bytearray:
    """Read the contents of a text file and encode the contents through a
    series of string-modifying algorithms.

    :param text_file: The file to read contents from.
    :param algorithm_list: A list of algorithm identifiers.
    :return: The encoded text, prepended by the list of algorithm identifiers.
    """
    with open(text_file, "rb") as f:
        raw_text = f.read()

    encoded_text = encode_text(raw_text, 0, algorithm_list)
    for i in range(1, len(algorithm_list)):
        encoded_text = encode_text(encoded_text, i, algorithm_list)

    # Randomize MSB on all bytes (Ascii -> UTF8 extra bit)
    rand_msb_text = bytearray()
    for byte in encoded_text:
        # print(byte)
        rand_msb_text.append(randrange(0, 2) * 128 + byte)

    return rand_msb_text


def print_help(exec_name: str) -> None:
    """Display help in console."""
    print(f"""
    Text to image encryption algorithm - Encoding
         
         Usage: python3 {exec_name} <file name> <password>

    The file to encode is expected to be in plain-text, and it should have
    a file extension (.txt, .md, ...) to prevent read/write errors.
    The password can be manually built from the list indicated in the file
    "Text-To-ImageEncryption/Algorithm_list.txt" or input blindly, but you
    should write it down for the decoding process.
    """)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print_help(sys.argv[0])
    else:
        file_name = sys.argv[1]
        # Encode file contents
        encoded_data = encode_file(file_name, bytes(sys.argv[2], "ascii"))
        # Manipulate encoded data into an RGB image
        image = image_conversions.bytes_to_image(encoded_data)

        # Get input file path and name without the file extension
        file_id = ''.join(file_name.split(".")[:-1])
        # Store output image as PNG
        image.save(f"{file_id}.png", "PNG")
