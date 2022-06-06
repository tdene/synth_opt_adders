name = "ppa_defactor_left"
data = dict()

### Black cell
data[
    "verilog"
] = """
module ppa_defactor_left(gin, pin, gout, pout);

	input [1:0] gin, pin;
	output gout, pout;

	and2 U1(pout,pin[1],pin[0]);
	oa21 U2(gout,gin[1],pin[1],gin[0]);

endmodule
"""

# Graphical representation
data["shape"] = "square"
data["fillcolor"] = "black"

# List of inputs represented by (name, total_bits, *bits_per_direction) tuple
data["ins"] = [("gin", 2, 1, 1), ("pin", 2, 1, 1)]

# List of outputs represented by (name, bits) tuple
data["outs"] = [("gout", 1), ("pout", 1)]

# Returns function that executes the logic of the module
data["logic"] = lambda gin, pin: [gin[1] | (pin[1] & gin[0]), pin[1] & pin[0]]

# Logical effort
data["pd"] = 7.5 / 3
data["le"] = [5.0 / 3, 6.0 / 3]
