name = "ppa_buffer"
data = dict()

### Buffer node
data[
    "verilog"
] = """
module ppa_buffer(pin, gin, pout, gout);

	input pin, gin;
	output pout, gout;

	buffer U1(pout,pin);
	buffer U2(gout,gin);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_buffer is
	port (
		pin : in std_logic;
		pout : out std_logic;
		gin : in std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_buffer is
begin

U1: buffer
	port map (
		A => pin,
		Y => pout
	);

U2: buffer
	port map (
		A => gin,
		Y => gout
	);

end architecture;
"""

data["shape"] = "invtriangle"
data["fillcolor"] = "white"

data["ins"] = [("gin", 1, 1, 0), ("pin", 1, 1, 0)]
data["outs"] = [("gout", 1), ("pout", 1)]

data["logic"] = lambda pin, gin: [pin, gin]

data["pd"] = 2
data["le"] = [1, 1]
