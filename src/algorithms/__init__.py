from src.algorithms import base
from src.algorithms import bit_cycle, bit_xor, bit_not, bit_reverse
from src.algorithms import char_reverse

algorithm_dict = {
    'a': base.BaseAlgorithm(),
    'b': bit_cycle.BitCycleAlgorithm(),
    'c': bit_xor.BitXorAlgorithm(),
    'd': bit_not.BitNotAlgorithm(),
    'e': bit_reverse.BitReverseAlgorithm(),
    'f': char_reverse.CharReverseAlgorithm(),
}
