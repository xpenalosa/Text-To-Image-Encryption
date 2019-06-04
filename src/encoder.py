from src import algorithms as algo


def encode_text(text: bytes, algorithm_index: int,
                algorithm_list: bytes = b'0') -> bytes:
    """Encode a string with the algorithm specified.

    :param text: The text to encode.
    :param algorithm_index: The algorithm list index.
    :param algorithm_list: The list of algorithm identifiers.
    :return: The encoded text.
    """
    return algo.algo_dict.get(algorithm_list[algorithm_index]).encode(
        text, algorithms=algorithm_list, index=algorithm_index)


def encode_file(text_file: str, algorithm_list: str = '0') -> str:
    """Read the contents of a text file and encode the contents through a
    series of string-modifying algorithms.

    :param text_file: The file to read contents from.
    :param algorithm_list: A list of algorithm identifiers.
    :return: The encoded text, prepended by the list of algorithm identifiers.
    """
    with open(text_file, "rb") as f:
        raw_text = f.read()

    encoded_text = encode_text(raw_text, algorithm_list[0])
    for algorithm in algorithm_list[1:]:
        encoded_text = encode_text(encoded_text, algorithm)

    return f"{algorithm_list}_{encoded_text}"


def print_help():
    """Display help in console."""
    pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print_help()
    else:
        encoded_data = encode_file(sys.argv[1], sys.argv[2])
        print(encoded_data)
