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

    # Static helper function that checks whether a node is not a buffer

    def _exists(n):
        return n is not None and n.m not in ['buffer_node']

    # The node object has dictionaries of input/output edges
    # These come in 3 possible flavors:
    # - None (unassigned net) -> parsed to 1'b0
    # - Integer (assigned net) -> parsed to n`Integer
    # - Hardcoded value (x'bx) -> kept as is
    # This is a static method that performs this conversion

    def _parse_net(x):
        if x is None:
            return "1'b0"
        if isinstance(x,int):
            return "n"+str(x)
        if "'" in x:
            return x
        raise TypeError("net stored in node {0} is invalid",repr(self))

    # Return single line of verilog consisting of module instantiation

    def _verilog(self):
        ret="{3} {0}_{1}_{2} (".format(self.m,self.x,self.y,self.m)
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
class adder_graph(nx.MultiGraph):

    # Pre-condition: width is an integer
    # Post-conditions: creates a 2-D array of all nodes; runs nx.DiGraph's init

    def __init__(self, width):
        if not isinstance(width,int):
            raise TypeError("adder_graph width must be an integer")
        self.w=width
        # Initialize graph to "width" of width
        self.node_list=[[None]*self.w]

        super().__init__(self)

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
        
        shape = modules[n.m].get('shape','square')
        fillcolor = modules[n.m].get('color','white')

        label=modules[n.m].get('label','') if label is None else label
        style=modules[n.m].get('style','filled') if style is None else style

        pos="{0},{1}!".format(-1*n.x,-1*n.y)

        super().add_node(n,shape=shape,label=label,pos=pos,
                         fillcolor=fillcolor,style=style)

    # Removes node from nodelist array as well as graph

    def remove_node(self, n):
        if n==None:
            return
        self.node_list[n.y][n.x]=None
        super().remove_node(n)

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
#        if abs(n1.y-n2.y)!=1:
#            raise ValueError("cannot add an edge between non-adjacent levels")
        if n2.y<=n1.y:
            raise ValueError("cannot add an edge in the wrong direction")
        if p1 not in n1.outs or p2 not in n2.ins:
            raise ValueError("cannot add an edge between invalid ports")

        n1.outs[p1][b1]=n2.ins[p2][b2]=len(self.edges)

        if p1!='pout':
            super().add_edge(n1,n2,arrowhead='none',ins=pin1,outs=pin2)

    # NetworkX has no way to remove all edges between 2 nodes in a MultiGraph?
    # Keep removing until an Exception is thrown?

    def remove_all_edges(self,n1,n2):
        try:
            self.remove_edge(n1,n2)
            return self.remove_all_edges(n1,n2)
        except nx.NetworkXError:
            return

    # Simplify self.node_list[y][x] to self[x,y]
    def __getitem__(self,n):
        # Auto-raise error if n is not iterable with the len call
        if len(n)!=2:
            raise ValueError("must input two numbers to access node in graph")
        return self.node_list[n[1]][n[0]]

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
