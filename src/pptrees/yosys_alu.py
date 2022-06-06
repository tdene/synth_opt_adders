from .YosysAdder import YosysAdder


class yosys_alu(YosysAdder):
    """Class that generates parallel prefix adder trees"""

    def __init__(self, width, network="ripple"):
        """Initializes a parallel prefix tree adder to be used by a Yosys $alu mapping pass

        Refer to the adder_tree's docstring for a full description.
        """
        if network == "very_slow":
            network = "ripple"
        elif network == "slow":
            network = "brent-kung"
        elif network == "fast":
            network = "sklansky"
        elif network == "very_fast":
            network = "kogge-stone"
        super().__init__(width, alias=network)


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
