name = "ppa_post"
data = dict()

### Post-processing node
data[
    "verilog"
] = """
module ppa_post(xin, yin, gin, sum);

	input xin, yin, gin;
	output sum;

	mux2 U1(sum,gin,yin,xin);

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_post is
	port (
		yin : in std_logic;
		xin : in std_logic;
		gin : in std_logic;
		sum : out std_logic
	);
end entity;

architecture behavior of ppa_post is
begin

U1: mux2
	port map (
		A => yin,
		B => xin,
		S => gin,
		Y => sum
	);

end architecture;
"""

data["shape"] = "circle"
data["color"] = "white"
data["fillcolor"] = "white"
data["label"] = "⊗"
data["style"] = "solid"
data["fixedsize"] = "shape"
data["fontsize"] = "60"

data["ins"] = [("gin", 1, 0, 1), ("xin", 1, 1, 0), ("yin", 1, 1, 0)]
data["outs"] = [("sum", 1)]

data["logic"] = lambda yin, xin, gin: [yin if gin else xin]

data["pd"] = 9 / 3
data["le"] = [9 / 3, 9 / 3]
