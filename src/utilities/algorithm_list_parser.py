from typing import Union


def get_algorithm_key(**kwargs) -> Union[chr, None]:
    algorithms = kwargs.get("algorithms", None)
    index = kwargs.get("index", None)
    if algorithms is None or index is None:
        return None
    return chr(algorithms[index])
