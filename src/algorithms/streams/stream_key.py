from src.algorithms.streams.base_stream import BaseStreamAlgorithm
from typing import Generator, Optional


class StreamKeyAlgorithm(BaseStreamAlgorithm):
    """Implementation of BaseStreamAlgorithm that streams the algorithm list.

    The class provides the option to apply an XOR operation to the input bytes
    with the algorithm list as the key. Since the algorithm list is already
    required in order to decode the message, it is preferred over prompting the
    user for another password.

    This class requires the following parameters:
        Algorithm list, provided by the user

    >>> ska = StreamKeyAlgorithm()
    >>> ska.encode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes(chr(0), "ascii"))
    b'a'
    >>> ska.encode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes("a", "ascii"))
    b'\\x00'
    >>> ska.decode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes(chr(0), "ascii"))
    b'a'
    >>> ska.decode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes("a", "ascii"))
    b'\\x00'
    """

    def stream_values(self, **kwargs) -> Generator[int, Optional[int], None]:
        """Create an integer generator that yields encoded byte values.

        The integer generator yields the byte values of each character in the
        key, XOR'd with the input text in order. If the key is shorter, it is
        repeated.

        :param kwargs: Optional parameters for the generator.
        :return: An integer generator.
        """
        next_val = yield -1
        key = kwargs["algorithms"]
        i = 0
        while True:
            i = (i + 1) % len(key)
            next_val = yield next_val ^ key[i]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
