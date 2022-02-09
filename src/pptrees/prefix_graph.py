import networkx as nx
import importlib.resources
import pathlib
import shutil
from .modules import modules
from .util import sub_brackets

class prefix_node():
    """Defines a node in the prefix summation graph

    Nodes have an x position (bit), y position (level),
    the module they are representing (black, grey, etc),
    and two dictionary of edges
    """

    def __init__(self, x, y, module, flat=False, custom_module=None):
        """Initializes a node in the prefix summation graph

        Pre-conditions:
            x, y are integers
            module is a valid module from the modules list
            flat is an optional flag to determine how HDL is output
            custom_module is an optional alternative for providing
            a module definition that is not included in modules

        Post-conditions:
            stores all these values into internal variables
            creates two dictionaries of input/output edges
        """
        if not (isinstance(x,int) and isinstance(y,int)):
            raise TypeError("prefix_node x,y must both be integers")

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

    def _exists(n):
        """Static helper function that checks whether a node is not invis"""
        return n is not None and modules[n.m]['exists']

    def _isbuf(n):
        """Static helper function that checks whether a node is a buffer"""
        return n is not None and modules[n.m]['buf']

    def _in_tree(n):
        """Static helper function that checks whether a node is in the tree"""
        return n is not None and modules[n.m]['type']=='main'

    def _parse_net(x):
        """Static helper function that converts a net's ID to its name in HDL

        These come in 3 possible flavors:
            - None (unassigned net) -> parsed to n0
            - Integer (assigned net) -> parsed to n`Integer
            - Hardcoded name ($net_name) -> parsed to net_name
        """
        if x is None:
            return "n0"
        if isinstance(x,int):
            return "n"+str(x)
        if "$" in x:
            return x.replace("$","")
        raise TypeError("net stored in node {0} is invalid".format(repr(x)))

    def _verilog(self):
        """Return single line of verilog consisting of module instantiation"""

        # Fill in the module instantiation
        ret="	{3} {0}_{1}_{2} (".format(self.m,self.x,self.y,self.m)
        # Create list of all instance pins and copy in unformatted net IDs
        pins=self.ins.copy()
        pins.update(self.outs)
        # Format net IDs and add them to module instantation line
        for a in pins:
            ret+=" ."+a+"( {"
            ret+=','.join(reversed([prefix_node._parse_net(x) for x in pins[a]]))
            ret+='} ),'
        ret=ret[:-1]+' );'
        return ret

    def _flat(self):
        """Return block of verilog consisting of the module's logic"""

        # Grab module's verilog definition without the header/footer
        ret='\n'.join([x for x in modules[self.m]['verilog'].split('\n')
                      if (x!=''
                          and 'input' not in x
                          and 'output' not in x
                          and 'module' not in x)])
        # Create list of all instance pins and copy in unformatted net IDs
        pins=self.ins.copy()
        pins.update(self.outs)
        # Format net IDs and replace them into module's verilog
        for a in pins:
            if len(pins[a])==1:
                net_name=prefix_node._parse_net(pins[a][0])
                ret=ret.replace(a,net_name)
            else:
                for b in range(len(pins[a])):
                    net_name=prefix_node._parse_net(pins[a][b])
                    ret=ret.replace("{0}[{1}]".format(a,b),net_name)
        return ret

    def flatten(self,flag=True):
        """Determine which verilog representation to output"""
        self.flat=flag

    def hdl(self):
        """Return HDL representation of node"""
        return self._flat() if self.flat else self._verilog()

    def __str__(self):
        """Currently returns same representation as __repr__"""
        return self.__repr__()

    def __repr__(self):
        """Basic representation of node that can partially recreate it"""
        return "prefix_node({0},{1},{2})".format(self.x,self.y,self.m)

    def __lt__(self,value):
        """Define less-than by position in tree"""
        return (self.x,self.y)<(value.x,value.y)

    def __gt__(self,value):
        """Define greater-than by position in tree"""
        return (self.x,self.y)>(value.x,value.y)

