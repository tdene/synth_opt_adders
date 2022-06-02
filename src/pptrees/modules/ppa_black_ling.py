name = "ppa_black_ling"
data = dict()

### Black cell
data[
    "verilog"
] = """
module ppa_black_ling(gin, pin, gout, pout);

	input [1:0] gin;
	input pin;
	output gout, pout;

	assign pout = pin;
	or2 U2(gout,gin[0],gin[1]);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_black_ling is
	port (
		gin : in std_logic_vector(1 downto 0);
		gout : out std_logic;
		pin : in std_logic;
		pout : out std_logic
	);
end entity;

architecture behavior of ppa_black_ling is
begin

	pout <= pin;

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
data["ins"] = [("gin", 2, 1, 1), ("pin", 1, 1, 0)]

# List of outputs represented by (name, bits) tuple
data["outs"] = [("gout", 1), ("pout", 1)]

# Returns function that executes the logic of the module
data["logic"] = lambda gin, pin: [gin[1] | (pin[1] & gin[0]), pin[1] & pin[0]]

# Logical effort
data["pd"] = 6.0 / 3
data["le"] = [4.0 / 3, 4.0 / 3]
