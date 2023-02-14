name = "ppa_lspine_pre_simple"
data = dict()

### ppa_lspine_pre_simple
data[
    "verilog"
] = """
module ppa_lspine_pre_simple(a_in, b_in, xout);

	input a_in, b_in;
	output xout;

	xor2 U1(xout,a_in,b_in);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_lspine_pre_simple is
	port (
		a_in : in std_logic;
		b_in : in std_logic;
		xout : out std_logic
	);
end entity;

architecture behavior of ppa_lspine_pre_simple is
begin

U1: xor2
	port map (
		A => a_in,
		B => b_in,
		Y => xout
	);

end architecture;
"""

data["shape"] = "square"
data["fillcolor"] = "white"
data["label"] = "pre"
data["style"] = "dashed"

data["ins"] = [("a_in", 1, 1, 0), ("b_in", 1, 0, 1)]
data["outs"] = [("xout", 1)]

data["logic"] = lambda pin, gin: [pin ^ gin]

data["pd"] = 9 / 3
data["le"] = [9 / 3, 9 / 3]
