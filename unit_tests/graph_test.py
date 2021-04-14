#!/bin/python3

import sys
sys.path.append(".")

from prefix import adder_graph
from prefix import adder_node as node
import networkx as nx
import pydot

g = adder_graph(4)

g.add_node(node(0,0,'buffer_node'))
g.add_node(node(1,0,'buffer_node'))
g.add_node(node(0,1,'black'))
g.add_node(node(1,1,'black'))
g.add_node(node(0,2,'grey'))
g.add_node(node(1,2,'grey'))

g.add_edge(g[0,0],('y',0),g[0,1],('gin',0))
g.add_edge(g[0,0],('y',0),g[1,1],('gin',0))
g.add_edge(g.node_list[0][1],('y',0),g.node_list[1][1],('gin',1))

g.add_edge(g.node_list[1][0],('pout',0),g.node_list[2][0],('gin',1))
g.add_edge(g.node_list[1][0],('gout',0),g.node_list[2][1],('gin',0))

g.add_edge(g[1,1],('gout',0),g[1,2],('gin',0))
g.add_edge(g[1,1],('pout',0),g[1,2],('gin',1))

adj_list=g.adj[g[0,1]]
assert(g.node_list[2][0])
assert(g.node_list[2][1])

assert(g[0,1].outs['pout'][0]==3)
assert(g[0,2].ins['gin'][1]==3)

assert(adj_list[g[0,2]][0]['ins']==('pout',0))
assert(adj_list[g[1,2]][0]['outs']==('gin',0))

#pg=nx.drawing.nx_pydot.to_pydot(g)
#pg.write_png('output.png',prog='neato')
