name = "ppa_small_root"
data = dict()

### Post-processing node
data[
    "verilog"
] = """
module ppa_small_root(xin, sum);

	input xin;
	output sum;

	assign sum = xin;

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_small_root is
	port (
		xin : in std_logic;
		sum : out std_logic
	);
end entity;

architecture behavior of ppa_small_root is
begin

	sum <= xin;

end architecture;
"""

data["shape"] = "circle"
data["label"] = "x"
data["fontname"] = "Comic Sans"
data["style"] = "bold"
data["fixedsize"] = "shape"
data["penwidth"] = "4.0"
data["fontsize"] = "52"

data["ins"] = [("xin", 1, 1, 0)]
data["outs"] = [("sum", 1)]

data["logic"] = lambda xin: [xin]

data["pd"] = 0
data["le"] = [0, 0]
