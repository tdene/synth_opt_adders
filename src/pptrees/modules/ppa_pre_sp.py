name = "ppa_pre_sp"
data = dict()

### Pre-processing node for input sparsity
data[
    "verilog"
] = """
module ppa_pre_sp(cin, pout, gout);

	input cin;
	output pout, gout;

	assign pout=1'b0;
	assign gout=cin;

endmodule
"""

data[
    "vhdl"
] = """
entity ppa_pre_sp is
	port (
		cin : in std_logic;
		pout : out std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_pre_sp is
begin

	pout <= '0';
	gout <= cin;

end architecture;
"""

data["shape"] = "square"
data["fillcolor"] = "white"
data["label"] = "pre"
data["style"] = "dashed"

# Footprint
data["footprint"] = "ppa_pre"
data["priority"] = 2

data["ins"] = [("c_in", 1, 1, 0)]
data["outs"] = [("pout", 1), ("gout", 1)]

data["logic"] = lambda a, b: [0, cin]

data["pd"] = 0
data["le"] = [0, 0]
