from src.algorithms.base import BaseAlgorithm
from src.utilities import bytes_conversions, algorithm_list_parser


class BitCycleAlgorithm(BaseAlgorithm):
    """Implementation of BaseAlgorithm that encodes through left-cycling bits.

    The class provides the option to cycle the bits forming the text string an
    arbitrary amount of positions. The decoding process uses right-cycling as
    the inverse operation of left-cycling.
    """

    def __get_cycle_positions(self, **kwargs) -> int:
        """Determine the positions to shift based on the algorithm list.

        Looks for the current position in the algorithm list and tries to find
        a single-digit value on the next position. The digit represents the
        amount of bits to cycle. If no digit is found, defaults to 4 bits.

        :param kwargs: See BitCycleAlgorithm.
        :return: The amount of positions to cycle.
        """
        try:
            # Access next digit in algorithm list
            positions = int(algorithm_list_parser.get_algorithm_key(
                algorithms=kwargs.get("algorithms"),
                index=kwargs.get("index")+1))
        except ValueError:
            # Fall back to default value
            positions = 4
        return positions

    def encode(self, text: bytes, **kwargs) -> bytes:
        """Encode the text using the left-cycle algorithm at bit level.

        :param text: The text to encode.
        :param kwargs: See BitCycleAlgorithm.
        :return: The encoded text, as a bytes object.
        """
        # Format each byte as a concatenation of 8-bit padded values
        bit_list = bytes_conversions.bytes_to_bit_rep(text)

        positions = self.__get_cycle_positions(**kwargs)

        # Cycle first N bits
        bit_list = bit_list[positions:] + bit_list[:positions]

        # Reconstruct string and return
        return bytes_conversions.bit_rep_to_bytes(bit_list)

    def decode(self, text: bytes, **kwargs) -> bytes:
        """Decode the text using the right-cycle algorithm at bit level.

        :param text: The text to decode.
        :param kwargs: See BitCycleAlgorithm.
        :return: The decoded text, as a bytes object.
        """
        bit_list = bytes_conversions.bytes_to_bit_rep(text)

        positions = self.__get_cycle_positions(**kwargs)

        bit_list = bit_list[-positions:] + bit_list[:-positions]
        # Reconstruct string and return
        return bytes_conversions.bit_rep_to_bytes(bit_list)
