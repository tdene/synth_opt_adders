from copy import deepcopy

from .node_data import node_data
from .util import lg, parse_net, verso_pin


class ExpressionNode:
    """Defines a node in an expression tree

    Attributes:
        children (list): A list of child nodes
            Note that this list is ordered for trees,
            and the first child is leftmost
        parent (ExpressionNode): The parent node
        value (str): The value of the node; a module name
        node_data (dict): The data associated with the node
        leafs (int): A binary encoding of all leafs reachable from this node
        graph (ExpressionGraph): The graph this node belongs to
        block (int): The block number of this node's HDL (if applicable)
        in_nets (dict): A dictionary of input nets
        out_nets (dict): A dictionary of output nets
        x_pos (float): The x-coordinate of this node's graphical representation
        y_pos (float): The y-coordinate of this node's graphical representation
        equiv_class (list of ExpressionNode): The list of all nodes equivalent
            to this one. The first node in the list is special, and is known
            as the representative of the equivalence class.
        equiv_wires (set of strings): The set of wires that are output by the
            representative node of this node's equivalence class.
        tracks_class (list of ExpressionNode): The list of all nodes that cause
            parallel wires in the layout. No node in this list is special.
    """

    def __init__(self, value, x_pos=0, y_pos=0, custom_data=None):
        """Initializes a new ExpressionNode

        Args:
            value (str): The value of the node; a valid module name
            x_pos (float): The x-coord of this node's graphical representation
            y_pos (float): The y-coord of this node's graphical representation
        """
        if not isinstance(x_pos, (int, float)):
            raise TypeError("X-coordinate must be a number")
        if not isinstance(y_pos, (int, float)):
            raise TypeError("Y-coordinate must be a number")
        if value not in node_data and custom_data is None:
            raise ValueError("Invalid module name: {}".format(value))

        # Node attributes
        self.value = value
        if custom_data is None:
            self.node_data = deepcopy(node_data[value])
        else:
            self.node_data = deepcopy(custom_data)
        self.children = []
        self.parent = None

        # HDL-related attributes
        self.in_nets = {x: [None] * y for x, y, *z in self.node_data["ins"]}
        self.out_nets = {x: [None] * y for x, y in self.node_data["outs"]}

        # Graph-related attributes
        self.leafs = 0
        self.graph = None
        self.block = None
        self.equiv_class = [self]
        self.equiv_wires = set()
        self.tracks_class = set()
        self.tracks_class.add(self)

        # Visualization-related attributes
        ### NOTE: The use of these attributes is no longer restricted to
        ### visualization. Somehow these attributes now play an integral
        ### role in the function of the library. Code rot has begun to
        ### set in before the official release of V1.0
        self.x_pos = x_pos
        self.y_pos = y_pos

    def __str__(self):
        """Returns a string representation of this node"""
        return self.__repr__()

    def __repr__(self):
        """Returns a string representation of this node"""
        return "{0}_{1}_{2}".format(self.value, self.x_pos, self.y_pos)

    def __len__(self):
        """Returns the height of the subtree rooted at this node"""
        if not self.children:
            return 0
        return 1 + max([len(x) for x in self])

    def __lt__(self, other):
        """Compares this node to another node by position in tree

        Args:
            other (ExpressionNode): The node to compare to

        Returns:
            bool: Whether or not this node is further right than the other node
        """
        return self.leafs < other.leafs

    def __gt__(self, other):
        """Compares this node to another node by position in tree

        Args:
            other (ExpressionNode): The node to compare to

        Returns:
            bool: Whether or not this node is further left than the other node
        """
        return self.leafs > other.leafs

    def __copy__(self):
        """Redefine __copy__"""
        return ExpressionNode(self.value)

    def copy(self):
        """Shorthand for __copy__"""
        return self.__copy__()

    ### NOTE: This should just convert the subtrees each node roots
    ### into their labels, and then compare the two strings
    ### TO-DO: Implement the above
    def equiv(self, other):
        """Checks if this node is equivalent to another node
        Cannot do this with __eq__ because NetworkX uses __eq__

        Args:
            other (ExpressionNode): The node to compare to
        """
        if not isinstance(other, ExpressionNode):
            raise TypeError("Cannot compare to non-ExpressionNode")

        # Check whether self and other are equivalent
        ret = not (self > other) and not (self < other)
        ret = ret and self.value == other.value

        # Check whether their subtrees are also equivalent
        for a in range(len(self.children)):
            if self[a] is not None:
                try:
                    other_c = other[a]
                except IndexError:
                    return False
                ret = ret and self[a].equiv(other_c)

        return ret

    def set_equiv(self, other):
        """Sets two nodes as equivalent

        If either already has an equivalence class assigned,
        the two classes are merged.

        If the nodes are in a graph that possesses a width attribute,
        priority is given to the nodes with higher width.
        Otherwise, priority is given to self.

        Args:
            other (ExpressionNode): The node to compare to
        """
        if not isinstance(other, ExpressionNode):
            raise TypeError("Cannot compare to non-ExpressionNode")
        if not self.equiv(other):
            raise ValueError("Nodes are not equivalent")

        # Grab both nodes' equivalence classes
        ec1 = self.equiv_class
        ec2 = other.equiv_class
        # Merge them
        ec = ec1.copy()
        for n in ec2:
            if n not in ec:
                ec.append(n)
        # If the two nodes' graphs have a width attribute,
        # sort the nodes by width
        if hasattr(self.graph, "width") and hasattr(other.graph, "width"):
            ec.sort(key=lambda x: x.graph.width, reverse=True)

        # In order to write out correct HDL,
        # each node must be aware of its representative's output nets.
        equiv_wires = [wire for net in ec[0].out_nets.values() for wire in net]
        # Set all nodes' equivalence classes to the result
        for n in ec:
            n.equiv_class = ec
            # Set each node's equiv_wires
            n.equiv_wires = set(equiv_wires)

        # Return the final equivalence class
        return ec

    def make_representative(self):
        """Makes this node the representative of its equivalence class"""
        ec = self.equiv_class.copy()
        # If the representative is not the first node in the class,
        # swap it with the first node in the class
        if ec[0] != self:
            ec.remove(self)
            ec.insert(0, self)
        # Reset equiv_wires
        equiv_wires = [wire for net in ec[0].out_nets.values() for wire in net]
        # Set all nodes in the class to the representative
        for n in ec:
            n.equiv_class = ec
            n.equiv_wires = equiv_wires

        # Return the final equivalence class
        return ec

    def is_bifurcation(self):
        """Checks whether the equivalence class of this node bifurcates

        That is to say, this answers ∃n ≡ self s.t n.parent !≡ self.parent
        """
        # Filter out None parents
        if self.parent is None:
            self_parent_equiv = None
        else:
            self_parent_equiv = self.parent.equiv_class[0]

        ret = False
        for n in self.equiv_class:
            if n.parent is None:
                continue
            n_parent_equiv = n.parent.equiv_class[0]
            if n_parent_equiv != self_parent_equiv:
                ret = True
                break
        return ret

    ### NOTE: Where this logic belongs is an open question
    def tracks(self, other):
        """Checks if self and other cause a need for parallel wires

        Args:
            other (ExpressionNode): The node to compare to
        """
        if not isinstance(other, ExpressionNode):
            raise TypeError("Cannot compare to non-ExpressionNode")

        # If the two nodes have different heights, they cannot lead
        # in a need for increased wire tracks???
        # NOTE: Requires further investigation
        # This makes sense classically, but does it make sense in general?
        if len(self) != len(other):
            return False

        # If either node is root, they cannot cause a need for parallel wires
        if self.parent is None or other.parent is None:
            return False

        # If either node is not the representative of its equivalence class
        # There is no physical meaning to this metric
        if (self.equiv_class[0] is not self) or (
            other.equiv_class[0] is not other
        ):
            return False

        # Check if the edges lead to parallel routes
        if self < other and other < self.parent and self.parent < other.parent:
            return True
        if self > other and other.parent > self and self.parent > other.parent:
            return True
        return False

    ### NOTE: Where this logic belongs is an open question
    def set_tracks(self, other):
        """Sets two nodes as causing parallel wires for each other"""
        if not self.tracks(other):
            raise ValueError("Nodes do not cause parallel routes")

        tr = self.tracks_class
        tr |= other.tracks_class
        other.tracks_class = tr

    def __iter__(self):
        """Iterates over the children of this node"""
        return iter(self.children)

    def __getitem__(self, key):
        """Returns the child node at the given index"""
        return self.children[key]

    def morph(self, value):
        """Morphs this node to a new value

        This will error out if the node has a parent or children.
        """
        if self.parent is not None or any([x is not None for x in self]):
            raise ValueError("Cannot morph a node with children or parents")
        if value not in node_data:
            raise ValueError("Invalid module name: {}".format(value))

        # Create new node
        new_node = ExpressionNode(value, self.x_pos, self.y_pos)
        new_node.leafs = self.leafs
        new_node.block = self.block

        return new_node

    def is_complete(self):
        """Checks if the subtree rooted at this node is complete"""
        # Avoid repeated height calculations (to some degree)
        c_heights = [len(c) for c in self]
        height = 1 + max(c_heights)
        # First confirm the subtree has minimal height
        if 1 << (height - 1) >= bin(self.leafs).count("1"):
            return False
        # Confirm that the children have heights consistent with completeness
        prev_d = height - 1
        for d in c_heights:
            if d > prev_d:
                return False
            prev_d = d
        # Iterate through the children, left to right
        # If a child is proper, proceed to the next one
        # Otherwise, check if the child is improper but complete
        for c in self:
            if not c.is_proper():
                if c.children:
                    return c.is_complete()
                # If there are no grandchildren, it's time to check handedness
                try:
                    idx = c.children.index(None)
                except ValueError:
                    return True
                return idx == bin(c.leafs).count("1")
        # Fall-through case if all children are proper and have the same height
        return True

    def is_proper(self):
        """Checks if the subtree rooted at this node is proper"""
        return 1 << len(self) == bin(self.leafs).count("1")

    def rightmost_leaf(self):
        """Finds the least significant leaf descendant of this node"""
        # Get the target leaf
        target = 1 << (len(bin(self.leafs)) - len(bin(self.leafs).rstrip("0")))
        # Iterate over all children
        for c in self:
            if c is None:
                continue
            if c.leafs & target:
                return c.rightmost_leaf()
        return self

    def leftmost_leaf(self):
        """Finds the most significant leaf descendant of this node"""
        # Get the target leaf
        target = 1 << lg(self.leafs)
        # Iterate over all children
        for c in self:
            if c is None:
                continue
            if c.leafs & target:
                return c.leftmost_leaf()
        return self

    def add_child(self, child, pin1, pin2, net_name):
        """Adds a child node to this node

        Args:
            child (ExpressionNode): The child node to add
            pin1 (tuple): (name, index) of the parent pin
            pin2 (tuple): (name, index) of the child pin
            net_name (str): Fall-back net name, if it does not exist
        """

        # Break the pins apart into names and indices
        pin_name1, pin_index1 = pin1
        pin_name2, pin_index2 = pin2

        if pin_name1 not in self.in_nets or pin_name2 not in child.out_nets:
            raise ValueError("Invalid pin connection")

        ## Check if net already exists
        if not (self.in_nets[pin_name1][pin_index1] is None):
            net_name = self.in_nets[pin_name1][pin_index1]
        elif not (child.out_nets[pin_name2][pin_index2] is None):
            net_name = child.out_nets[pin_name2][pin_index2]

        ## Assign net name to ports
        self.in_nets[pin_name1][pin_index1] = net_name
        child.out_nets[pin_name2][pin_index2] = net_name

        # If nodes are not already connected, connect them
        if child.parent is not self:
            try:
                index = self.children.index(None)
                self.children[index] = child
            except ValueError:
                self.children.append(child)
            child.parent = self
            # Recalculate leafs recursively
            self._recalculate_leafs()

        return net_name

    def remove_child(self, child):
        """Removes a child node from this node

        Args:
            child (ExpressionNode): The child node to remove
        """

        # Remove child/parent connection
        index = self.children.index(child)
        self.children[index] = None
        child.parent = None

        # Reset net names in parent (inpins only!)
        for pin_name, pins in self.in_nets.items():
            # Check if port is connected to this child
            vrs = verso_pin(pin_name)
            if vrs not in child.out_nets:
                continue
            # If so, query the port pin by pin
            for pin_index in range(len(pins)):
                net = pins[pin_index]
                if net is None:
                    continue
                if net in child.out_nets[vrs]:
                    pins[pin_index] = None

        # Recalculate leafs recursively
        self._recalculate_leafs()

    def iter_down(self, fun):
        """Calls a function on this node and all descendants

        Args:
            fun (function): The function to call on each child
        """
        fun(self)
        for c in self:
            if c is not None:
                c.iter_down(fun)

    ### NOTE: THIS ASSUMES THAT PARENTS AND CHILDREN ARE FULLY CONNECTED
    ### TO-DO: Handle case of partially connected nodes
    def _recalculate_leafs(self, leafs=0):
        """Recalculates the leafs of this node and its parents"""
        self.leafs = leafs
        for c in self:
            if c is None:
                continue
            self.leafs = self.leafs | c.leafs
        if self.parent is not None:
            self.parent._recalculate_leafs()

    def hdl(self, language="verilog", flat=False):
        """Returns the HDL of this node

        Args:
            language (str): The language in which to generate the HDL
            flat (bool): If True, flatten the node's HDL

        Returns:
            str: The HDL of this node
            list: Set of HDL module definitions used in the node
        """
        if not flat and language == "verilog":
            return (self._verilog(), (self.node_data[language],))
        if not flat and language == "vhdl":
            return (self._vhdl(), (self.node_data[language],))
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
            b = ",".join([parse_net(x) for x in pins[a]])
            ret += " .{0}( {{ {1} }} ),".format(a, b)
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

        # If this node is part of an equivalence class,
        # but not the main representative,
        # replace its HDL by assign statements
        if self is not self.equiv_class[0]:
            # But if this node is part of a bigger subtree
            # There is no need to even do assign statements
            # The equivalent subtree will take care of everything
            if self.parent.equiv_class[0] != self.parent:
                return ""
            ret = ""
            virtual = self.equiv_class[0].out_nets
            for v in virtual:
                port = virtual[v]
                for a in range(len(port)):
                    net = port[a]
                    n = ExpressionNode("invis")
                    n.in_nets["A"][0] = net
                    n.out_nets["Y"][0] = self.out_nets[v][a]
                    ret += n.hdl(language="verilog", flat=True)[0]
            return ret

        ### Grab only instantiated cells from the HDL definiton

        # Iterate over each line in the HDL definition
        hdl_def = self.node_data["verilog"].splitlines()

        # Flag whether we're currently looking at a cell
        in_std_cell = False

        # Store the filtered HDL in a string
        ret = ""

        for line in hdl_def:
            if "assign" in line:
                ret += line + "\n\n"
            else:
                if "U" in line:
                    in_std_cell = True
                if in_std_cell:
                    ret += line + "\n\n"
                if line != "" and line[-1] == ";":
                    in_std_cell = False

        # Create list of all instance pins and copy in unformatted net IDs
        pins = self.in_nets.copy()
        pins.update(self.out_nets)

        # Format net IDs and replace them into module's HDL
        for a in pins:
            if len(pins[a]) == 1:
                net_name = parse_net(pins[a][0])
                ret = ret.replace(a, net_name)
            else:
                for b in range(len(pins[a])):
                    net_name = parse_net(pins[a][b])
                    idx = len(pins[a]) - b - 1
                    ret = ret.replace("{0}[{1}]".format(a, idx), net_name)

        return ret[:-1]


if __name__ == "__main__":
    raise RuntimeError("This module is not intended to be run directly")
