from src.algorithms.base import BaseAlgorithm


class BitXorAlgorithm(BaseAlgorithm):

    def encode(self, text: bytes, **kwargs) -> bytes:
        # Obtain XOR key
        key = kwargs.get("algorithm_list")
        # Pad to at least text size
        if len(key) < len(text):
            key = key * (len(text) // len(key) + 1)
        # Crop to text size
        key = key[:len(text)]
        # Zip values and XOR each byte
        return bytes([t ^ k for t, k in zip(text, key)])

    def decode(self, text: bytes, **kwargs) -> bytes:
        # XOR is a symmetric operation
        return self.encode(text, **kwargs)
