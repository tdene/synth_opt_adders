# Prefix tree adder generation scripts

## Table of Contents

[Introduction](#introduction)

[How to install](#installation-instructions)

[How to use](#user-guide)

[References](#references)

## Introduction

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/adder_transforms.gif?raw=true" width="400"/>

In general, prefix tree adders are usually generated from scratch. That is, either previously-named families of adders are used, or hybrid adders are created by combining / concatenating previously-named families of adders.

In addition, current taxonomies of adders cannot properly describe the entire space of all valid prefix tree adder structures.

Despite the overall elegance and great usefulness of Harris's taxonomy, for example, the two adders below would be classified as the same structure in spite of significant differences. [2]

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/knowles1.png?raw=true" width="250"/>

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/knowles2.png?raw=true" width="250"/>

What if there was a way to navigate the entire space of valid adder trees, incrementally and bit-targeted, using a minimal and circular, transform group?

This repository seeks to implement this using transforms between the following three states \[L, T, F\]: [4]

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/L.png?raw=true" width="150"/>

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/T.png?raw=true" width="150"/>

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/F.png?raw=true" width="150"/>

The L\<-\>F transform was previously discussed by Fishburn [1]. The L\<-\>T transform and F\<-\>T transforms have not been found in published works by the author.

## Installation Instructions

In order to use this repository, the following programs are required:

 * Python3.6+ (`apt install python3`)
 * pip3 (`apt install python3-pip`)
 * GraphViz (`apt install graphviz`)

Then simply install this repository as a local Python package:
```
pip3 install git+https://github.com/tdene/synth_opt_adders.git --user
```

## User Guide

The bulk of this tool's source code is currently contained in two modules:
[prefix_graph.py](src/prefix_graph.py) and [prefix_tree.py](src/prefix_tree.py).

Some examples of how to use the methods within these two modules can be found
in [unit_tests/tree_test.py](unit_tests/tree_test.py).

The guide below will show how to generate a Sklansky / Brent-Kung hybrid,
modify it slightly towards Kogge-Stone, flatten its worst path, and finally
print out a diagram and HDL representation. This guide seeks to showcase
some of the flexibility that this library offers.

Begin by opening a new Python shell or creating a new file. It is simplest to
perform this demo within a shell:
```
python3
```

First, import the classes and methods that will be used for this demo:
```
from pptrees.prefix_graph import prefix_node as node
from pptrees.adder_tree import adder_tree as tree
from pptrees.util import lg
```

Next, initialize a prefix tree of width 32. For brevity, we will initialize
directly to the Sklansky structure:
```
g = tree(32,"sklansky")
```

If so desired, you may at this point print out a diagram of the tree to follow
alongside its progress. To view the diagram, simply open the specified .png
file in a new window.
```
g.png('1.png')
```
<img src="https://raw.githubusercontent.com/tdene/synth_opt_adders/main/demo/1.png?raw=true" width="1200"/>

Next, we will turn this Sklansky adder into a Sklansky / Brent-Kung hybrid.
This is done by taking "Harris steps" on the adder's less-significant half. As
an example, take one Harris step in the FL direction and view the output:
```
g.harris_step('FL',1,top_bit=32//2)
g.png('2.png')
```
<img src="https://raw.githubusercontent.com/tdene/synth_opt_adders/main/demo/2.png?raw=true" width="1200"/>

You will notice that the bottom half of the prefix structure is now a
Ladner-Fischer structure with maximum fan-out of 4. By taking several more
Harris steps, a Brent-Kung structure can be reached. Note that a "Harris step"
is defined in the source code as well in the author's publications, and is
simply a loop of its respective transforms.
```
g.harris_step('FL',3,top_bit=32//2)
g.harris_step('FL',1,top_bit=32//4)
g.harris_step('FL',1,top_bit=32//8)
g.png('3.png')
```
<img src="https://raw.githubusercontent.com/tdene/synth_opt_adders/main/demo/3.png?raw=true" width="1200"/>

Looking at "3.png", a hybrid Sklansky / Brent-Kung hybrid is easily
recognizable. Let us now perform some point-targeted transforms. For example,
we may choose to decouple some of the fanout:
```
g.FL(31,5)
g.FL(30,5)
g.FL(29,5)
g.FL(28,5)

g.FL(19,5)
g.FL(18,5)
g.FL(17,5)
g.FL(16,5)
g.png('4.png')
```
<img src="https://raw.githubusercontent.com/tdene/synth_opt_adders/main/demo/4.png?raw=true" width="1200"/>

We may also choose to turn some of the fan-out for wire-tracks. Note that in
the current version of this code-base, this operation runs in O(n^2) time.
Future optimizations will reduce this run-time.
```
g.FT(16,6)
g.FT(17,6)
g.png('5.png')
g.FT(13,6)
g.png('6.png')
```
<img src="https://raw.githubusercontent.com/tdene/synth_opt_adders/main/demo/6.png?raw=true" width="1200"/>

At any point in time, we may query the data structure in a multitude of ways.
The next example queries what node is present at the coordinates (13,6), its
diagonal predecessor, and its vertical black node predecessor:
```
print(g[13,6])
print(g.pre(g[13,6]))
print(g.r_top(g[13,6]))
```

In its current form, the netlist would be written using hierarchical modules.
The HDL can also be output flat, or partially flat. This next example will
choose the estimated three worst paths of the design and flatten only those:
```
g.recalc_weights()
worst_path_1 = g.longest_path()
g.add_block(*worst_path_1)
worst_path_2 = g.longest_path()
g.add_block(*worst_path_2)
worst_path_3 = g.longest_path()
g.add_block(*worst_path_3)
g.png('7.png')
g.hdl('sample.v')
```
<img src="https://raw.githubusercontent.com/tdene/synth_opt_adders/main/demo/7.png?raw=true" width="1200"/>

The final output image, "7.png", contains a visualization of the flattening
performed by the last step. The file "sample.v" contains HDL for the design
written in the Verilog standard.

Numerous possibilities exist for the use of this library. Future efforts will
include the creation of a fully automatic constraint-driven adder synthesis
tool, as well as the implementation of sparsity and multi-level Ling
optimization.

## References

[1] J. P. Fishburn. A depth-decreasing heuristic for combinational logic; or how to convert a ripple-carry adder into a carrylookahead adder or anything in-between. In Proc. 27th Design Automation Conf., pages 361–364, 1990

[2] D. Harris, "A taxonomy of parallel prefix networks," The Thirty-Seventh Asilomar Conference on Signals, Systems & Computers, 2003, 2003, pp. 2213-2217 Vol.2

[3] R. Zimmermann, "Non-Heuristic Optimization and Synthesis of Parallel-Prefix Adders", in Proc. Int. Workshop on Logic and Architecture Synthesis (IWLAS'96), Grenoble, France, Dec. 1996, pp. 123-132.

[4] T. Ene and J. E. Stine, "A Comprehensive Exploration of the Parallel Prefix Adder Tree Space," 2021 IEEE 39th International Conference on Computer Design (ICCD), 2021, pp. 125-129, doi: 10.1109/ICCD53106.2021.00030.
