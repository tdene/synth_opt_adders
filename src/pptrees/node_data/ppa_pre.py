name = "ppa_pre"
data = dict()

### Pre-processing node
data[
    "verilog"
] = """
module ppa_pre(a_in, b_in, pout, gout);

	input a_in, b_in;
	output pout, gout;

	xor2 U1(pout,a_in,b_in);
	and2 U2(gout,a_in,b_in);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_pre is
	port (
		a_in : in std_logic;
		b_in : in std_logic;
		pout : out std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_pre is
begin

U1: xor2
	port map (
		A => a_in,
		B => b_in,
		Y => pout
	);

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
data["outs"] = [("pout", 1), ("gout", 1)]

data["logic"] = lambda a, b: [a ^ b, a & b]

data["pd"] = 9 / 3
data["le"] = [9 / 3, 9 / 3]
