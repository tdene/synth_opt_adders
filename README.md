# Prefix tree adder generation scripts

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/adder_transforms.gif?raw=true" width="400"/>

In general, prefix tree adders are usually generated from scratch. That is, either previously-named families of adders are used, or hybrid adders are created by combining / concatenating previously-named families of adders.

In addition, current taxonomies of adders cannot properly describe the entire space of all valid prefix tree adder structures.

Despite the overall elegance and great usefulness of Harris's taxonomy, for example, the two adders below would be classified as the same structure in spite of significant differences. [2]

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/knowles1.png?raw=true" width="250"/>

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/knowles2.png?raw=true" width="250"/>

What if there was a way to navigate the entire space of valid adder trees, incrementally and bit-targeted, using a minimal and circular, transform group?

This repository seeks to implement this using transforms between the following three states \[L, T, F\]:

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/L.png?raw=true" width="150"/>

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/T.png?raw=true" width="150"/>

<img src="https://github.com/tdene/synth_opt_adders/blob/main/demo/F.png?raw=true" width="150"/>

The L\<-\>F transform was previously discussed by Fishburn [1]. The L\<-\>T transform and F\<-\>T transforms have not been found in published works by the author.

[1]  J. P. Fishburn. A depth-decreasing heuristic for combinational logic; or how to convert a ripple-carry adder into a carrylookahead adder or anything in-between. In Proc. 27th Design Automation Conf., pages 361–364, 1990

[2] D. Harris, "A taxonomy of parallel prefix networks," The Thirty-Seventh Asilomar Conference on Signals, Systems & Computers, 2003, 2003, pp. 2213-2217 Vol.2
