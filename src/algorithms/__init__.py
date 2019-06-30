from src.algorithms import base
from src.algorithms import bit_cycle, bit_not, bit_reverse
from src.algorithms import char_reverse
from src.algorithms.streams import stream_seed, stream_rc4, stream_key

algo_dict = {
    'a': base.BaseAlgorithm(),
    'b': bit_cycle.BitCycleAlgorithm(),
    'c': bit_not.BitNotAlgorithm(),
    'd': bit_reverse.BitReverseAlgorithm(),
    'e': char_reverse.CharReverseAlgorithm(),
    'f': stream_key.StreamKeyAlgorithm(),
    'g': stream_seed.StreamSeedAlgorithm(),
    'h': stream_rc4.StreamRC4Algorithm(),
}
