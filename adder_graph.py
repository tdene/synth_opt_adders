import networkx as nx
from modules import modules

# Defines a node in the adder graph
class adder_node():

# Nodes have an x position (bit), y position (level),
# the module they are representing (black, grey, etc),
# and two dictionary of edges

    # Pre-conditions:
    # x, y are integers
    # module is a valid module from modules
    # flat is a flag that determine how HDL is output
    # custom_module is an optional alternative for providing
    # a module definition not included in modules

    # Post-conditions:
    # stores all these values into internal variables
    # creates two dictionaries of input/output edges

    def __init__(self, x, y, module, flat=False, custom_module=None):
        if not (isinstance(x,int) and isinstance(y,int)):
            raise TypeError("adder_node x,y must both be integers")

        if module not in modules and not isinstance(custom_module,dict):
            raise ValueError("trying to create node with invalid module")
        if isinstance(custom_module,dict):
            if 'verilog' not in custom_module:
                raise ValueError("custom modules must have valid HDL")
            if 'logic' not in custom_module:
                raise ValueError("custom modules must have valid logic")
            modules[module]=custom_module

        self.x=x; self.y=y; self.m=module; self.flat=flat;

        # Create inputs and outputs dictionaries; initialize to None
        self.ins={x:[None]*y for x,y in modules[self.m]['ins']}
        self.outs={x:[None]*y for x,y in modules[self.m]['outs']}

        # A list of all nodes that directly or indirectly feed into this one
        self.upstream=set()

        # All nodes start, by default, outside of any blocks
        self.block=None

    # Static helper function that checks whether a node is not invis
    def _exists(n):
        return n is not None and n.m not in ['invis_node']

    # Static helper function that checks whether a node is a buffer
    def _isbuf(n):
        return n is not None and n.m in ['buffer_node']

    # Static helper function that checks whether a node is
    # not none, pre-processing, or post-processing
    def _in_tree(n):
        return n is not None and n.m not in ['post_node','pre_node']

    # The node object has dictionaries of input/output edges
    # These come in 4 possible flavors:
    # - None (unassigned net) -> parsed to n0
    # - Integer (assigned net) -> parsed to n`Integer
    # - Hardcoded name ($net_name) -> parsed to net_name
    # - Hardcoded value (x'bx) -> kept as is
    # ::: UPDATE ::: removing 4th functionality
    # This is a static method that performs this conversion

    def _parse_net(x):
        if x is None:
            return "n0"
        if isinstance(x,int):
            return "n"+str(x)
        if "$" in x:
            return x.replace("$","")
#        if "'" in x:
#            return x
        raise TypeError("net stored in node {0} is invalid".format(repr(x)))

    # Return single line of verilog consisting of module instantiation

    def _verilog(self):
        ret="    {3} {0}_{1}_{2} (".format(self.m,self.x,self.y,self.m)
        tmp=self.ins.copy()
        tmp.update(self.outs)
        for a in tmp:
            ret+=" ."+a+"( {"
            ret+=','.join([adder_node._parse_net(x) for x in tmp[a]])
            ret+='} ),'
        ret=ret[:-1]+' );'
        return ret

    # Return block of verilog consisting of module logic

    def _flat(self):
        ret='\n'.join([x for x in modules[self.m]['verilog'].split('\n')
                      if (x!='' and 'input' not in x
                          and 'output' not in x
                          and 'module' not in x)])+'\n'
        tmp=self.ins.copy()
        tmp.update(self.outs)
        for a in tmp:
            if len(tmp[a])==1:
                net_name=adder_node._parse_net(tmp[a][0])
                ret=ret.replace(a,net_name)
            else:
                for b in range(len(tmp[a])):
                    net_name=adder_node._parse_net(tmp[a][b])
                    ret=ret.replace("{0}[{1}]".format(a,b),net_name)
        return ret

    # Determine which verilog representation str() will use

    def flatten(self,flag=True):
        self.flat=flag

    def hdl(self):
        return self._flat() if self.flat else self._verilog()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "adder_node({0},{1},{2})".format(self.x,self.y,self.m)


