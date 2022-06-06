from .AdderForest import AdderForest as AdderForest


class adder_tree(AdderForest):
    """Class that generates parallel prefix adder trees"""

    def __init__(self, width, network="ripple"):

        super().__init__(width, alias=network)


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
