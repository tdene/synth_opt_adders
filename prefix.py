from modules import modules

# Defines a node in the adder graph
class adder_node():

# Nodes have an x position (bit), y position (level),
# the module they are representing (black, grey, etc),
# and two dictionary of edges

    # Pre-conditions:
    # x, y are integers
    # module is a valid module from modules

    # Post-conditions:
    # stores all these values into internal variables
    # creates two dictionaries of input/output edges

    def __init__(self, x, y, module):
        if not (isinstance(x,int) and isinstance(y,int)):
            raise TypeError("adder_node x,y must both be integers")
        if module not in modules:
            raise ValueError("trying to create node with invalid module")
        self.x=x; self.y=y; self.m=module;

        # Create inputs and outputs dictionaries; initialize to None
        self.ins={x:[None]*y for x,y in modules[self.m]['ins']}
        self.outs={x:[None]*y for x,y in modules[self.m]['outs']}

    def __str__(self):
        return "Adder node of module {2} at bit {0} and level {1}"\
               .format(self.x,self.y,self.m)

    def __repr__(self):
        return "adder_node({0},{1},{2})".format(self.x,self.y,self.m)


# Defines a di-graph of adder nodes and edges
# The basic internal structure of the graph is a 2-D array of nodes
# The graph also includes a list of start nodes to make it easy to traverse
class adder_graph():

    # Note that self.nodes is accessed in the order self.nodes[y][x], not [x][y]

    # Pre-condition: width is an integer
    # Post-condition: creates a list of start nodes and a 2-D array of all nodes

    def __init__(self, width):
        if not isinstance(width,int):
            raise TypeError("adder_graph width must be an integer")
        self.width=width
        # Initialize graph to contain `width number of 'input' nodes
        # Note that self.nodes is accessed in the order self.nodes[y][x], not [x][y]
        self.start_nodes=[adder_node(self.width-x,0,'adder_input') for x in range(self.width)]
        self.nodes=[self.start_nodes]


    # Pre-condtions:
    # 0 <= x < width
    # 0 <= y <= len(self.nodes) [no skipping levels!!!]
    # module is a valid module from modules

    # Post-condition: adds node to 2-D array of all nodes
    def add_node(self, x, y, module):
        if not (x<self.width and x>=0):
            raise ValueError("cannot add a node with x beyond the width")
        if y<0:
            raise ValueError("cannot add a node with negative level")
        if y>len(self.nodes):
            raise ValueError("cannot skip levels when adding nodes")
        if module not in modules:
            raise ValueError("trying to add node with invalid module")
        if y==len(self.nodes):
            self.nodes.append([None]*self.width)
        self.nodes[y][x]=adder_node(x,y,module)

    # Pre-conditions:
    # n1, n2, are 2-element integer arrays, [x,y] describing valid nodes
    # n1, n2 are on adjacent levels [use buffers otherwise]
    # p1, p2 are valid, unassigned, ports of n1, n2, respectively
    # only one of (p1, p2) is an input, the other being an output
    # specifically, to keep code simple, p1 is output and p2 is input

    # Post-condition: adds edge between target nodes
    def add_edge(self, n1, p1, n2, p2):
        x1,y1=n1; x2,y2=n2;
        if abs(y1-y2)!=1:
            raise ValueError("cannot add an edge between non-adjacent levels")
        if p1 not in n1.outs or p2 not in n2.ins:
            raise ValueError("cannot add an edge between invalid ports")
        if n1.outs[p1]!=None or n2.ins[p2]!=None:
            raise ValueError("cannot overload node ports with extra edges")

        n1.outs[p1]=n2; n2.ins[p2]=n1;

class prefix():

    def __init__(self,w,l,f,t):
        if(self.w!=2**(w.bit_length())):
            raise ValueError("Program currently only support widths that are powers of two")
        self.w=w;
        tmp=w.bit_length();
        if not(all([(x>=0 and x<tmp) for x in [l,f,t]])):
            raise ValueError("l, f, and t parameters must all be within the range [0,L-1]")
        self.l=l; self.l_=l+tmp;
        self.f=f; self.f_=1+1<<f;
        self.t=t; self.t_=1<<t;

        self.graph = adder_graph(self.w)

    def __str__(self):
        return "Prefix adder with {0} width, {1} logic levels, {2} fan-out, {3} wire tracks"\
                .format(self.w,self.l_,self.f_,self.t_)

    def __repr__(self):
        return "adder({0},{1},{2},{3})".format(self.w,self.l,self.f,self.t)

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
