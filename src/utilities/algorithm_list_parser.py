def get_algorithm_key(**kwargs) -> str:
    algorithms = kwargs["algorithms"]
    index = kwargs["index"]
    return str(algorithms[index])
