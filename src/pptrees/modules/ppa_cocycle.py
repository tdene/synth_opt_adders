name = "ppa_cocycle"
data = dict()

### Black cell
data[
    "verilog"
] = """
module ppa_cocycle(gin, pin, gout, pout);

	input [1:0] gin, pin;
	output gout, pout;

	and2 U1(pout,pin[1],pin[0]);
	ao21 U2(gout,gin[0],pin[1],gin[1]);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_cocycle is
	port (
		gin : in std_logic_vector(1 downto 0);
		gout : out std_logic;
		pin : in std_logic_vector(1 downto 0);
		pout : out std_logic
	);
end entity;

architecture behavior of ppa_cocycle is
begin

U1: and2
	port map (
		A => pin(0),
		B => pin(1),
		Y => pout
	);

U2: ao21
	port map (
		A0 => gin(0),
		A1 => pin(1),
		B0 => gin(1),
		Y => gout
	);

end architecture;
"""

# Graphical representation
data["shape"] = "square"
data["fillcolor"] = "black"

# List of inputs represented by (name, total_bits, *bits_per_direction) tuple
data["ins"] = [("gin", 2, 1, 1), ("pin", 2, 1, 1)]

# List of outputs represented by (name, bits) tuple
data["outs"] = [("gout", 1), ("pout", 1)]

# Returns function that executes the logic of the module
data["logic"] = lambda gin, pin: [gin[1] | (pin[1] & gin[0]), pin[1] & pin[0]]

# Logical effort
data["pd"] = 7.5 / 3
data["le"] = [5.0 / 3, 6.0 / 3]