# Defines a di-graph of adder nodes and edges
# The basic internal structure of the graph is a 2-D array of nodes
class adder_graph(nx.MultiDiGraph):

    # Pre-condition: width is an integer
    # Post-conditions: creates a 2-D array of all nodes; runs nx.DiGraph's init

    def __init__(self, width):
        if not isinstance(width,int):
            raise TypeError("adder_graph width must be an integer")
        self.w=width
        # Initialize graph to "width" of width
        self.node_list=[[None]*self.w]

        # Procedurally-generated net names start with "n1"
        self.next_net = 1

        # Procedurally-generated block names start with "block1"
        self.next_block = 1
        self.blocks = [None,None]

        super().__init__(self)

    # Simplify self.node_list[y][x] to self[x,y]
    def __getitem__(self,n):
        # Auto-raise error if n is not iterable with the len call
        if len(n)!=2:
            raise ValueError("must input two numbers to access node in graph")
        return self.node_list[n[1]][n[0]]

    # Pre-condtions:
    # 0 <= x < width
    # 0 <= y <= len(self.node_list) [no skipping levels!!!]
    # module is a valid module from modules

    # Post-condition: adds node to graph and 2-D array of all nodes
    def add_node(self, n, style=None, label=None):
        if not isinstance(n,adder_node):
            raise TypeError("can only add adder_nodes to adder_graph")
        if not (n.x<self.w and n.x>=0):
            raise ValueError("cannot add a node with x beyond the width")
        if n.y<0:
            raise ValueError("cannot add a node with negative level")
        if n.y>len(self.node_list):
            raise ValueError("cannot skip levels when adding nodes")
        if n.m not in modules:
            raise ValueError("trying to add node with invalid module")
        if n in self:
            raise ValueError("trying to double-add a node to the graph")
        if n.y<len(self.node_list) and self[n.x,n.y]!=None:
            raise ValueError("trying to add node to populated grid square")
        if n.y==len(self.node_list):
            self.node_list.append([None]*self.w)
        self.node_list[n.y][n.x]=n
        
        n_kwargs = modules[n.m]
        n_kwargs['shape'] = n_kwargs.get('shape','square')
        n_kwargs['fillcolor'] = n_kwargs.get('fillcolor','white')
        n_kwargs['label'] = n_kwargs.get('label','') if label is None else label
        n_kwargs['style'] = n_kwargs.get('style','filled') if style is None else style
        n_kwargs['pos'] = "{0},{1}!".format(-1*n.x,-1*n.y)

        super().add_node(n,**n_kwargs)
        return n

    # Removes node from nodelist array as well as graph

    def remove_node(self, n):
        if n==None:
            return
        self.node_list[n.y][n.x]=None
        super().remove_node(n)
        return n

    # Pre-conditions:
    # n1, n2, are 2-element integer arrays, [x,y] describing valid nodes
    # n1, n2 are on adjacent levels [use buffers otherwise]
    # pin1, pin2 are valid, unassigned, ports of n1, n2, respectively
    # only one of (pin1, pin2) is an input, the other being an output
    # specifically, to keep code simple, pin1 is output and pin2 is input

    # Post-condition: adds edge between target nodes
    def add_edge(self, n1, pin1, n2, pin2):
        p1,b1=pin1; p2,b2=pin2;
        if not isinstance(n1,adder_node) or not isinstance(n2,adder_node):
            raise TypeError("can only add edge between nodes")
        if abs(n1.y-n2.y)!=1:
            raise ValueError("cannot add an edge between non-adjacent levels")
        if n2.y<=n1.y:
            raise ValueError("cannot add an edge in the wrong direction")
        if p1 not in n1.outs or p2 not in n2.ins:
            raise ValueError("cannot add an edge between invalid ports")

        # Assigns name to edge, based on order in which it was added
        #edge_name = len(self.edges)
        #edge_name = "${0}_{1}_{2}_{3}".format(p1,b1,n1.x,n1.y)
        edge_name = self.next_net
        self.next_net += 1
        if not n1.outs[p1][b1] is None: edge_name = n1.outs[p1][b1]
        elif not n2.ins[p2][b2] is None: edge_name = n2.ins[p2][b2]
        n1.outs[p1][b1]=edge_name
        n2.ins[p2][b2]=edge_name

        # Styles the edge
        edge_kwargs={'arrowhead':'none',
                     'headport':'ne','tailport':'sw',
                     'ins':pin1,'outs':pin2}
        if n2.x==n1.x:
            edge_kwargs['headport']='n'
            edge_kwargs['tailport']='s'
        if adder_node._isbuf(n1):
            edge_kwargs['tailport']='s'

        n2.upstream.add((n1.x,n1.y))
        n2.upstream.update(n1.upstream)

        super().add_edge(n1,n2,**edge_kwargs)

    # NetworkX has no way to remove all edges between 2 nodes in a MultiGraph?
    # Keep removing until an Exception is thrown?

    def remove_all_edges(self,n1,n2):
        try:
            self.remove_edge(n1,n2)
            return self.remove_all_edges(n1,n2)
        except nx.NetworkXError:
            return

    # Create a new block
    # Pre-condition:
    # nodes is a list of nodes, all of which have attribute block = None
    # Post-condition: adds new block, containing nodes
    def add_block(self,*nodes):
        if not all([n.block is None for n in nodes]):
            raise ValueError("cannot add node to multiple blocks")
        # Set block attribute for all nodes
        for n in nodes:
            n.block = self.next_block
            n.flatten()
        # Add block to blocks list
        new_block = set(nodes)
        if self.next_block==len(self.blocks)-1: self.blocks.append(None)
        self.blocks[self.next_block]=new_block

        self.next_block = next(x for x in range(1,len(self.blocks)) if self.blocks[x] is None)

    # Remove a block
    # Pre-condition: block is a valid block ID
    # Post-condition: removes block
    def remove_block(self,block):
        if block>=len(self.blocks) or self.blocks[block] is None:
            raise ValueError("trying to remove non-existent block")
        for n in self.blocks[block]:
            n.block = None
            n.flatten(False)
        self.blocks[block] = None

    # Remove all block from graph
    def remove_all_blocks(self):
        for b in range(len(self.blocks)):
            if self.blocks[b] is not None:
                self.remove_block(b)
        self.next_block = 1
        self.blocks = [None,None]

    # Print out HDL
    # Needs to be cleaned
    def hdl(self,out=None):
        module_list=[]
        #module_defs=""
        head=""; body=""; block_instances="";
        module_defs=modules['grey']['verilog']
        block_defs=""
        endmodule="\nendmodule\n"
        ### CLEAN BELOW PLEASE!!!!!!!!!!!!!!!!
        head="\nmodule adder(cout, sum, a, b, cin);\n"
        head+="\tinput [{0}:0] a, b;\n".format(self.w-1)
        head+="\tinput cin;\n"
        head+="\toutput [{0}:0] sum;\n".format(self.w-1)
        head+="\toutput cout;\n"
        head+="\tpre_node pre_node_{1}_0 ( .a( a[{0}] ), .b( b[{0}] ), .pout ( p{0} ), .gout ( g{0} ) );\n".format(self.w-1,self.w)
        cfinal=self.node_list[-1][-1].ins['gin'][0]
        head+="\tgrey grey_node_cout ( .gin ( {{g{0},n{1}}} ), .pin ( p{0} ), .gout ( cout ) );\n".format(self.w-1,cfinal)
        ### CLEAN ABOVE PLEASE!!!!!
        for a in self.node_list:
            for n in a:
                if n.block is not None:
                    continue
                if n.m in ['buffer_node','invis_node']:
                    n.flatten()
                if n.m in ['post_node']:
                    tmp = n.ins['pin'][0]
                    n.ins['pin'][0]="$p{0}".format(n.x)
                    body+=n.hdl()+'\n'
                    n.ins['pin'][0] = tmp
                else:
                    body+=n.hdl()+'\n'
                if n.m not in module_list:
                    module_list.append(n.m)
                    module_defs+=modules[n.m]['verilog']

        # Iterate over all blocks
        for b in range(len(self.blocks)):
            nodes = self.blocks[b]
            # Skip empty blocks
            if nodes is None: continue
            # For each block
            # Create list of inputs and outputs
            ins = set()
            outs = set()
            # Iterate over all nodes in a block
            for n in nodes:
                # Add ins/outs to block ins/outs
                for x in n.ins.values(): ins.update([adder_node._parse_net(y) for y in x])
                for x in n.outs.values(): outs.update([adder_node._parse_net(y) for y in x])
            # end iterate over all nodes in a block

            # Should a signal be generated as an output by
            # a node inside the block, it is clearly not a
            # block input, and should not be in the header.
            ins = ins - outs

            # Instantiate block
            inst_b = "    block_{0} block_{0}_instance (".format(b)
            tmp=ins|outs
            # Add ins/outs to block instantiation with dot notation
            for x in tmp: inst_b+=" .{0} ( {0} ),".format(x)
            inst_b=inst_b[:-1]+' );\n'
            # Add block instantiation to list of block_instances
            block_instances+=inst_b

            # Define block
            block_def="\nmodule block_{0}(".format(b)
            # List all ins/outs in module definition
            for x in tmp: block_def+=' '+x+','
            block_def = block_def[:-1]+');\n\n'
            # Declare all inputs and outputs
            block_def += "    input"
            for x in ins: block_def+=" {0},".format(x)
            block_def = block_def[:-1]+";\n"

            block_def += "    output"
            for x in outs: block_def+=" {0},".format(x)
            block_def = block_def[:-1]+";\n"
            # Put all nodes' hdl inside block definition
            block_def += '\n'
            for n in nodes:
                block_def+=n.hdl()+'\n'
            # Write endmodule line
            block_def+=endmodule
            # Add block definition to list of block_defs
            block_defs+=block_def

        # end iterate over all blocks
        ret=head+body+block_instances+endmodule+module_defs+block_defs
        if out is not None:
            with open(out,'w') as f:
                print(ret,file=f)
        return ret

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
