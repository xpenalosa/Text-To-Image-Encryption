class BaseAlgorithm:

    def encode(self, text: bytes, **kwargs) -> bytes:
        """Encode the text using an arbitrary implementation."""
        return text

    def decode(self, text: bytes, **kwargs) -> bytes:
        """Decode the text using an arbitrary implementation."""
        return text
