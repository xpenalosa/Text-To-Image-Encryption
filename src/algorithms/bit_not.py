from src.algorithms.base import BaseAlgorithm


class BitNotAlgorithm(BaseAlgorithm):

    def encode(self, text: bytes, **kwargs) -> bytes:
        return bytes([255 - t for t in text])

    def decode(self, text: bytes, **kwargs) -> bytes:
        # NOT is a symmetric operation
        return self.encode(text, **kwargs)
