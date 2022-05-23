name = "ppa_buffer_grey"
data = dict()

### Buffer node
data[
    "verilog"
] = """
module ppa_buffer_grey(gin, gout);

	input gin;
	output gout;

	buffer U2(gout,gin);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_buffer_grey is
	port (
		gin : in std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_buffer_grey is
begin

U2: buffer
	port map (
		A => gin,
		Y => gout
	);

end architecture;
"""

data["shape"] = "invtriangle"
data["fillcolor"] = "white"

# Footprint
data["footprint"] = "ppa_buffer"
data["priority"] = 1

data["ins"] = [("gin", 1, 1, 0)]
data["outs"] = [("gout", 1)]

data["logic"] = lambda gin: [gin]

data["pd"] = 2
data["le"] = [1, 1]
