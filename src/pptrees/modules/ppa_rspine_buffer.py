name = "ppa_rspine_buffer"
data = dict()

### Buffer node
data[
    "verilog"
] = """
module ppa_rspine_buffer(gin, gout);

	input gin;
	output gout;

	buffer U2(gout,gin);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_rspine_buffer is
	port (
		gin : in std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_rspine_buffer is
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

data["ins"] = [("gin", 1, 1, 0)]
data["outs"] = [("gout", 1)]

data["logic"] = lambda gin: [gin]

data["pd"] = 2
data["le"] = [1, 1]
