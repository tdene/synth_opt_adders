name = "ppa_pre_t"
data = dict()

### Pre-processing node
data[
    "verilog"
] = """
module ppa_pre_t(a_in, b_in, pout, gout);

	input a_in, b_in;
	output pout, gout;

	or2 U1(pout,a_in,b_in);
	and2 U2(gout,a_in,b_in);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_pre_t is
	port (
		a_in : in std_logic;
		b_in : in std_logic;
		pout : out std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_pre_t is
begin

U1: or2
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

data["logic"] = lambda a, b: [a | b, a & b]

data["pd"] = 2
data["le"] = [5.0 / 3, 5.0 / 3]
