#!/bin/python3

import sys
sys.path.append("..")

from prefix import adder_graph
from prefix import adder_node as node
import networkx as nx
import pydot

g = adder_graph(4)

g.add_node(node(0,0,'buffer_node'))
g.add_node(node(1,0,'buffer_node'))
g.add_node(node(0,1,'black'))
g.add_node(node(0,2,'grey'))
g.add_node(node(1,2,'grey'))

g.add_edge(g.node_list[0][0],('y',0),g.node_list[1][0],('gin',0))
g.add_edge(g.node_list[1][0],('pout',0),g.node_list[2][0],('gin',1))
g.add_edge(g.node_list[1][0],('gout',0),g.node_list[2][1],('gin',0))

adj_list=g.adj[g.node_list[1][0]]
assert(g.node_list[2][0] in adj_list)
assert(g.node_list[2][1] in adj_list)

assert(g.node_list[1][0].outs['pout'][0]==g.node_list[2][0])
assert(g.node_list[2][0].ins['gin'][1]==g.node_list[1][0])

assert(adj_list[g.node_list[2][0]]['ins']==('pout',0))
assert(adj_list[g.node_list[2][1]]['outs']==('gin',0))

#pg=nx.drawing.nx_pydot.to_pydot(g)
#print(pg)
#pg.write_png('output.png',prog='neato')
