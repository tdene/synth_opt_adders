name = "invis"
data = dict()

### Buffer node
data[
    "verilog"
] = """
module invis(A, Y);

	input A;
	output Y;

	assign Y = A;

endmodule
"""

data[
    "vhdl"
] = """
entity invis is
	port (
		A : in std_logic;
		Y : out std_logic
	);
end entity;

architecture behavior of invis is
begin

	Y <= A;

end architecture;
"""

data["shape"] = "point"
data["fixedsize"] = "shape"
data["width"] = 0
data["height"] = 0
data["fillcolor"] = "black"

data["ins"] = [("A", 1, 1, 0)]
data["outs"] = [("Y", 1)]

data["logic"] = lambda A: [A]

data["pd"] = 0
data["le"] = [0, 0]
