# Prefix tree adder generation scripts

![gif going through some transforms](https://github.com/tdene/synth_opt_adders/blob/main/demo/adder_transforms.gif?raw=true)

In general, prefix tree adders are currently generated from scratch. Either previously-named families of adders are used, or hybrid adders are created by combining / concatenating previously-named families of adders.

In addition, current taxonomies of adders, such as that of David Harris, cannot properly describe the entire space of all valid prefix tree adder structures. Below are images of two valid adders that would be classified as the same structure under the Harris taxonomy, despite significant differences. [2]

![knowles1](https://github.com/tdene/synth_opt_adders/blob/main/demo/knowles1.png?raw=true)
![knowles2](https://github.com/tdene/synth_opt_adders/blob/main/demo/knowles2.png?raw=true)

What if there was a way to navigate the entire space of valid adder trees, incrementally, bit-targeted, using a minimal transform group?

This repository seeks to implement this using transforms between the following three states \[L, T, F\]:

![L state](https://github.com/tdene/synth_opt_adders/blob/main/demo/L.png?raw=true)
![T state](https://github.com/tdene/synth_opt_adders/blob/main/demo/T.png?raw=true)
![F state](https://github.com/tdene/synth_opt_adders/blob/main/demo/F.png?raw=true)

The L\<-\>F transform was previously discussed by Fishburn [1]. The L\<-\>T transform and F\<-\>T transforms have not been found in published works by the author.

[1]  J. P. Fishburn. A depth-decreasing heuristic for combinational logic; or how to convert a ripple-carry adder into a carrylookahead adder or anything in-between. In Proc. 27th Design Automation Conf., pages 361–364, 1990
[2] D. Harris, "A taxonomy of parallel prefix networks," The Thirty-Seventh Asilomar Conference on Signals, Systems & Computers, 2003, 2003, pp. 2213-2217 Vol.2
