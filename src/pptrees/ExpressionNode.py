from .EquivClass import EquivClass
from .node_data import node_data
from .util import change_in_nets, lg, parse_net, verso_pin


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
        equiv_class (EquivClass): The equivalence class of this node
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
        ### NOTE: This is not a deepcopy
        ### This is done for performance purposes.
        ### It causes no problems, for now.
        if custom_data is None:
            self.node_data = node_data[value].copy()
        else:
            self.node_data = custom_data.copy()
        self.children = []
        self.parent = None

        # HDL-related attributes
        self.in_nets = {x: [None] * y for x, y, *z in self.node_data["ins"]}
        self.out_nets = {x: [None] * y for x, y in self.node_data["outs"]}

        # Graph-related attributes
        self.leafs = 0
        self.graph = None
        self.block = None
        self.equiv_class = EquivClass(self)

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
        return "{0}_{1}_{2}".format(
            self.value, lg(self.leafs), lg(self.leafs & -self.leafs)
        )

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
        if not isinstance(value, str) and not isinstance(value, dict):
            raise TypeError("Invalid value type")
        if isinstance(value, str) and value not in node_data:
            raise ValueError("Invalid module name: {}".format(value))

        # Create new node
        if isinstance(value, dict):
            name = value["verilog"].split("module ")[1].split("(")[0]
            new_node = ExpressionNode(
                name, self.x_pos, self.y_pos, custom_data=value
            )
        else:
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
                # If there are no grandchildren it's time to check handedness
                try:
                    idx = c.children.index(None)
                except ValueError:
                    return True
                return idx == bin(c.leafs).count("1")
        # Fall-through case if all children are proper and the same height
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
            child.equiv_class.parents.add(self)
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
        child.equiv_class.parents.discard(self)

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

    def hdl(self, language="verilog"):
        """Returns the HDL of this node

        Args:
            language (str): The language in which to generate the HDL

        Returns:
            str: The HDL of this node
            list: Set of HDL module definitions used in the node
        """
        if language not in ["verilog"]:
            raise ValueError("Unsupported hardware descriptive language")
        if language == "verilog":
            return self._verilog()
        if language == "vhdl":
            return self._vhdl()

    def _verilog(self):
        """Return Verilog consisting of the module's internal logic"""

        # If this node is part of an equivalence class,
        # but not the main representative,
        # destructively change the net names of its parent
        if self.equiv_class.rep is not self:
            parent = self.parent
            # But if this node is part of a bigger equivalent subtree
            # There is no need to even do assign statements
            # The equivalent subtree will take care of everything
            if parent.equiv_class.rep is not parent:
                return ""
            ret = ""
            index = parent.children.index(self)
            change_in_nets(
                parent, self.out_nets, self.equiv_class.out_nets, index
            )
            return ret

        ### Grab only instantiated cells from the HDL definiton

        # Iterate over each line in the HDL definition
        hdl_def = self.node_data["verilog"].splitlines()

        # Flag whether we're currently looking at a cell
        in_std_cell = False

        # Store the filtered HDL in a string
        ret = ""

        for line in hdl_def:
            if "assign" in line or "wire" in line:
                ret += line + "\n"
            else:
                if "U" in line:
                    in_std_cell = True
                if in_std_cell:
                    ret += line + "\n"
                if line != "" and line[-1] == ";":
                    in_std_cell = False

        # Create list of all instance pins and copy in unformatted net IDs
        pins = self.in_nets.copy()
        pins.update(self.equiv_class.out_nets)

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

        return ret


if __name__ == "__main__":
    raise RuntimeError("This module is not intended to be run directly")
