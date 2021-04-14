#!/bin/python3

import sys
sys.path.append(".")

from adder_graph import adder_graph
from adder_graph import adder_node as node
import networkx as nx
import pydot

g = adder_graph(4)

g.add_node(node(0,0,'buffer_node'),style='invis')
g.add_node(node(1,0,'buffer_node'))
g.add_node(node(0,1,'black'))
g.add_node(node(1,1,'black'))
g.add_node(node(0,2,'grey'))
g.add_node(node(1,2,'grey'))

g.add_edge(g[0,0],('y',0),g[0,1],('gin',0))
g.add_edge(g[0,0],('y',0),g[1,1],('gin',0))
g.add_edge(g[1,0],('y',0),g[1,1],('gin',1))

g.add_edge(g[0,1],('pout',0),g[0,2],('gin',1))
g.add_edge(g[0,1],('gout',0),g[1,2],('gin',0))

g.add_edge(g[1,1],('gout',0),g[1,2],('gin',0))
g.add_edge(g[1,1],('pout',0),g[1,2],('gin',1))

# Node connecting to two separate children via different ports
adj_list=g.adj[g[0,1]]
assert(g[0,2] in adj_list)
assert(g[1,2] in adj_list)

assert(g[0,1].outs['pout'][0]==3)
assert(g[0,2].ins['gin'][1]==3)

assert(adj_list[g[0,2]][0]['ins']==('pout',0))
assert(adj_list[g[1,2]][0]['outs']==('gin',0))

# Node connecting to child via multiple ports
adj_list=g.adj[g[1,1]]
assert(g[1,2] in adj_list)
assert(len(adj_list.keys())==1)

assert(adj_list[g[1,2]][0]['outs']!=adj_list[g[1,2]][1]['outs'])
assert(adj_list[g[1,2]][0]['ins']!=adj_list[g[1,2]][1]['ins'])

# Node connecting to two separate children via same port
adj_list=g.adj[g[0,0]]
assert(g[0,1] in adj_list)
assert(g[1,1] in adj_list)

assert(adj_list[g[0,1]][0]['ins']==adj_list[g[1,1]][0]['ins'])

#pg=nx.drawing.nx_pydot.to_pydot(g)
#pg.write_png('output.png',prog='neato')