class prefix_graph(nx.MultiDiGraph):
    """Defines a di-graph of prefix nodes and edges
    
    The basic internal structure of the graph is a 2-D array of nodes
    """

    def __init__(self, width):
        """Initializes a prefix summation graph

        Pre-condition: width is an integer
        Post-conditions: creates a 2-D array of all nodes; runs nx.DiGraph's init
        """
        if not isinstance(width,int):
            raise TypeError("prefix_graph width must be an integer")
        self.w=width
        # Initialize graph to have a width of width
        self.node_list=[[None]*self.w]

        # Procedurally-generated net names start with "n1"
        self.next_net = 1

        # Procedurally-generated block names start with "block1"
        self.next_block = 1
        self.blocks = [None,None]

        super().__init__(self)

    def __getitem__(self,n):
        """Syntactic sugar to allow self[x,y] instead of self.node_list[y][x]"""
        # Auto-raise error if n is not iterable with the len call
        if len(n)!=2:
            raise ValueError("must input two numbers to access node in graph")
        return self.node_list[n[1]][n[0]]


    def add_node(self, n, style=None, label=None):
        """Adds a prefix_node to the prefix_graph
        
        Pre-condtions:
        0 <= node.x < width
        0 <= node.y <= len(self.node_list) [no skipping levels!!!]
        Post-condition: adds node to graph and 2-D array of all nodes
        """
        if not isinstance(n,prefix_node):
            raise TypeError("can only add prefix_nodes to prefix_graph")
        if not (n.x<self.w and n.x>=0):
            raise ValueError("cannot add a node with x beyond the width")
        if n.y<0:
            raise ValueError("cannot add a node with negative level")
        if n.y>len(self.node_list):
            raise ValueError("cannot skip levels when adding nodes")
        if n in self:
            raise ValueError("trying to double-add a node to the graph")
        if n.y<len(self.node_list) and self[n.x,n.y]!=None:
            raise ValueError("trying to add node to populated grid square")
        if n.y==len(self.node_list):
            self.node_list.append([None]*self.w)
        self.node_list[n.y][n.x]=n
        
        # Add node attributes to NetworkX parent graph class
        # Some of these are used for GraphViz visualization
        n_kwargs = modules[n.m]
        n_kwargs['shape'] = n_kwargs.get('shape','square')
        n_kwargs['fillcolor'] = n_kwargs.get('fillcolor','white')
        n_kwargs['label'] = n_kwargs.get('label','') if label is None else label
        n_kwargs['style'] = n_kwargs.get('style','filled') if style is None else style
        n_kwargs['pos'] = "{0},{1}!".format(-1*n.x,-1*n.y)

        super().add_node(n,**n_kwargs)
        return n

    def remove_node(self, n):
        """Removes node from graph as well as nodelist array"""
        if n==None:
            return
        self.node_list[n.y][n.x]=None
        super().remove_node(n)
        return n

    def add_edge(self, n1, pin1, n2, pin2):
        """Adds an edge between two nodes in the graph

        Pre-conditions:
        n1, n2 are prefix_nodes in this prefix_graph
        n1, n2 are on adjacent levels [use buffers otherwise]
        pin1, pin2 are valid, unassigned, ports of n1, n2, respectively
        only one of (pin1, pin2) is an input, the other being an output
        specifically, to keep code simple, pin1 is output and pin2 is input

        Post-condition: adds edge between target nodes
        """
        p1,b1=pin1; p2,b2=pin2;
        if not isinstance(n1,prefix_node) or not isinstance(n2,prefix_node):
            raise TypeError("can only add edge between nodes")
        if abs(n1.y-n2.y)!=1:
            raise ValueError("cannot add an edge between non-adjacent levels")
        if n2.y<=n1.y:
            raise ValueError("cannot add an edge in the wrong direction")
        if p1 not in n1.outs or p2 not in n2.ins:
            raise ValueError("cannot add an edge between invalid ports")

        # Assigns name to edge, based on order in which it was added
        edge_name = self.next_net
        self.next_net += 1
        # If net is already named, use pre-existing name
        if not n1.outs[p1][b1] is None: edge_name = n1.outs[p1][b1]
        elif not n2.ins[p2][b2] is None: edge_name = n2.ins[p2][b2]
        n1.outs[p1][b1]=edge_name
        n2.ins[p2][b2]=edge_name

        # Styles the edge for GraphViz visualization
        edge_kwargs={'arrowhead':'none',
                     'headport':'ne','tailport':'sw',
                     'ins':pin1,'outs':pin2}
        edge_kwargs['edge_name']=edge_name
        if n2.x==n1.x:
            edge_kwargs['headport']='n'
            edge_kwargs['tailport']='s'
        if prefix_node._isbuf(n1):
            edge_kwargs['tailport']='s'

        # Initialize weight to 1
        edge_kwargs['weight']=1

        # Keep track of which nodes lie upstream
        n2.upstream.add((n1.x,n1.y))
        n2.upstream.update(n1.upstream)

        super().add_edge(n1,n2,**edge_kwargs)


    def remove_all_edges(self,n1,n2):
        """Removes all edges between two nodes

        NetworkX has no way to remove all edges between 2 nodes in a
        MultiGraph?  Keep removing until an Exception is thrown?
        """
        try:
            self.remove_edge(n1,n2)
            return self.remove_all_edges(n1,n2)
        except nx.NetworkXError:
            return

    def add_block(self,*nodes):
        """Creates a new module block of nodes

        This is a group of nodes that are flattened together
        into a single monolithic module.

        Pre-condition:
        nodes is a list of nodes, all of which have attribute block = None
        Post-condition: adds new module block, containing specific nodes
        """
        if not all([n.block is None for n in nodes]):
            raise ValueError("cannot add node to multiple blocks")
        if len([n.y for n in nodes])!=len(set([n.y for n in nodes])):
            raise ValueError("block cannot have multiple nodes on same level")

        # If the list of nodes is empty, return None
        if len(nodes)==0:
            return None
        # Set block attribute for all nodes
        this_block = self.next_block
        for n in nodes:
            n.block = this_block
        # Add block to blocks list
        new_block = set(nodes)
        if this_block==len(self.blocks)-1: self.blocks.append(None)
        self.blocks[this_block]=new_block

        # Find next available block ID
        # This can recycle pre-existing block IDs if they are no longer in use
        # TO-DO: Consider removing this recycling, as it will rarely be useful
        self.next_block = next(x for x in range(1,len(self.blocks)) if self.blocks[x] is None)

        return this_block

    def remove_block(self,block):
        """Deletes a module block definition

        This is a group of nodes that are flattened together
        into a single monolithic module.

        Pre-condition: block is a valid block ID
        Post-condition: removes block
        """
        if block>=len(self.blocks) or self.blocks[block] is None:
            raise ValueError("trying to remove non-existent block")
        # Unsets block attribute for all nodes in block
        for n in self.blocks[block]:
            n.block = None
        # Deletes block itself
        self.blocks[block] = None

    def remove_all_blocks(self):
        """Deletes all module block definitions from graph"""
        for b in range(len(self.blocks)):
            if self.blocks[b] is not None:
                self.remove_block(b)
        self.next_block = 1
        self.blocks = [None,None]

    def longest_path(self):
        """Calculate longest path from any node not in a block to the output

        Note that neither the start nor end point may be a buffer
        (why was this decision made? TO-DO: Re-evaluate this decision)
        """
        # Get ordered list of all nodes
        topo_order = nx.lexicographical_topological_sort(self)
        topo_order = (x for x in topo_order if (x.block is None) \
#                and prefix_node._in_tree(x) \
                )
        # Iterate through graph looking for longest paths
        dists = {}
        for n in topo_order:
            # For each node, first get distances through all predecessors
            weight_list = [(v,dists[v][1]+e[0]['weight']) \
                    for v,e in self.pred[n].items() \
                    if v.block is None]
            # In case of a tie, select left-most beginpoint
            dists[n] = max(weight_list,key = lambda x: (x[1],x[0].x),default=(n,0))
        # Helper function used for filtering
        is_node = lambda n: prefix_node._exists(n)
        # Filter out paths that start with a buffer/invis
        dists = {k:v for k,v in dists.items() if is_node(k) or v[1]!=0}
        # Filter out paths that end in a buffer/invis
        # In case of a tie, select right-most endpoint
        n1 = max(dists,key = lambda x: (x!=dists[x][0],is_node(x),dists[x][1],-dists[x][0].x),default=None)
        # Filter out paths that end in a buffer/invis
        if not is_node(n1): n1 = None
        # Filter out single-element paths:
        if n1==dists[n1][0]: n1 = None
        if dists[n1][0] not in dists: n1 = None
        # If no valid path, return None
        if n1 is None: return None
        # Re-create path
        n2 = None
        path = []
        while n1 != n2:
            if not n1 in dists:
                break
            path.append(n1)
            n2 = n1
            n1 = dists[n1][0]
        return path

    def add_best_blocks(self):
        """Groups nodes belonging to each critical path inside blocks"""
        path = self.longest_path()
        if path is not None:
            self.add_block(*path)
            return self.add_best_blocks()

    def _hdl_blocks(self):
        """Writes HDL of the graph's blocks
        
        Returns a tuple consisting of the HDL string,
        and the block module definitions.
        """

        block_hdl = ""; block_defs = ""

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
                for x in n.ins.values(): ins.update([prefix_node._parse_net(y) for y in x])
                for x in n.outs.values(): outs.update([prefix_node._parse_net(y) for y in x])
            # end iterate over all nodes in a block

            # Should a signal be generated as an output by
            # a node inside the block, it is clearly not a
            # block input, and should not be in the header.
            ins = ins - outs

            # Instantiate block
            inst_b = "	block_{0} block_{0}_instance (".format(b)
            tmp=ins|outs
            # Add ins/outs to block instantiation with dot notation
            for x in tmp: inst_b+=" .{0} ( {1} ),".format(sub_brackets(x),x)
            inst_b=inst_b[:-1]+' );\n'
            # Add block instantiation to block HDL
            block_hdl+=inst_b

            # Define block
            block_def="\nmodule block_{0}(".format(b)
            # List all ins/outs in module definition
            for x in tmp: block_def+=' '+sub_brackets(x)+','
            block_def = block_def[:-1]+');\n\n'
            # Declare all inputs and outputs
            block_def += "	input"
            for x in ins: block_def+=" {0},".format(sub_brackets(x))
            block_def = block_def[:-1]+";\n"

            block_def += "	output"
            for x in outs: block_def+=" {0},".format(sub_brackets(x))
            block_def = block_def[:-1]+";\n"
            # Put all nodes' hdl inside block definition
            block_def += '\n'
            for n in nodes:
                if modules[n.m]['type']=='post':
                    tmp = n.ins['pin'][0]
                    n.ins['pin'][0]="$p{0}".format(n.x)
                    n.flatten()
                    block_def+=sub_brackets(n.hdl())+'\n'
                    n.ins['pin'][0] = tmp
                else:
                    n.flatten()
                    block_def+=sub_brackets(n.hdl())+'\n'
            # Write "\nendmodule\n" line
            block_def+="\nendmodule\n"
            # Add block definition to list of block_defs
            block_defs+=block_def

        # end iterate over all blocks
        return (block_hdl,block_defs)
        

    def _hdl_preamble(self):
        """Defines the preamble of the graph's HDL
        
        This abstract method is meant to be implemented by child classes.

        Returns a tuple consisting of the HDL string,
        and any modules used by the preamble.
        """
        return ("",set())

    def hdl(self,out=None,mapping="behavioral",full_flat=False):
        """Outputs HDL representation of graph
        
        out is an optional file to write the HDL to
        full_flat is an optional argument that can fully flatten the netlist
        """
        if out is not None:
            outdir = pathlib.Path(out).resolve().parent
            if not outdir.exists():
                raise FileNotFoundError("desired path for hdl output is invalid")

        block_hdl=""; block_defs=""

        # Pull in HDL preamble, as defined by child class 
        hdl, module_defs = self._hdl_preamble()

        # Iterate over all nodes in graph
        for a in self.node_list:
            for n in a:
                # Skip pre/post nodes
                if not prefix_node._in_tree(n):
                    continue
                # Skip nodes inside a block
                if n.block is not None:
                    continue
                # Flatten invis nodes
                if not prefix_node._exists(n):
                    n.flatten()
                # If full_flat, flatten all nodes
                if full_flat:
                    n.flatten()
                # Add in HDL
                hdl += n.hdl()+'\n'
                # Mark the node's module as in-use
                module_defs.add(n.m)
            hdl += '\n'

        # Pull in HDL of blocks
        block_hdl, block_defs = self._hdl_blocks()

        hdl += block_hdl

        # End main module
        hdl += "endmodule\n"

        # Turn module defs to text
        module_def_text = ""
        for a in module_defs:
            module_def_text+=modules[a]['verilog']
        # Add in block defs
        module_def_text += block_defs

        # Combine main module and module defs
        hdl = hdl + module_def_text

        # Write to file
        if out is not None:
            
            with open(out,'w') as f:
                print(hdl,file=f)

            # Copy mapping file from package to local directory
            with importlib.resources.path("pptrees","mappings") as pkg_map_dir:
                pkg_map_file = pkg_map_dir / (mapping+'_map.v')
                local_map_file = outdir / (mapping+'_map.v')
                # Use shutil.copy to avoid loading file into memory
                shutil.copy(pkg_map_file,local_map_file)

        return hdl

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
