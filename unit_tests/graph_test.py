#!/bin/python3

import sys
sys.path.append("..")

from prefix import adder_graph

g = adder_graph(4)

print(g.nodes)

g.add_node(0,1,'buffer_node')

print(len(g.nodes[1]))

print(g.nodes[1][0])

print()

print(g)
