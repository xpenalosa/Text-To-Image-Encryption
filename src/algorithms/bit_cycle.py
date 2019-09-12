from src.algorithms.base import BaseAlgorithm
from src.utilities import bytes_conversions, algorithm_list_parser


class BitCycleAlgorithm(BaseAlgorithm):
    """Implementation of BaseAlgorithm that encodes through left-cycling bits.

    The class provides the option to cycle the bits forming the text string an
    arbitrary amount of positions. The decoding process uses right-cycling as
    the inverse operation of left-cycling.

    This class requires the following parameters:
        Algorithm list, provided by the user
        Algorithm index, calculated automatically
    """

    def __get_cycle_positions(self, **kwargs) -> int:
        """Determine the positions to shift based on the algorithm list.

        Looks for the current position in the algorithm list and tries to find
        a single-digit value (1-9) on the next position. The digit represents
        the amount of bits to cycle. If no digit is found, defaults to 4 bits.
        If digit found is 0, defaults to 1.

        :param kwargs: See BitCycleAlgorithm.
        :return: The amount of positions to cycle.

        >>> bca = BitCycleAlgorithm()
        >>> bca._BitCycleAlgorithm__get_cycle_positions(
        ...     algorithms=bytes("b1", "ascii"),
        ...     index=0)
        1
        >>> bca = BitCycleAlgorithm()
        >>> bca._BitCycleAlgorithm__get_cycle_positions(
        ...     algorithms=bytes("b0", "ascii"),
        ...     index=0)
        1
        >>> bca = BitCycleAlgorithm()
        >>> bca._BitCycleAlgorithm__get_cycle_positions(
        ...     algorithms=bytes("acdb5ef", "ascii"),
        ...     index=3)
        5
        >>> bca = BitCycleAlgorithm()
        >>> bca._BitCycleAlgorithm__get_cycle_positions(
        ...     algorithms=bytes("a", "ascii"),
        ...     index=10)
        4
        >>> bca = BitCycleAlgorithm()
        >>> bca._BitCycleAlgorithm__get_cycle_positions(
        ...     algorithms=bytes("abc", "ascii"),
        ...     index=1)
        4
        """
        try:
            # Access next digit in algorithm list
            positions = int(algorithm_list_parser.get_algorithm_key(
                algorithms=kwargs["algorithms"],
                index=kwargs["index"] + 1))
        except (ValueError, IndexError):
            # Fall back to default value
            positions = 4
        return max(positions, 1)

    def encode(self, text: bytes, **kwargs) -> bytes:
        """Encode the text using the bit-wise left-cycle algorithm.

        :param text: The text to encode.
        :param kwargs: See BitCycleAlgorithm.
        :return: The encoded text, as a bytes object.

        >>> bca = BitCycleAlgorithm()
        >>> bca.encode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes(chr(0)+"1", "ascii"),
        ...     index=0)
        b'C'
        >>> bca.encode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes(chr(0)+"7", "ascii"),
        ...     index=0)
        b'a'
        >>> bca.encode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes(chr(0), "ascii"),
        ...     index=0)
        b'\\x1c'
        """
        # Format each byte as a concatenation of 7-bit padded values
        bit_list = bytes_conversions.bytes_to_bit_rep(text)

        positions = self.__get_cycle_positions(**kwargs)
        # Cycle first N bits
        bit_list = bit_list[positions:] + bit_list[:positions]

        # Reconstruct string and return
        return bytes_conversions.bit_rep_to_bytes(bit_list)

    def decode(self, text: bytes, **kwargs) -> bytes:
        """Decode the text using the bit-wise right-cycle algorithm.

        :param text: The text to decode.
        :param kwargs: See BitCycleAlgorithm.
        :return: The decoded text, as a bytes object.

        >>> bca = BitCycleAlgorithm()
        >>> bca.decode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes(chr(0)+"1", "ascii"),
        ...     index=0)
        b'p'
        >>> bca.decode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes(chr(0)+"7", "ascii"),
        ...     index=0)
        b'a'
        >>> bca.decode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes(chr(0), "ascii"),
        ...     index=0)
        b'\\x0e'
        """
        bit_list = bytes_conversions.bytes_to_bit_rep(text)

        positions = self.__get_cycle_positions(**kwargs)

        bit_list = bit_list[-positions:] + bit_list[:-positions]
        # Reconstruct string and return
        return bytes_conversions.bit_rep_to_bytes(bit_list)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
