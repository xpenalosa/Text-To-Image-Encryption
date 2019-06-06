from src.algorithms.base import BaseAlgorithm


class BitNotAlgorithm(BaseAlgorithm):
    """Implementation of BaseAlgorithm that encodes through the NOT operation.

    The class provides the option to apply a NOT operation to the input bytes.

    The decoding process uses the same NOT operation as it is symmetric.

    This class requires no parameters.
    """

    def encode(self, text: bytes, **kwargs) -> bytes:
        """Encode the text using a bit-wise NOT operation.

        Instead of using the NOT operator "~", subtracting the byte value from
        the maximum byte value (2^7-1 => 127) has been chosen as the class'
        implementation. The operation yields the same result and is easier to
        understand when displaying intermediate steps on the console, as the
        NOT operator outputs to console the two's complement of the value as if
        it were a signed byte.

        Instead, working with numbers in the range of 0..127 as an unsigned byte
        might prove to be easier to understand.

        :param text: The bytes object to encode.
        :param kwargs: See BitNotAlgorithm.
        :return: The encoded text, as a bytes object.
        """
        return bytes([127 - t for t in text])

    def decode(self, text: bytes, **kwargs) -> bytes:
        """Decode the text using a bit-wise NOT operation.

        Symmetric operation, see encode() for more information.

        :param text: The bytes object to decode.
        :param kwargs: See BitNotAlgorithm.
        :return: The decoded text, as a bytes object.
        """
        return self.encode(text, **kwargs)
