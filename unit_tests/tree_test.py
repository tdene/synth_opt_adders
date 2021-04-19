#!/bin/python3

import sys
sys.path.append(".")

from adder_graph import adder_graph as graph
from adder_graph import adder_node as node
from adder_tree import adder_tree as tree
import networkx as nx
import pydot

g = tree(8)

#pg=nx.drawing.nx_pydot.to_pydot(g)
#pg.write_png('output.png',prog='neato')
