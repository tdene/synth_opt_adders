#!/bin/python3

from pptrees.prefix_graph import prefix_node
from pptrees.modules import modules

n = prefix_node(0, 1, "ppa_grey")

assert n.x == 0
assert n.y == 1
assert n.m in modules
assert "pin" in n.ins
assert "gout" in n.outs
assert len(n.ins["gin"]) == 2
# print(n.hdl())
# n.flatten()
# print(n.hdl())
