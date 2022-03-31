from .modules import modules
from .prefix_tree import prefix_tree
from .prefix_graph import prefix_node as node

class adder_tree(prefix_tree):
    """Class that generates parallel prefix adder trees"""

    def __init__(self,width,network="ripple",
            node_defs={
                'pre':'ppa_pre',
                'post':'ppa_post',
                'black':'ppa_black',
                'grey':'ppa_grey',
                'buffer':'ppa_buffer',
                'first_pre':'ppa_first_pre'
                },
            is_idem=True):
        """Initializes a parallel prefix tree adder

        Refer to the prefix_tree's docstring for a full description.
        """
        super().__init__(width,network,node_defs,is_idem)

    def hdl(self,out=None,mapping="behavioral",language="verilog",top_module="adder",full_flat=False):
        super().hdl(out,mapping,language,top_module,full_flat)

    def _hdl_preamble(self,language="verilog",top_module="adder"):
        """Defines the preamble of the graph's HDL

        This method implements prefix_graph's counterpart for adders.
        """
        if language=="verilog": return self._verilog_preamble(top_module)
        if language=="vhdl": return self._vhdl_preamble(top_module)

    def _verilog_preamble(self,top_module):
        """Verilog preamble for the adder's HDL"""

        preamble = []
        used_modules = set()

        # Main module header
        preamble.append("""
module {1}(cout, sum, a, b, cin);

	input [{0}:0] a, b;
	input cin;
	output [{0}:0] sum;
	output cout;
""".format(self.w-1,top_module))

        # Wire definitions

        # set of all wires
        wire_set = set([e[2]['edge_name'] for e in self.edges(data=True)])
        
        # Special-named wires
        wires1 = ["\twire"]

        # Generic-named wires
        wires2 = ["\twire"]

        # Sort wires by their origin
        for x in wire_set:
            if isinstance(x,int):
                wires2.append(" {0},".format(node._parse_net(x)))
            else:
                wires1.append(" {0},".format(node._parse_net(x)))
        wires1 = ''.join(wires1)[:-1] + ";"
        wires2 = ''.join(wires2)[:-1] + ";"

        # Add both kinds of wires to preamble
        preamble.append(wires1)
        preamble.append(wires2)
        preamble.append('')

        ### Add normal pre-processing nodes

        preamble.append("// start of pre-processing logic\n")
        # Iterate over all pre-processing nodes
        for n in self.node_list[0]:
            preamble.append(n.hdl(language="verilog"))
            used_modules.add(n.m)

        preamble.append('')

        ### Add normal post-processing nodes

        preamble.append("// start of post-processing logic\n")
        # Iterate over all post-processing nodes
        for n in self.node_list[-1]:
            n.ins['pin'][0]="$p{0}".format(n.x)
            preamble.append(n.hdl(language="verilog"))
            used_modules.add(n.m)

        preamble.append('')

        preamble.append("// start of custom pre/post logic\n")
        ### Add custom pre/post processing

        # Additional pre node to handle cout
        cout_pre = "\t{1} {1}_cout ( .a_in( a[{0}] ), .b_in( b[{0}] ), .pout ( p{0} ), .gout ( g{0} ) );"
        cout_pre = cout_pre.format(self.w-1,self.node_defs['pre'])

        preamble.append(cout_pre)
        used_modules.add(self.node_defs['pre'])

        # Additional grey node to handle cout
        cout_g = node._parse_net(self.node_list[-1][-1].ins['gin'][0])
        cout_grey = "\t{2} {2}_cout ( .gin ( {{g{0},{1}}} ), .pin ( p{0} ), .gout ( cout ) );"
        cout_grey = cout_grey.format(self.w-1,cout_g,self.node_defs['grey'])

        preamble.append(cout_grey)
        used_modules.add(self.node_defs['grey'])

        return (preamble,used_modules)

    def _vhdl_preamble(self,top_module):
        """VHDL preamble for the adder's HDL"""

        preamble = []
        used_modules = set()

        # Library imports
        preamble.append("""
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std;""")
        # Entity definition
        preamble.append("""
entity {1} is
	port (
		a,b : in std_logic_vector({0} downto 0);
		cin : in std_logic;
		cout : out std_logic;
		sum : out std_logic_vector({0} downto 0)
	);
end entity;
""".format(self.w-1,top_module))

        # Architecture definition
        preamble.append("architecture pptree of adder is")

        # Wire definitions

        # set of all wires
        wire_set = set([e[2]['edge_name'] for e in self.edges(data=True)])

        # Special-named wires
        wires1 = ["\tsignal"]

        # Generic-named wires
        wires2 = ["\tsignal"]

        # Sort wires by their origin
        for x in wire_set:
            if isinstance(x,int):
                wires2.append(" {0},".format(node._parse_net(x)))
            else:
                wires1.append(" {0},".format(node._parse_net(x)))
        wires1 = ''.join(wires1)[:-1] + " : std_logic;"
        wires2 = ''.join(wires2)[:-1] + " : std_logic;"

        # Add both kinds of wires to architecture definition
        preamble.append(wires1)
        preamble.append(wires2)
        preamble.append("\nbegin\n")

        ### Add normal pre-processing nodes

        preamble.append("-- start of pre-processing logic\n")
        # Iterate over all pre-processing nodes
        for n in self.node_list[0]:
            preamble.append(n.hdl(language="vhdl"))
            used_modules.add(n.m)

        preamble.append('')

        ### Add normal post-processing nodes

        preamble.append("-- start of post-processing logic\n")
        # Iterate over all post-processing nodes
        for n in self.node_list[-1]:
            n.ins['pin'][0]="$p{0}".format(n.x)
            preamble.append(n.hdl(language="vhdl"))
            used_modules.add(n.m)

        preamble.append('')
        
        ### Add custom pre/post processing
        
        preamble.append("-- start of custom pre/post logic\n")
        # Additional pre node to handle cout
        cout_pre = """
	{1}_cout: {1}
		port map (
			a_in => a({0}),
			b_in => b({0}),
			pout => p{0},
			gout => g{0}
		);""".format(self.w-1,self.node_defs['pre'])[1:]

        preamble.append(cout_pre)
        used_modules.add(self.node_defs['pre'])

        # Additional grey node to handle cout
        cout_g = node._parse_net(self.node_list[-1][-1].ins['gin'][0])
        cout_grey = """
	{2}_cout: {2}
		port map (
			gin(0) => {1},
			gin(1) => g{0},
			pin => p{0},
			gout => cout
		);""".format(self.w-1,cout_g,self.node_defs['grey'])[1:]

        preamble.append(cout_grey)
        used_modules.add(self.node_defs['grey'])

        return (preamble,used_modules)

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
