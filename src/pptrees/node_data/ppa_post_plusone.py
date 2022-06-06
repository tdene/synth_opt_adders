name = "ppa_post_plusone"
data = dict()

### Post-processing node
data[
    "verilog"
] = """
module ppa_post_plusone(xin, yin, pin, gin, sum, sum_plus_one);

	input xin, yin, pin, gin;
	output sum, sum_plus_one;

        wire w1;

        or2  U1(w1, pin, gin);
	mux2 U2(sum,gin,xin,yin);
	mux2 U3(sum_plus_one,w1 ,xin,yin);

endmodule
"""

data[
    "vhdl"
] = """
"""

data["shape"] = "circle"
data["label"] = "x"
data["fontname"] = "Comic Sans"
data["style"] = "bold"
data["fixedsize"] = "shape"
data["penwidth"] = "4.0"
data["fontsize"] = "52"

data["ins"] = [("gin", 1, 0, 1), ("xin", 1, 1, 0), ("yin", 1, 1, 0)]
data["outs"] = [("sum", 1), ("sum_plus_one", 1)]

# data["logic"] = lambda yin, xin, gin, pin: [yin if gin else xin]

data["pd"] = 9 / 3
data["le"] = [9 / 3, 9 / 3]
