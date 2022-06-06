name = "ppa_grey_ling"
data = dict()

### Black cell
data[
    "verilog"
] = """
module ppa_grey_ling(gin, gout);

	input [1:0] gin;
	output gout;

	or2 U2(gout,gin[0],gin[1]);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_grey_ling is
	port (
		gin : in std_logic_vector(1 downto 0);
		gout : out std_logic;
	);
end entity;

architecture behavior of ppa_grey_ling is
begin

U2: or2
	port map (
		A => gin(0),
		B => gin(1),
		Y => gout
	);

end architecture;
"""

# Graphical representation
data["shape"] = "square"
data["fillcolor"] = "black"

# List of inputs represented by (name, total_bits, *bits_per_direction) tuple
data["ins"] = [("gin", 2, 1, 1)]

# List of outputs represented by (name, bits) tuple
data["outs"] = [("gout", 1)]

# Returns function that executes the logic of the module
data["logic"] = lambda gin, pin: [gin[1] | (pin[1] & gin[0]), pin[1] & pin[0]]

# Logical effort
data["pd"] = 6.0 / 3
data["le"] = [4.0 / 3, 4.0 / 3]
