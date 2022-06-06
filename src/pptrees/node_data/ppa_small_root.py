name = "ppa_small_root"
data = dict()

### Post-processing node
data[
    "verilog"
] = """
module ppa_small_root(pin, sum);

	input pin;
	output sum;

	assign sum = pin;

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_small_root is
	port (
		pin : in std_logic;
		sum : out std_logic
	);
end entity;

architecture behavior of ppa_small_root is
begin

	sum <= pin;

end architecture;
"""

data["shape"] = "circle"
data["label"] = "x"
data["fontname"] = "Comic Sans"
data["style"] = "bold"
data["fixedsize"] = "shape"
data["penwidth"] = "4.0"
data["fontsize"] = "52"

data["ins"] = [("pin", 1, 1, 0)]
data["outs"] = [("sum", 1)]

data["logic"] = lambda pin: [pin]

data["pd"] = 0
data["le"] = [0, 0]
