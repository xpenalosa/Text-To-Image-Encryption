from src.algorithms.base import BaseAlgorithm
from src.utilities import bytes_conversions


class BitReverseAlgorithm(BaseAlgorithm):
    """Implementation of BaseAlgorithm that encodes through reversal of bits.

    The class provides the option to apply a bit-wise reversal operation to the
    input bytes.

    The decoding process uses the same operation as it is symmetric.

    This class requires no parameters.
    """

    def encode(self, text: bytes, **kwargs) -> bytes:
        """Encode the text using bit-wise reversal.

        After converting the bytes object to its binary representation in a
        string, reverse the characters of the string and rebuild the bytes
        object.

        :param text: The bytes object to encode.
        :param kwargs: See BitReverseAlgorithm.
        :return: The encoded text, as a bytes object.
        """
        # Format each byte as a concatenation of 8-bit padded values
        bit_list = bytes_conversions.bytes_to_bit_rep(text)
        # Reconstruct reversed string and return
        return bytes_conversions.bit_rep_to_bytes(bit_list[::-1])

    def decode(self, text: bytes, **kwargs) -> bytes:
        """Decode the text using a bit-wise NOT operation.

        Symmetric operation, see encode() for more information.

        :param text: The bytes object to decode.
        :param kwargs: See BitReverseAlgorithm.
        :return: The decoded text, as a bytes object.
        """
        return self.encode(text, **kwargs)
