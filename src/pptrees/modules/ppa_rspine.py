name = "ppa_rspine"
data = dict()

### Grey cell
data[
    "verilog"
] = """
module ppa_rspine(gin, pin, gout);

	input[1:0] gin;
	input pin;
	output gout;

	ao21 U1(gout,gin[0],pin,gin[1]);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_rspine is
	port (
		gin : in std_logic_vector(1 downto 0);
		gout : out std_logic;
		pin : in std_logic
	);
end entity;

architecture behavior of ppa_rspine is
begin

U1: ao21
	port map (
		A0 => gin(0),
		A1 => pin,
		B0 => gin(1),
		Y => gout
	);

end architecture;
"""

# Graphical representation
data["shape"] = "square"
data["fillcolor"] = "grey"

# List of inputs represented by (name, bits, diagonal_bits) tuple
data["ins"] = [("gin", 2, 1, 1), ("pin", 1, 1, 0)]

# List of outputs represented by (name, bits) tuple
data["outs"] = [("gout", 1)]

# Returns function that executes the logic of the module
data["logic"] = lambda gin, pin: [gin[1] | (pin & gin[0])]

# Logical effort
data["pd"] = 7.5 / 3
data["le"] = [5.0 / 3, 6.0 / 3]
