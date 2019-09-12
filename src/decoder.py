from PIL import Image
from src import algorithms as algo
from src.utilities import image_conversions


def decode_text(text: bytes, algorithm_index: int,
                algorithm_list: bytes) -> bytes:
    """Encode a string with the algorithm specified.

    :param text: The text to encode.
    :param algorithm_index: The algorithm list index.
    :param algorithm_list: The list of algorithm identifiers.
    :return: The encoded text.
    """
    algorithm_id = chr(algorithm_list[algorithm_index])
    algorithm_object = algo.algo_dict.get(algorithm_id, algo.algo_dict.get('a'))
    return algorithm_object.decode(
        text, algorithms=algorithm_list, index=algorithm_index)


def decode_file(image_file: str, algorithm_list: bytes) -> bytes:
    """Read the contents of an image file and decode the contents through a
    series of string-modifying algorithms.

    :param image_file: The file to read contents from.
    :param algorithm_list: A list of algorithm identifiers.
    :return: The encoded text, prepended by the list of algorithm identifiers.
    """
    image = Image.open(image_file, "r")
    rand_msb_data = image_conversions.image_to_bytes(image)

    # Ignore randomized MSB in every byte
    encoded_data = bytes("", "ascii")
    for byte in rand_msb_data:
        encoded_data += bytes(chr(byte & 127), "ascii")

    # Run the algorithm list backwards
    decoded_text = decode_text(
        encoded_data, len(algorithm_list) - 1, algorithm_list)

    for i in range(len(algorithm_list) - 1, 0, -1):
        decoded_text = decode_text(decoded_text, i - 1, algorithm_list)

    return decoded_text


def print_help(exec_name: str) -> None:
    """Display help in console."""
    print(f"""
    Text to image encryption algorithm - Decoding
         
         Usage: python3 {exec_name} <file name> <password>

    The file to decode is expected to be an RGB image stored in PNG format
    (Portable Network Graphics).
    The password should match the one used in the encoding process. Please
    see the encoding script for a small tip on selecting the password. 
    """)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print_help(sys.argv[0])
    else:
        file_name = sys.argv[1]
        # Decode file contents
        decoded_data = decode_file(file_name, bytes(sys.argv[2], "ascii"))

        # Get input file path and name without the file extension
        file_id = ''.join(file_name.split(".")[:-1])
        with open(f"{file_id}.txt", "w") as f:
            f.write(decoded_data.decode("ascii"))
