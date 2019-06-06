from src.algorithms.base import BaseAlgorithm


class BitXorAlgorithm(BaseAlgorithm):
    """Implementation of BaseAlgorithm that encodes through XOR operations.

    The class provides the option to apply an XOR operation to the input bytes
    with the algorithm list as the key. Since the algorithm list is already
    required in order to decode the message, it is preferred over prompting the
    user for another password.

    The decoding process uses the same XOR operation as it is symmetric when
    using the same key.

    This class requires the following parameters:
        Algorithm list, provided by the user
    """

    def encode(self, text: bytes, **kwargs) -> bytes:
        """Encode the text using a byte-wise XOR operation.

        The algorithm list is concatenated with itself until it matches the
        length of the text to encode. The text to encode and the key are zipped
        together and an XOR operation is performed on each of their bytes.

        :param text: The bytes object to encode.
        :param kwargs: See BitXorAlgorithm.
        :return: The encoded text, as a bytes object.

        >>> bxa = BitXorAlgorithm()
        >>> bxa.encode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes(chr(0), "ascii"))
        b'a'
        >>> bxa.encode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes("a", "ascii"))
        b'\\x00'
        """
        key = kwargs.get("algorithms")
        # Copy to at least text size
        if len(key) < len(text):
            key = key * (len(text) // len(key) + 1)
        # Crop to text size
        key = key[:len(text)]
        # Zip values and XOR each byte
        return bytes([t ^ k for t, k in zip(text, key)])

    def decode(self, text: bytes, **kwargs) -> bytes:
        """Decode the text using a byte-wise XOR operation.

        Symmetric operation, see encode() for more information.

        :param text: The bytes object to decode.
        :param kwargs: See BitXorAlgorithm.
        :return: The decoded text, as a bytes object.

        >>> bxa = BitXorAlgorithm()
        >>> bxa.decode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes(chr(0), "ascii"))
        b'a'
        >>> bxa.decode(
        ...     bytes("a", "ascii"),
        ...     algorithms=bytes("a", "ascii"))
        b'\\x00'
        """
        return self.encode(text, **kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
