name = "ppa_rspine_pre"
data = dict()

### Pre-processing node for input sparsity
data[
    "verilog"
] = """
module ppa_rspine_pre(a_in, b_in, gout);

	input a_in, b_in;
	output gout;

	and2 U2(gout,a_in,b_in);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_rspine_pre is
	port (
		a_in : in std_logic;
		b_in : in std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_rspine_pre is
begin

U2: and2
	port map (
		A => a_in,
		B => b_in,
		Y => gout
	);

end architecture;
"""

data["shape"] = "square"
data["fillcolor"] = "white"
data["label"] = "pre"
data["style"] = "dashed"

data["ins"] = [("a_in", 1, 1, 0), ("b_in", 1, 1, 0)]
data["outs"] = [("gout", 1)]

data["logic"] = lambda a, b: [0, a & b]

data["pd"] = 2
data["le"] = [4.0 / 3, 4.0 / 3]
