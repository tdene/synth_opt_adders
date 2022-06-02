name = "ppa_post"
data = dict()

### Post-processing node
data[
    "verilog"
] = """
module ppa_post(xin, yin, gin, sum);

	input xin, yin, gin;
	output sum;

	mux2 U1(sum,gin,xin,yin);

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
		A => xin,
		B => yin,
		S => gin,
		Y => sum
	);

end architecture;
"""

data["shape"] = "circle"
data["label"] = "x"
data["fontname"] = "Comic Sans"
data["style"] = "bold"
data["fixedsize"] = "shape"
data["penwidth"] = "4.0"
data["fontsize"] = "52"

data["ins"] = [("gin", 1, 0, 1), ("xin", 1, 1, 0), ("yin", 1, 1, 0)]
data["outs"] = [("sum", 1)]

data["logic"] = lambda yin, xin, gin: [yin if gin else xin]

data["pd"] = 9 / 3
data["le"] = [9 / 3, 9 / 3]
