from .modules import modules
from .utils import parse_net

class ExpressionNode:
    """Defines a node in an expression tree

    Attributes:
        nid (int): The unique ID of this node
        children (list): A list of child nodes
        parent (ExpressionNode): The parent node
        value (str): The value of the node; a module name
        leafs (int): An integer encoding all leaf nodes reachable from this node
        flat (bool): Whether or not this node's HDL should be flattened
        block (int): The block number of this node's HDL (if applicable)
        in_nets (list): A list of input nets
        out_nets (list): A list of output nets
        x_pos (int): The x-coordinate of this node's graphical representation
        y_pos (int): The y-coordinate of this node's graphical representation
    """
    def __init__(self, nid, value, x_pos, y_pos, children=[], parent=None):
        """Initializes a new ExpressionNode

        Args:
            value (str): The value of the node; a valid module name
            children (list): A list of child nodes
            parent (ExpressionNode): The parent node
        """
        if value not in modules:
            raise ValueError("Invalid module name: {}".format(value))

        # Node attributes
        self.nid = nid
        self.children = children
        self.parent = parent
        self.value = value

        # HDL-related attributes
        self.flat = False
        self.in_nets = {x: [None] * y for x, y in modules[value]["ins"].items()}
        self.out_nets = {x: [None] * y for x, y in modules[value]["outs"].items()}

        # Graph-related attributes
        self.leafs = 0
        self.block = None

        # Visualization-related attributes
        self.x_pos = x_pos
        self.y_pos = y_pos

    def __str__(self):
        """Returns a string representation of this node"""
        return self.value

    def __repr__(self):
        """Returns a string representation of this node"""
        return (self.value, self.nid, self.x_pos, self.y_pos)

    def __lt__(self, other):
        """Compares this node to another node by position in tree

        Args:
            other (ExpressionNode): The node to compare to

        Returns:
            bool: Whether or not this node is further right than the other node
        """
        return self.leafs < other.leafs

    def __eq__(self, other):
        """Compares this node to another node by position in tree

        Args:
            other (ExpressionNode): The node to compare to

        Returns:
            bool: Whether or not this node is in the same position as the other node
        """
        return self.leafs == other.leafs

    def __gt__(self, other):
        """Compares this node to another node by position in tree

        Args:
            other (ExpressionNode): The node to compare to

        Returns:
            bool: Whether or not this node is further left than the other node
        """
        return self.leafs > other.leafs

    def add_child(self, child):
        """Adds a child node to this node

        Args:
            child (ExpressionNode): The child node to add
        """
        self.children.append(child)
        self.leafs = self.leafs | child.leafs
        child.parent = self

    def remove_child(self, child):
        """Removes a child node from this node

        Args:
            child (ExpressionNode): The child node to remove
        """
        self.children.remove(child)
        self.leafs = self.leafs & ~child.leafs
        child.parent = None

    def toggle_flat(self):
        """Flattens or unflattens the HDL of this node"""
        self.flat = not self.flat

    def hdl(self, language="verilog"):
        """Returns the HDL of this node

        Args:
            language (str): The language to return the HDL in

        Returns:
            str: The HDL of this node
        """
        if not self.flat and self.language == "verilog":
            return self._verilog()
        if not self.flat and self.language == "vhdl":
            return self._vhdl()
        if self.flat and self.language == "verilog":
            return self._flat_verilog()
        if self.flat and self.language == "vhdl":
            return self._flat_vhdl()

    def _verilog(self):
        """Return single line of Verilog consisting of module instantiation"""

        # Instantiate module
        ret = "\t{0} U{1} (".format(self.value, self.nid)

        # Create list of all instance pins and copy in unformatted net IDs
        pins = self.in_nets.copy()
        pins.update(self.out_nets)

        # Format net IDs into the module instantiation
        for a in pins:
            b = reversed([parse_net(x) for x in pins[a]])
            ret += " .{0}( {{ {1} }} ),".format(a)
        ret = ret[:-1] + " );"

        return ret

    def _vhdl(self):
        """Return single line of VHDL consisting of module instantiation"""

        # Instantiate module
        ret = "\tU{1}: {0}\n".format(self.value, self.nid)
        ret += "\t\tport map ("

        # Create list of all instance pins and copy in unformatted net IDs
        pins = self.in_nets.copy()
        pins.update(self.out_nets)

        # Format net IDs into the module instantiation
        for a in pins:
            for b in range(len(pins[a])):
                net_name = parse_net(pins[a][b])
                ret += "\n\t\t\t{0}({1}) => {2},".format(a, b, net_name)

        # Close parenthesis
        ret = ret[:-1] + "\n\t\t);"

        return ret

    def _flat_verilog(self):
        """Return Verilog consisting of the module's internal logic"""

        ### Grab only instantiated cells from the HDL definiton

        # Iterate over each line in the HDL definition
        hdl_def = modules[self.value][language].splitlines()

        # Flag whether we're currently looking at a cell
        in_std_cell = False

        # Store the filtered HDL in a string
        ret = ""

        for l in hdl_def:
            if "assign" in l or "<=" in l:
                ret += l + "\n"
            else:
                if "U" in l:
                    in_std_cell = True
                if in_std_cell == True:
                    ret += l + "\n"
                if l != "" and l[-1] == ";":
                    in_std_cell = False

        # Create list of all instance pins and copy in unformatted net IDs
        pins = self.ins.copy()
        pins.update(self.outs)

        # Format net IDs and replace them into module's HDL
        for a in pins:
            if len(pins[a]) == 1:
                net_name = parse_net(pins[a][0])
                ret = ret.replace(a, net_name)
            else:
                for b in range(len(pins[a])):
                    net_name = parse_net(pins[a][b])
                    ret = ret.replace("{0}[{1}]".format(a, b), net_name)

        return ret[:-1]
