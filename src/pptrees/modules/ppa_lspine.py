name = "ppa_lspine"
data = dict()

### ppa_lspine
data[
    "verilog"
] = """
module ppa_lspine(xin, yin, pin, gin, xout, yout);

	input xin, yin, pin, gin;
	output xout, yout;

	wire w1;

	or2  U1(w1, pin, gin);
	mux2 U2(xout,gin,yin,xin);
	mux2 U3(yout,w1 ,yin,xin);

endmodule
"""

data[
    "vhdl"
] = """
"""

data["shape"] = "circle"
data["color"] = "white"
data["fillcolor"] = "white"
data["label"] = "⊗"
data["style"] = "solid"
data["fixedsize"] = "shape"
data["fontsize"] = "60"

# Footprint
data["footprint"] = "ppa_lspine"
data["priority"] = 1

data["ins"] = [("xin", 1, 1, 0), ("yin", 1, 1, 0),
                     ("pin", 1, 0, 1), ("gin", 1, 0, 1)]
data["outs"] = [("xout", 1), ("yout", 1)]

#ppa_lspine["logic"] = lambda pin, gin: [pin ^ gin, ~(pin ^ gin)]

data["pd"] = 9 / 3
data["le"] = [9 / 3, 9 / 3]
