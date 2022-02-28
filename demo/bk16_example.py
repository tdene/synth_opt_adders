#!/usr/bin/python3
from pptrees.prefix_graph import prefix_node as node
from pptrees.adder_tree import adder_tree as tree
from pptrees.util import lg

g = tree(16,"brent-kung")
g.hdl('bk16.vhd',language="vhdl")
g.recalc_weights()
worst_path_3 = g.longest_path()
g.add_block(*worst_path_3)
g.png('bk16.png')
g.hdl('bk16.v')
