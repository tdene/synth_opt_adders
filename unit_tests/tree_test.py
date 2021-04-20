#!/bin/python3

import sys
sys.path.append(".")

from adder_graph import adder_graph as graph
from adder_graph import adder_node as node
from adder_tree import adder_tree as tree

g = tree(8)
assert(g._checkLF(7,7)==(g[7,7],g[6,6]))
assert(g._checkLT(7,7)==(g[7,7],g[6,6]))
assert(g._checkLT(3)==(g[3,3],g[2,2]))
assert(g._checkLF(2,2)==(None,None))
assert(g._checkLT(2)==(None,None))

assert(g._checkFT(7)==(None,None))
assert(g._checkTF(7)==(None,None))
assert(g._checkFL(7)==(None,None))
assert(g._checkTL(7)==(None,None))

assert(len(g.node_list)==9)
g.trim_layer()
assert(len(g.node_list)==9)

def TF_test():
    g.LF(7)
    g.compress()
    g.LF(7)
    g.compress()
    g.LF(6)
    g.compress()
    g.TL(7,2)
    g.reduce_idem()
    g.png('1.png')
    g.LT(7,3)
    g.TL(7,2)
    g.reduce_idem()
    g.png('2.png')

def sklanksy():
    g.LF(7)
    g.compress()
    g.LF(5)
    g.compress()
    g.LF(3)
    g.compress()
    g.LF(7)
    g.compress()
    g.LF(6)
    g.compress()
    g.trim_layer()
    g.trim_layer()
    g.trim_layer()
    g.trim_layer()

def reverse_sklansky():
    g.add_layer()
    g.add_layer()
    g.add_layer()
    g.add_layer()
    g.FL(6)
    g.reduce_idem()
    g.FL(7)
    g.reduce_idem()
    g.FL(7)
    g.reduce_idem()
    g.shift_node(g[7,5],g.bot)
    g.shift_node(g[6,4],g.bot)
    g.FL(5)
    g.reduce_idem()
    g.shift_node(g[7,6],g.bot)
    g.shift_node(g[6,5],g.bot)
    g.shift_node(g[5,4],g.bot)
    g.shift_node(g[4,3],g.bot)
    g.FL(3)
    g.reduce_idem()
