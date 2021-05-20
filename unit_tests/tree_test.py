#!/bin/python3

import sys
sys.path.append(".")

from adder_graph import adder_node as node
from adder_tree import adder_tree as tree

n = 8

g = tree(n)
#assert(g._checkLF(7,7)==(g[7,7],g[6,6],[g[7,5]],[g[6,4]]))
assert(g._checkLT(7,7)==(g[7,7],g[6,6]))
assert(g._checkLT(3)==(g[3,3],g[2,2]))
#assert(g._checkLF(2,2)==(g[2,2],g[1,1],[g[2,1]],[g[1,0]]))
assert(g._checkLT(2)==(None,None))

assert(g._checkFT(7)==(None,None,None,None))
assert(g._checkTF(7)==(None,None))
assert(g._checkFL(7,7)==(g[7,7],g[6,7]))
assert(g._checkTL(7)==(None,None))

assert(len(g.node_list)==9)
g.trim_layer()
assert(len(g.node_list)==9)

def lg(x):
    return x.bit_length()-1

def sklansky():
    # Start from ripple-carry
    # Reduce layer by layer
    # From a total of n layers
    # To a total of lg(n) layers
    g.LF(3)
    for a in range(lg(n)+1,n):
        g.batch_transform('LF',a,n)
        g.png("{0}.png".format(a-lg(n)))
    g.png('sklansky.png')

def koggestone():
    # Start from ripple-carry
    # Reduce 1st layer
    g.LT(7)
    g.png('1.png')

    # Reduce 2nd layer
    g.LT(6)
    g.LT(7)
    g.png('2.png')

    # Reduce 3rd layer
    g.LT(5)
    g.LT(6)
    g.LT(7)
    g.png('3.png')

    # Reduce 4th layer
    g.LT(3)
    g.LT(4)
    g.LT(5)
    g.LT(6)
    g.LT(7)
    g.png('4.png')
    g.png('koggestone.png')

def brentkung():
    g.LF(3)
    # Start from ripple-carry
    # Arrive at Sklansky
    g.png('1.png')

    g.FL(4)
    g.FL(5)
    g.FL(6)

    g.FL(2)
    g.FL(4)
    g.FL(6)
    g.png('2.png')

    g.png('3.png')
    for a in range(lg(n)+1,n):
        g.batch_transform('LF',a,n)
    g.png('4.png')

    # Reduce 4th layer
    g.png('brentkung.png')

def demo():
    g=tree(8)
    g.png('00.png')
    g.png('01.png')
    g.png('02.png')
    g.png('03.png')
    g.png('04.png')
    g.LF(7)
    g.compress()
    g.png('05.png')
    g.LF(5)
    g.compress()
    g.png('06.png')
    g.LF(3)
    g.compress()
    g.png('07.png')
    g.LF(7)
    g.png('08.png')
    g.trim_layer()
    g.trim_layer()
    g.png('09.png')
    g.shift_node(g[4,3],g.bot)
    g.shift_node(g[4,4],g.bot)
    g.shift_node(g[6,4],g.bot)
    g.shift_node(g[5,3],g.bot)
    g.shift_node(g[2,2],g.bot)
    g.shift_node(g[2,3],g.bot)
    g.shift_node(g[2,4],g.bot)
    g.png('10.png')
    g.png('11.png')
    g.png('12.png')
    g.png('13.png')
    g.png('14.png')
    g.LF(6)
    g.png('15.png')
    g.compress()
    g.png('16.png')
    g.png('17.png')
    g.png('18.png')
    g.png('19.png')
    g.png('20.png')
    g.FT(7)
    g.png('21.png')
    g.FT(6)
    g.png('22.png')
    g.FT(7,2)
    g.png('23.png')
    g.FT(5,2)
    g.png('24.png')
    g.FT(3,2)
    g.png('25.png')
    g.FT(7)
    g.png('26.png')
    g.FT(5)
    g.png('27.png')
    g.png('28.png')
    g.png('29.png')
    g.png('30.png')
    g.png('31.png')
    g.TF(7,3)
    g.png('32.png')
    g.TF(5,3)
    g.png('33.png')
    g.TF(7,2)
    g.remove_node(g[6,1])
    g.add_node(node(6,1,'buffer_node'))
    g.png('34.png')
    g.TF(5,2)
    g.remove_node(g[4,1])
    g.add_node(node(4,1,'buffer_node'))
    g.png('35.png')
    g.TF(3,2)
    g.remove_node(g[2,1])
    g.add_node(node(2,1,'buffer_node'))
    g.png('36.png')
    g.png('37.png')
    g.png('38.png')
    g.png('39.png')
    g.png('40.png')

def LFT():
    g=tree(4)
    g.png('L.png')
    g.LF(3)
    g.png('F.png')
    g.FT(3)
    g.png('T.png')

def test():
    g.FT(5)
    g.FT(6)
    g.FT(7)
    g.FT(5)
    g.FT(5)
    g.FT(3)
    g.FT(7)
    g.FT(6)
    g.FT(5)
    g.TF(7)
    g.TF(6)
    g.TF(5)
    g.FT(5)
    g.FT(6)
    g.FT(7)

def test2():
    g.png('1.png')
    g.LF(7)
    g.LF(6)
    g.LF(7)
    g.LF(5)
    g.LF(6)
    g.LF(7)
    g.LF(3)
    g.png('2.png')
    g.FL(3)
    g.FL(7)
    g.FL(6)
    g.FL(5)
    g.FL(7)
    g.FL(6)
    g.FL(7)
    g.png('3.png')

brentkung()

# Re-calculate the tree
pre_processing = g.node_list[0]
for n in pre_processing:
    g.walk_downstream(n,fun=g._recalc_pg)

# Check that tree remains valid
post_processing = g.node_list[-1]
for i in range(len(post_processing)):
    assert all(post_processing[i].pg[:i+1])
    assert post_processing[i].m in ['xor_node']
