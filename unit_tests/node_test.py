#!/bin/python3

from pptrees.ExpressionNone import ExpressionNode
from pptrees.modules import modules

n = prefix_node(0, "ppa_grey")

assert n.value in modules
assert "pin" in n.in_nets
assert "gout" in n.out_nets
assert len(n.ins["gin"]) == 2
# print(n.hdl())
# n.flatten()
# print(n.hdl())
