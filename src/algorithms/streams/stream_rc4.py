from src.algorithms.streams.base_stream import BaseStreamAlgorithm
from typing import Generator, Union, List


class StreamRC4Algorithm(BaseStreamAlgorithm):
    """Implementation of BaseStreamAlgorithm using the RC4 algorithm.

    The class implements the RC4 (Rivest Cipher 4) algorithm.

    This class requires the following parameters:
        Algorithm list, provided by the user

    >>> src4a = StreamRC4Algorithm()
    >>> # seed = 0, generates int(97)
    >>> src4a.encode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes(chr(0), "ascii"))
    b'?'
    >>> # seed = 97, generates int(49)
    >>> src4a.encode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes("a", "ascii"))
    b'q'
    >>> src4a.decode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes(chr(0), "ascii"))
    b'?'
    >>> src4a.decode(
    ...     bytes("a", "ascii"),
    ...     algorithms=bytes("a", "ascii"))
    b'q'
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
        s_boxes = self.key_scheduling(kwargs.get("algorithms"))

        i, j = 0, 0
        while True:
            i = (i + 1) % 256
            j = (j + s_boxes[i]) % 256

            tmp = s_boxes[j]
            s_boxes[j] = s_boxes[i]
            s_boxes[i] = tmp

            # Adapt K to ascii encoding (7 bits)
            k = s_boxes[(s_boxes[i] + s_boxes[j]) % 256] % 128

            next_val = yield next_val ^ k

    def key_scheduling(self, algorithm_list: bytes) -> List[int]:
        """Key scheduling algorithm for the RC4 implementation.

        :param algorithm_list:
        :return:
        """
        key_length = len(algorithm_list)
        s_boxes = [i for i in range(0, 256)]
        j = 0
        for i in range(0, 256):
            j = (j + s_boxes[i] + algorithm_list[i % key_length]) % 256
            tmp = s_boxes[j]
            s_boxes[j] = s_boxes[i]
            s_boxes[i] = tmp
        return s_boxes


if __name__ == "__main__":
    import doctest
    doctest.testmod()
