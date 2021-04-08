#!/bin/python3

import sys
sys.path.append("..")

from prefix import adder_node

n = adder_node(0,1,'grey')

assert(n.x==0)
assert(n.y==1)
from modules import modules; assert(n.m in modules);
assert('pin' in n.ins)
assert('gout' in n.outs)
assert(len(n.ins['gin'])==2)
