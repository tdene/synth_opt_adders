name = "ppa_lspine_pre"
data = dict()

### ppa_lspine_pre
data[
    "verilog"
] = """
module ppa_lspine_pre(a_in, b_in, yout, xout);

	input a_in, b_in;
	output yout, xout;

	xor2  U1(xout,a_in,b_in);
	xnor2 U2(yout,a_in,b_in);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_lspine_pre is
	port (
		a_in : in std_logic;
		b_in : in std_logic;
		xout : out std_logic
		yout : out std_logic
	);
end entity;

architecture behavior of ppa_lspine_pre is
begin

U1: xor2
	port map (
		A => a_in,
		B => b_in,
		Y => xout
	);

U2: xnor2
	port map (
		A => a_in,
		B => b_in,
		Y => yout
	);

end architecture;
"""

data["shape"] = "square"
data["fillcolor"] = "white"
data["label"] = "pre"
data["style"] = "dashed"

data["ins"] = [("a_in", 1, 1, 0), ("b_in", 1, 0, 1)]
data["outs"] = [("xout", 1), ("yout", 1)]

data["logic"] = lambda pin, gin: [pin ^ gin, ~(pin ^ gin)]

data["pd"] = 9 / 3
data["le"] = [9 / 3, 9 / 3]
