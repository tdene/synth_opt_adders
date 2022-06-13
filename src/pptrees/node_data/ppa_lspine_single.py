name = "ppa_lspine_single"
data = dict()

### ppa_lspine_single
data[
    "verilog"
] = """
module ppa_lspine_single(xin, yin, pin, gin, xout, yout);

	input xin, yin, pin, gin;
	output xout, yout;

	mux2 U2(xout,gin,xin,yin);
	mux2 U3(yout,pin,xin,yin);

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

data["ins"] = [
    ("xin", 1, 1, 0),
    ("yin", 1, 1, 0),
    ("pin", 1, 0, 1),
    ("gin", 1, 0, 1),
]
data["outs"] = [("xout", 1), ("yout", 1)]

# ppa_lspine_single["logic"] = lambda pin, gin: [pin ^ gin, ~(pin ^ gin)]

data["pd"] = 9 / 3
data["le"] = [9 / 3, 9 / 3]
