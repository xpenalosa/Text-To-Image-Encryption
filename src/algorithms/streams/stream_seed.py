from src.algorithms.streams.base_stream import BaseStreamAlgorithm
from typing import Generator, Union
import random


class StreamSeedAlgorithm(BaseStreamAlgorithm):
    """Implementation of BaseStreamAlgorithm that streams the algorithm list.

    The class provides the option to apply an XOR operation to the input bytes
    with the algorithm list as the key. Since the algorithm list is already
    required in order to decode the message, it is preferred over prompting the
    user for another password.

    This class requires the following parameters:
        Algorithm list, provided by the user

    >>> ssa = StreamSeedAlgorithm()
    >>> # seed = 0, generates int(97)
    >>> ssa.encode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes(chr(0), "ascii"))
    b'\\x03'
    >>> # seed = 97, generates int(49)
    >>> ssa.encode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes("a", "ascii"))
    b'P'
    >>> ssa.decode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes(chr(0), "ascii"))
    b'\\x03'
    >>> ssa.decode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes("a", "ascii"))
    b'P'
    """

    def stream_values(self, **kwargs) -> Generator[int, Union[int, None], None]:
        """Create an integer generator that yields encoded byte values.

        The integer generator yields randomly generated integers in the range
        1-127, XOR'd with the input text in order. The random seed is the sum
        of each byte value of the algorithm key.

        :param kwargs: Optional parameters for the generator.
        :return: An integer generator.
        """
        next_val = yield
        key = kwargs.get("algorithms")
        seed = sum([b for b in key])
        random.seed(seed)
        while True:
            next_val = yield next_val ^ random.randint(0, 2**7-1)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
