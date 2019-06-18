class BaseAlgorithm:
    """Basic interface for the encoding and decoding algorithms in the project.

    The class will return the input text as-is, without performing any modifying
    operations, regardless of the method called.

    This class requires no parameters.
    """

    def encode(self, text: bytes, **kwargs) -> bytes:
        """Encode the text using an arbitrary implementation."""
        return text

    def decode(self, text: bytes, **kwargs) -> bytes:
        """Decode the text using an arbitrary implementation."""
        return text
