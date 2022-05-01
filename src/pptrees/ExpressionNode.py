from .modules import modules
from .util import parse_net

class ExpressionNode:
    """Defines a node in an expression tree

    Attributes:
        children (list): A list of child nodes
            Note that this list is ordered, and the first child is rightmost
        parent (ExpressionNode): The parent node
        value (str): The value of the node; a module name
        leafs (int): An integer encoding all leafs reachable from this node
        block (int): The block number of this node's HDL (if applicable)
        in_nets (list): A list of input nets
        out_nets (list): A list of output nets
        x_pos (int): The x-coordinate of this node's graphical representation
        y_pos (int): The y-coordinate of this node's graphical representation
    """
    def __init__(self, value, x_pos=0, y_pos=0):
        """Initializes a new ExpressionNode

        Args:
            value (str): The value of the node; a valid module name
            x_pos (int): The x-coordinate of this node's graphical representation
            y_pos (int): The y-coordinate of this node's graphical representation
        """
        if not isinstance(x_pos, int):
            raise TypeError("X-coordinate must be an integer")
        if not isinstance(y_pos, int):
            raise TypeError("Y-coordinate must be an integer")
        if value not in modules:
            raise ValueError("Invalid module name: {}".format(value))

        # Node attributes
        self.value = value

        # HDL-related attributes
        self.in_nets = {x: [None] * y for x, y, z in modules[value]["ins"]}
        self.out_nets = {x: [None] * y for x, y in modules[value]["outs"]}

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
        return "{0}_{1}_{2}_{3}".format(self.value, self.leafs, self.x_pos, self.y_pos)

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

    def __hash__(self):
        """Returns the hash of this node"""
        return hash(self.__repr__())

    def add_child(self, child, pin1, pin2, net_name):
        """Adds a child node to this node

        Args:
            child (ExpressionNode): The child node to add
            pin1 (tuple): (name, index) of the parent pin
            pin2 (tuple): (name, index) of the child pin
            net_name (str): Fall-back net name, if it does not exist
        """

        if pn1 not in self.out_nets or pn2 not in child.in_nets:
            raise ValueError("Invalid pin connection")

        # Connect correct ports
        pn1, pi1 = pin1
        pn2, pi2 = pin2

        ## Check if net already exists
        if not (self.out_nets[pn1][pi1] is None):
            net_name = self.out_nets[pn1][pi1]
        elif not (child.in_nets[pn2][pi2] is None):
            net_name = child.in_nets[pn2][pi2]

        ## Assign net name to ports
        node1.out_nets[pn1][pi1] = net_name
        node2.in_nets[pn2][pi2] = net_name

        # If nodes are not already connected, connect them
        if child.parent != self:
            self.children.append(child)
            self.leafs = self.leafs | child.leafs
            child.parent = self

        return net_name

    def remove_child(self, child):
        """Removes a child node from this node

        Args:
            child (ExpressionNode): The child node to remove
        """
        self.children.remove(child)
        child.parent = None
        # Recalculate leafs
        self.leafs = 0
        for c in self.children:
            self.leafs = self.leafs | c.leafs

    def hdl(self, language="verilog",flat=False):
        """Returns the HDL of this node

        Args:
            language (str): The language in which to generate the HDL
            flat (bool): If True, flatten the node's HDL

        Returns:
            str: The HDL of this node
            list: Set of HDL module definitions used in the node
        """
        if not flat and language == "verilog":
            return (self._verilog(), set(modules[self.value][language]))
        if not flat and language == "vhdl":
            return (self._vhdl(), set(modules[self.value][language]))
        if flat and language == "verilog":
            return (self._verilog_flat(), set())
        if flat and language == "vhdl":
            return (self._vhdl_flat(), set())

    def _verilog(self):
        """Return single line of Verilog consisting of module instantiation"""

        # Instantiate module
        ret = "\t{0} U0 (".format(self.value)

        # Create list of all instance pins and copy in unformatted net IDs
        pins = self.in_nets.copy()
        pins.update(self.out_nets)

        # Format net IDs into the module instantiation
        for a in pins:
            b = reversed([parse_net(x) for x in pins[a]])
            ret += " .{0}( {{ {1} }} ),".format(a)
        ret = ret[:-1] + " );\n"

        return ret

    def _vhdl(self):
        """Return single line of VHDL consisting of module instantiation"""

        # Instantiate module
        ret = "\tU0: {0}\n".format(self.value)
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
        ret = ret[:-1] + "\n\t\t);\n"

        return ret

    def _verilog_flat(self):
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

if __name__ == "__main__":
    raise RuntimeError("This module is not intended to be run directly")
