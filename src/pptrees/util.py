#!/bin/python3


def lg(x):
    """Returns the base-2 logarithm of x, rounded up"""
    return x.bit_length() - 1


def sub_brackets(x):
    """Reformats 'a[0]' to 'a_0'"""
    return x.replace("[", "_").replace("]", "")


def verso_pin(x):
    """Returns the verso version of a pin"""
    return x.replace("out", "in") if "out" in x else x.replace("in", "out")

def parse_net(x):
    """Converts a net's ID to its name in HDL

    These come in 3 possible flavors:
        - None (unassigned net) -> parsed to n0
        - Integer (assigned net) -> parsed to n`Integer
        - Hardcoded name ($net_name) -> parsed to net_name
    """
    if x is None:
        return "n0"
    if isinstance(x, int):
        return "n" + str(x)
    if "$" in x:
        return x.replace("$", "")
    raise TypeError("net stored in node {0} is invalid".format(repr(x)))

if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
