from pptrees.prefix_graph import prefix_node as node
from pptrees.adder_tree import adder_tree as tree
from pptrees.util import lg

g = tree(32,"sklansky")

g.png('1.png')

g.harris_step('FL',1,top_bit=32//2)
g.png('2.png')

g.harris_step('FL',3,top_bit=32//2)
g.harris_step('FL',1,top_bit=32//4)
g.harris_step('FL',1,top_bit=32//8)
g.png('3.png')

g.FL(31,5)
g.FL(30,5)
g.FL(29,5)
g.FL(28,5)

g.FL(19,5)
g.FL(18,5)
g.FL(17,5)
g.FL(16,5)
g.png('4.png')

g.FT(16,6)
g.FT(17,6)
g.png('5.png')
g.FT(13,6)
g.png('6.png')

print(g[13,6])
print(g.pre(g[13,6]))
print(g.r_top(g[13,6]))

g.recalc_weights()
worst_path_1 = g.longest_path()
g.add_block(*worst_path_1)
worst_path_2 = g.longest_path()
g.add_block(*worst_path_2)
worst_path_3 = g.longest_path()
g.add_block(*worst_path_3)
g.png('7.png')
g.hdl('sample.v')
