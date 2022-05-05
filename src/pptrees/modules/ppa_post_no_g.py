name = "ppa_post_no_g"
data = dict()

### Post-processing node
data[
    "verilog"
] = """
module ppa_post_no_g(pin, sum);

	input pin;
	output sum;

	assign sum = pin;

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_post_no_g is
	port (
		pin : in std_logic;
		sum : out std_logic
	);
end entity;

architecture behavior of ppa_post_no_g is
begin

	sum <= pin;

end architecture;
"""

data["shape"] = "circle"
data["color"] = "white"
data["fillcolor"] = "white"
data["label"] = "⊗"
data["style"] = "solid"
data["fixedsize"] = "shape"
data["fontsize"] = "60"

# Footprint
data["footprint"] = "ppa_post"
data["priority"] = 3

data["ins"] = [("pin", 1, 1, 0)]
data["outs"] = [("sum", 1)]

data["logic"] = lambda pin: [pin]

data["pd"] = 0
data["le"] = [0, 0]