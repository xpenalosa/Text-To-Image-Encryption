from src.algorithms.base import BaseAlgorithm


class CharReverseAlgorithm(BaseAlgorithm):
    """Implementation of BaseAlgorithm that encodes through reversal of bytes.

    The class provides the option to apply a byte-wise reversal operation to the
    input bytes.

    The decoding process uses the same operation as it is symmetric.

    This class requires no parameters.
    """

    def encode(self, text: bytes, **kwargs) -> bytes:
        """Encode the text using byte-wise reversal.

        Reverse the characters of the string.

        :param text: The bytes object to encode.
        :param kwargs: See CharReverseAlgorithm.
        :return: The encoded text, as a bytes object.
        """
        return text[::-1]

    def decode(self, text: bytes, **kwargs) -> bytes:
        """Decode the text using a bit-wise NOT operation.

        Symmetric operation, see encode() for more information.

        :param text: The bytes object to decode.
        :param kwargs: See BitReverseAlgorithm.
        :return: The decoded text, as a bytes object.
        """
        return self.encode(text, **kwargs)
