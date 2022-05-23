from .YosysAdder import YosysAdder

class yosys_alu(YosysAdder):
    """Class that generates parallel prefix adder trees"""

    def __init__(self, width, network="ripple"):
        """Initializes a parallel prefix tree adder to be used by a Yosys $alu mapping pass

        Refer to the adder_tree's docstring for a full description.
        """
        super().__init__(width, network)

if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
