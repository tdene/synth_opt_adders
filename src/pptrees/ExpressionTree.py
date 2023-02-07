import networkx as nx

from .ExpressionGraph import ExpressionGraph
from .ExpressionNode import ExpressionNode as Node
from .node_data import node_data
from .util import catalan, catalan_mirror_point, display_png, lg, match_nodes


class ExpressionTree(ExpressionGraph):
    """Defines a tree of binary expressions

    Attributes:
        root (ExpressionNode): The root node of the tree
        width (int): The number of leaves in the tree
        radix (int): The radix of the tree
        idem (bool): Whether the tree's main operator is idempotent
        node_defs (dict): A dictionary that defines the tree's nodes
        in_shape (list of int): The shape of each leaf node's input
        out_shape (list of int): The shape of the root node's output
        cocycle_shape (int, int): The shape of the main recurrence node's output

    Attributes inherited from ExpressionGraph:
        name (string): The name of the graph
        next_net (int): The next net name to be used
        next_block (int): The next block name to be used
        blocks (list): The list of blocks in the graph
        in_ports (list of ((string, int), string)): The list of input ports
        out_ports (list of ((string, int), string)): The list of output ports
    """

    # NOTE: This function fails flake8 C901
    # TO-DO: Make this function pass flake8 C901
    def __init__(
        self,
        width=1,
        in_ports=None,
        out_ports=None,
        name="tree",
        start_point=0,
        alias=None,
        no_shape=False,
        radix=2,
        idem=False,
        leaf_labels=["g", "gp", "p"],
        node_defs={},
    ):
        """Initializes the ExpressionTree

        Args:
            width (int): The number of leaves in the tree
            in_ports (list of ((string, int), string)): List of input ports
            out_ports (list of ((string, int), string)): List of output ports
            name (string): The name of the graph
            start_point (int): The starting Catalan ID of the tree
            alias (string): The name of a desired classic structure
            no_shape (bool): If this is True, the tree will not be initialized
            radix (int): The radix of the tree
            idem (bool): Whether the tree's main operator is idempotent
            leaf_label (string): The label of the leaf nodes
            node_defs (dict): A dictionary that must define these nodes:
                - "pre": Pre-processing node
                - "root": Root node
                - "cocycle": Main expression node used in the tree
                - "buffer": Buffer node

            Optional node definitions include but are not limited to:
                - "lspine": Nodes that lie along the left spine of the tree
                - "lspine_pre": Pre- node that feeds into the left spine
                - "small_root": Root node that corresponds to width = 1
                - "small_pre": Pre- node that corresponds to width = 1
        """
        if not isinstance(width, int):
            raise TypeError("Tree width must be an integer")
        if width < 1:
            raise ValueError("Tree width must be at least 1")
        if not isinstance(radix, int):
            raise TypeError("Tree radix must be an integer")
        if not isinstance(name, str):
            raise TypeError("Tree name must be a string")
        if not isinstance(idem, bool):
            raise TypeError("Tree idempotency must be a boolean")
        if not isinstance(node_defs, dict):
            raise TypeError("Tree node definitions must be a dictionary")
        for required in ["pre", "root", "cocycle", "buffer"]:
            if required not in node_defs:
                raise ValueError(
                    (
                        "Tree node definitions must contain" " the node {}"
                    ).format(required)
                )

        # Save constructor arguments
        self.width = width
        self.max_id = catalan(width - 1)
        self.radix = radix
        self.idem = idem
        self.node_defs = node_defs

        # Get node port shapes from the module definitions
        self.in_shape = [x[1] for x in node_data[node_defs["pre"]]["ins"]]
        self.out_shape = [x[1] for x in node_data[node_defs["root"]]["outs"]]

        cocycle = node_data[node_defs["cocycle"]]
        self.cocycle_shape = [x[1] for x in cocycle["ins"]]
        cocycle_out_shape = [x[1] for x in cocycle["outs"]]
        cocycle_out_shape = [self.radix * x for x in cocycle_out_shape]
        if cocycle_out_shape != self.cocycle_shape:
            raise ValueError(
                (
                    "The main recurrence node of the tree"
                    " must have the same input and output shape"
                )
            )
        del cocycle_out_shape

        # Check that node shapes are compatible with port shapes
        ### NOTE: INPUT SHAPE IS CURRENTLY ASSUMED TO BE [1,1,1,..]
        ### TO-DO: Allow for arbitrary input shape
        ### Need to check whole file for this implicit assumption
        for a in range(len(self.in_shape)):
            if a > len(in_ports) - 1 or in_ports[a][0][1] != self.width:
                raise ValueError(
                    (
                        "Input port {} of the tree must have the"
                        " compatible shape with input shape of the"
                        " pre-processing node"
                    ).format(a)
                )
        for a in range(len(self.out_shape)):
            if (
                a > len(out_ports) - 1
                or self.out_shape[a] != out_ports[a][0][1]
            ):
                raise ValueError(
                    (
                        "Output port {} of the tree must have the"
                        " same shape as the output shape of the"
                        " root node"
                    ).format(a)
                )

        # Initialize the graph
        super().__init__(name=name, in_ports=in_ports, out_ports=out_ports)

        # Initialize the tree

        ## If the tree should not be initialized, do not initialize it
        if no_shape:
            return

        ## Initialize the root node
        if self.width == 1 and "small_root" in node_defs:
            self.root = Node(node_defs["small_root"], x_pos=0, y_pos=0)
        else:
            self.root = Node(node_defs["root"], x_pos=0, y_pos=0)
        self.root = self.add_node(self.root)
        ### Connect the root node to the tree's ports
        self._connect_outports(self.root)

        ## Initialize the leafs
        leafs = []
        for a in range(self.width):
            # Left-most leaf may be special
            if width == 1 and "small_pre" in node_defs:
                stem = leaf_labels[2]
                node_def = node_defs["small_pre"]
            elif a == self.width - 1 and "lspine_pre" in node_defs:
                stem = leaf_labels[2]
                node_def = node_defs["lspine_pre"]
            else:
                stem = leaf_labels[1]
                node_def = node_defs["pre"]
            label = "{0}[{1}]".format(stem, a)
            leaf = Node(node_def)
            leaf = self.add_node(leaf, label=label)
            # Connect the leaf to the tree's ports
            self._connect_inports(leaf, a)
            leaf._recalculate_leafs(leafs=2**a)
            leafs.append(leaf)

        ## Initialize the rest of the tree
        if alias is None:
            if start_point < 0 or start_point > self.max_rank():
                raise ValueError("Tree start point out of bounds")
        elif alias not in [
            "serial",
            "ripple",
            "ripple-carry",
            "sklansky",
            "kogge-stone",
            "brent-kung",
        ]:
            error = "Structure alias {0} is not implemented.\n"
            error += "Consider using non-legacy start points.\n"
            error += "These correspond to the trees' Catalan IDs."
            error = error.format(alias)
            raise NotImplementedError(error)
        else:
            start_point = 0
        # If tree width is 1, hard-code the structure
        if self.width == 1:
            self.add_edge(self.root, leafs[0], 0)
            return
        # Unrank the tree based on the start_point
        self.unrank(None, 0, start_point, self.width - 1, leafs, lspine=True)

        # If an alias was given, implement it
        if alias in ["serial", "ripple", "ripple-carry"]:
            return
        elif alias == "sklansky":
            if self.width > 2:
                self.rbalance(self.root[1])
        elif alias == "kogge-stone":
            if self.width > 2:
                self.lbalance(self.root[1])
                self.equalize_depths(self.root[1])
        elif alias == "brent-kung":
            if self.width > 2:
                self.rbalance(self.root[1])
                while not self.root[1][0].is_proper():
                    self.right_rotate(self.root[1][0])

    def __len__(self):
        """Redefine the len() function to return the height of the tree"""
        return len(self.root) + 1

    def __getitem__(self, key):
        """Redefine the [] operator to readily access nodes

        This method must be called with two attributes, such as tree[a,b] with
        a >= b. It will then return the root of the subtree that spans the
        interval [a,b].

        This general representation works for all points in a tree.

        If the specified node does not exist, this method returns an IndexError.
        """
        # Don't overwrite the parent __getitem__
        # There is a chance that the parent __getitem__ is needed by NetworkX
        if isinstance(key, tuple) and len(key) == 2:

            if not isinstance(key[0], int) or not isinstance(key[1], int):
                raise TypeError("Node indices must be integers")
            if key[0] < key[1]:
                raise ValueError("First index must be greater than second")

            # Find the leafs corresponding to the requested node
            start = None
            target = None
            for leaf in self._get_leafs():
                # Find the leaf that corresponds to the first index
                if leaf.leafs == 2 ** key[0]:
                    start = leaf
                # Find the leaf that corresponds to the second index
                if leaf.leafs == 2 ** key[1]:
                    target = leaf
            if start is None or target is None:
                raise IndexError("Node indices are not valid")

            # Iterate up the tree until the target is met
            node = start
            while True:
                # Check whether we have gone too far
                if (node.leafs & (start.leafs << 1)) or (
                    node.leafs & (target.leafs >> 1)
                ):
                    raise IndexError("Requested node does not exist")
                # Check whether we have combined the two leafs
                if node.leafs & target.leafs:
                    return node
                # Move up the tree
                node = node.parent
        else:
            return super().__getitem__(key)

    def __gt__(self, other):
        """Define order by rank"""
        return self.rank(self.root) > other.rank(other.root)

    def __lt__(self, other):
        """Define order by rank"""
        return self.rank(self.root) < other.rank(other.root)

    def __copy__(self):
        """Define copying of Trees in terms of rank"""
        return self.__class__(width=self.width, start_point=self.rank())

    def copy(self):
        """Define copying of Trees in terms of rank"""
        return self.__class__(width=self.width, start_point=self.rank())

    def _repr_png_(self):
        """Automatically display diagrams in a Notebook"""
        return display_png(self)

    def max_rank(self):
        """Return the maximum rank of the tree"""
        return catalan(self.width - 1) - 1

    def _get_row(self, depth):
        """Return the nodes at a given depth"""
        nodes = [n for n in self.nodes if n.y_pos == depth]
        return sorted(nodes, key=lambda x: -x.x_pos)

    def _get_reversed_leafs(self, node):
        """Return a list of leaf nodes in the subtree rooted at node"""
        if node is None:
            return []
        if len(node.children) == 0:
            return [node]
        else:
            return [
                n for c in node.children for n in self._get_reversed_leafs(c)
            ]

    def _get_leafs(self, node=None):
        """Return a sorted list of leaf nodes in the subtree rooted at node"""
        if node is None:
            node = self.root
        return list(reversed(self._get_reversed_leafs(node)))

    def _connect_outports(self, root):
        """Connect the tree's output ports to the root node"""
        for a in range(len(self.out_shape)):
            port_name = self.out_ports[a][0][0]
            if self.out_shape[a] == 1:
                net_name = "${}".format(port_name)
                root.out_nets[port_name][0] = net_name
                continue
            for b in range(self.out_shape[a]):
                net_name = "${}[{}]".format(port_name, b)
                root.out_nets[port_name][b] = net_name

    def _connect_inports(self, node, index):
        """Connect the tree's input ports to a pre-processing node"""
        for a in range(len(self.in_shape)):
            port_name = self.in_ports[a][0][0]
            if self.width == 1:
                net_name = "${}".format(port_name)
            else:
                net_name = "${}[{}]".format(port_name, index)
            node.in_nets[port_name][0] = net_name

    def add_edge(self, parent, child, index):
        """Adds a directed edge to the tree, from child output to parent input
        All index ports on the parents's port list are connected to the child

        Args:
            parent (Node): The parent node
            child (Node): The child node
            index (int): The index of the parent's input port
        """
        if not isinstance(parent, Node):
            raise TypeError("Parent must be an Node")
        if not isinstance(child, Node):
            raise TypeError("Child must be an Node")
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if index < -self.radix or index > self.radix - 1:
            raise ValueError(
                (
                    "Tree nodes may not have more edges"
                    "than the radix of the tree"
                )
            )

        # Normalize index
        index = index % self.radix

        # Attempt to match the nodes' ports
        pin_pairs = match_nodes(parent, child, index)
        if pin_pairs is None:
            raise ValueError("Nodes do not have matching ports")

        for (p, c) in pin_pairs:
            # Connect the ports
            super().add_edge(parent, p, child, c)

        # Adjust x-pos and y-pos of the child
        ### NOTE: THIS IS HARD-CODED FOR RADIX OF 2
        ### TO-DO: Make this more general
        y_pos = parent.y_pos + 1
        x_diff = 1

        if index == 0:
            x_pos = parent.x_pos + x_diff
        elif index == 1:
            x_pos = parent.x_pos - x_diff

        child.x_pos = x_pos
        child.y_pos = y_pos

        diagram_pos = "{0},{1}!".format(x_pos * -1, y_pos * -1)
        self.nodes[child]["pos"] = diagram_pos

    def detach_subtree(self, node, return_data=True):
        """Detach the subtree rooted at node

        Args:
            node (Node): The root of the subtree to detach
            return_data (bool): Whether to return the data of the subtree

        Returns:
            rank (int): The rank of the subtree
            leafs (list): The leaf nodes of the subtree
        """
        if not isinstance(node, Node):
            raise TypeError("Node must be an Node")

        # Save the rank and leafs
        if return_data:
            rank = self.rank(node=node)
            leafs = self._get_leafs(node)
            labels = [self.nodes[n]["label"] for n in leafs]

        # Remove the subtree at node
        for c in node.children:
            self.detach_subtree(c, return_data=False)
        if node.parent is not None:
            self.remove_edge(node.parent, node)
        self.remove_node(node)

        # Return the data
        if return_data:
            return rank, leafs, labels

    def attach_subtree(self, parent, index, rank, leafs, labels, lspine=False):
        """Attach the subtree rooted at node

        Args:
            parent (Node): The parent node
            index (int): The index of the parent's input port
            rank (int): The rank of the subtree
            width (int): The width of the subtree
            leafs (list): The leaf nodes of the subtree
        """
        if not isinstance(parent, Node) and parent is not None:
            raise TypeError("Parent must be an Node")
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if not isinstance(rank, int):
            raise TypeError("rank must be an integer")
        if not isinstance(leafs, list):
            raise TypeError("leafs must be a list")
        if not all(isinstance(leaf, Node) for leaf in leafs):
            raise TypeError("leafs must be a list of Nodes")

        # Add the leafs to the tree
        for leaf, label in zip(leafs, labels):
            self.add_node(leaf, label=label)

        # Get the width of the subtree, based on the number of leafs
        width = len(leafs) - 1

        # Build the subtree
        return self.unrank(parent, index, rank, width, leafs, lspine=lspine)

    def mirror_subtree(self, node):
        """Mirror the subtree rooted at node"""
        if not isinstance(node, Node):
            raise TypeError("Node must be an Node")

        # Get the parent and index of the node
        parent = node.parent
        index = node.parent.children.index(node)

        # Detach the subtree
        rank, leafs, labels = self.detach_subtree(node)
        width = len(leafs) - 1

        # Mirror the rank
        high_bound = catalan_mirror_point(width) - 1
        low_bound = catalan(width) - high_bound - 1
        if rank > low_bound and rank < high_bound:
            raise ValueError("Cannot mirror tree with rank {0}".format(rank))
        rank = catalan(width) - rank - 1

        # Attach the mirrored subtree
        return self.attach_subtree(parent, index, rank, leafs, labels)

    def graft_branch_left(self, node):
        """Detach the subtree rooted at node, and graft it to the left

        Args:
            node (Node): The root of the subtree to detach

        Returns:
            rootstock (Node): The rootstock of the graft
        """
        if not isinstance(node, Node):
            raise TypeError("Node must be an Node")
        if self._on_lspine(node):
            raise ValueError("There is nothing to the left of this node")

        # Get the parent and index of the node
        parent = node.parent
        index = node.parent.children.index(node)

        # Find the rootstock
        stock_id = lg(node.leafs) + 1
        rootstock = self._get_leafs(self.root)[stock_id]
        r_parent = rootstock.parent
        r_index = r_parent.children.index(rootstock)

        # Detach the scion
        rank, leafs, labels = self.detach_subtree(node)

        # Check whether the scion will be attached onto the left spine
        lspine = r_index == 0 and self._on_lspine(r_parent)

        # Re-attach the rightmost leaf of the scion
        self.attach_subtree(parent, index, 0, [leafs.pop(0)], [labels.pop(0)])

        # Detach the leaf attached to the rootstock
        _, leaf, label = self.detach_subtree(rootstock)

        # Combine this leaf with the scion
        leafs += leaf
        labels += label

        # Graft the scion to the rootstock
        self.attach_subtree(r_parent, r_index, rank, leafs, labels, lspine)

        # Return the rootstock
        return rootstock

    def optimize_nodes(self):
        """Optimizes nodes in the tree by removing unnecessary logic

        This method is meant to be called after the structure of the tree
        has been finalized, and final HDL is desired.

        There is currently no guarantee that this method will allow for further
        modification of the tree structure. Instead, it may cause any and all
        methods that modify the tree, such as rotations and buffer insertions,
        to fail.

        This method should be extended by child classes to implement
        operation-specific optimizations.
        """

        # First fix node positions
        self._fix_diagram_positions()

    def swap_node_def(self, node, new_def):
        """Change a node's module definition

        Args:
            node (Node): The node to change
            new_def (str): The new module definition
        """

        # Disconnect the node from its parent
        parent = node.parent
        index = None
        if parent is not None:
            index = parent.children.index(node)
            self.remove_edge(parent, node)

        new_node, children = self._swap_node_def(node, parent, index, new_def)

        # Reconnect the node's children
        for index in range(len(children)):
            c = children[index]
            if c is not None:
                self.add_edge(new_node, c, index)
            else:
                new_node.children.append(None)

        return new_node

    def _swap_node_def(self, node, parent, index, new_def):
        """Change a node's module definition and disconnect children

        Args:
            node (Node): The node to change
            parent (Node): The parent of the node (already disconnected)
            index (int): The index of the parent's input port
            new_def (str): The new module definition
        """

        # Save the node's children
        children = node.children.copy()
        for c in node.children:
            if c is not None:
                self.remove_edge(node, c)

        # Remove the node from the tree
        if not node.children:
            label = self.nodes.data("label")[node]
            leafs = node.leafs
        self.remove_node(node)

        # Create the new node
        new_node = node.morph(new_def)

        # Add the new node to the tree
        if not node.children:
            self.add_node(new_node, **{"label": label})
            self._connect_inports(new_node, lg(leafs))
            new_node._recalculate_leafs(leafs=leafs)
        else:
            self.add_node(new_node)

        # Reconnect the node to its parent
        if parent is not None:
            self.add_edge(parent, new_node, index)
        else:
            self.root = new_node
            self._connect_outports(new_node)

        return new_node, children

    def _on_lspine(self, node):
        """Checks if a node is on the left spine of this tree"""
        if node not in self:
            raise ValueError("Node is not part of this tree")

        return node.leafs >= 2 ** (self.width - 1)

    def _on_rspine(self, node):
        """Checks if a node is on the right spine of this tree"""
        if node not in self:
            raise ValueError("Node is not part of this tree")

        return node.leafs & (node.leafs + 1) == 0

    ### NOTE: THIS IS HARD-CODED FOR RADIX OF 2
    ### TO-DO: Make this more general
    def left_rotate(self, node):
        """Rotate a node to the left

        Args:
            node (Node): The node to rotate
        """
        if not isinstance(node, Node):
            raise TypeError("node must be an Node")
        if node.parent is None or len(node.children) != self.radix:
            raise ValueError("Can only rotate nodes with full families")
        if node.parent[1] != node:
            raise ValueError("Can only rotate right children")

        # Get the parent and child nodes
        parent = node.parent
        grandparent = parent.parent
        lchild = node[0]
        rchild = node[1]
        plchild = node.parent[0]

        # Check for special cases
        thru_root = True
        if grandparent is not None:
            thru_root = False
            parent_dir = grandparent.children.index(parent)

        thru_lspine = False
        if "lspine" in self.node_defs and self._on_lspine(parent):
            thru_lspine = True

        # Adjust the y-pos
        parent.y_pos += 1
        plchild.iter_down(lambda x: setattr(x, "y_pos", x.y_pos + 1))
        node.iter_down(lambda x: setattr(x, "y_pos", x.y_pos - 1))
        lchild.iter_down(lambda x: setattr(x, "y_pos", x.y_pos + 1))

        # Disconnect the nodes
        if not thru_root:
            self.remove_edge(grandparent, parent)
        self.remove_edge(parent, node)
        self.remove_edge(node, lchild)
        if thru_lspine:
            self.remove_edge(parent, plchild)
            self.remove_edge(node, rchild)

        # If rotating through lspine, nodes must be morphed
        if thru_lspine:
            if thru_root:
                self.remove_node(parent)
                parent = parent.morph(self.node_defs["lspine"])
                self.add_node(parent)

            self.remove_node(node)
            if thru_root:
                node = node.morph(self.node_defs["root"])
            else:
                node = node.morph(self.node_defs["lspine"])
            self.add_node(node)
            if thru_root:
                self.root = node
                self._connect_outports(self.root)

        # Rotate the nodes
        if not thru_root:
            self.add_edge(grandparent, node, parent_dir)
        if thru_lspine:
            self.add_edge(parent, plchild, 0)
        self.add_edge(parent, lchild, 1)
        self.add_edge(node, parent, 0)
        if thru_lspine:
            self.add_edge(node, rchild, 1)

        self._fix_diagram_positions()
        return node

    ### NOTE: THIS IS HARD-CODED FOR RADIX OF 2
    ### TO-DO: Make this more general
    def right_rotate(self, node):
        """Rotate a node to the right

        Args:
            node (Node): The node to rotate
        """
        if not isinstance(node, Node):
            raise TypeError("node must be an Node")
        if node.parent is None or len(node.children) != self.radix:
            raise ValueError("Can only rotate nodes with full families")
        if node.parent[0] != node:
            raise ValueError("Can only rotate left children")

        # Get the parent and child nodes
        parent = node.parent
        grandparent = parent.parent
        rchild = node[1]
        lchild = node[0]
        prchild = node.parent[1]

        # Check for special cases
        thru_root = True
        if grandparent is not None:
            thru_root = False
            parent_dir = grandparent.children.index(parent)

        thru_lspine = False
        if "lspine" in self.node_defs and self._on_lspine(parent):
            thru_lspine = True

        # Adjust the y-pos
        parent.y_pos += 1
        prchild.iter_down(lambda x: setattr(x, "y_pos", x.y_pos + 1))
        node.iter_down(lambda x: setattr(x, "y_pos", x.y_pos - 1))
        rchild.iter_down(lambda x: setattr(x, "y_pos", x.y_pos + 1))

        # Disconnect the nodes
        if not thru_root:
            self.remove_edge(grandparent, parent)
        self.remove_edge(parent, node)
        self.remove_edge(node, rchild)
        if thru_lspine:
            self.remove_edge(parent, prchild)
            self.remove_edge(node, lchild)

        # If rotating through root, nodes must be morphed
        if thru_lspine:
            self.remove_node(parent)
            parent = parent.morph(self.node_defs["cocycle"])
            self.add_node(parent)

            if thru_root:
                self.remove_node(node)
                node = node.morph(self.node_defs["root"])
                self.add_node(node)
                self.root = node
                self._connect_outports(self.root)

        # Rotate the nodes
        if not thru_root:
            self.add_edge(grandparent, node, parent_dir)
        self.add_edge(parent, rchild, 0)
        if thru_lspine:
            self.add_edge(node, lchild, 0)
        self.add_edge(node, parent, 1)
        if thru_lspine:
            self.add_edge(parent, prchild, 1)

        self._fix_diagram_positions()
        return node

    ### NOTE: THIS IS HARD-CODED FOR RADIX OF 2
    ### TO-DO: Make this more general
    def left_shift(self, node):
        """Shifts a node left out of its local subtree"""
        # If the node sits on the left spine, it can no longer be shifted
        if self._on_lspine(node):
            return None

        # If the node can rotate left, simply do so
        try:
            return self.left_rotate(node)
        # NOTE: This error should only catch wrong-index issues
        # TO-DO: Perhaps make a custom, WrongChild, error?
        except ValueError:
            node = self.right_rotate(node)
            return self.left_shift(node)

    ### NOTE: THIS IS HARD-CODED FOR RADIX OF 2
    ### TO-DO: Make this more general
    def right_shift(self, node):
        """Shifts a node right out of its local subtree"""
        # If the node sits on the right spine, it can no longer be shifted
        if self._on_rspine(node):
            return None

        # If the node can rotate right, simply do so
        try:
            return self.right_rotate(node)
        # NOTE: This error should only catch wrong-index issues
        # TO-DO: Perhaps make a custom, WrongChild, error?
        except ValueError:
            node = self.left_rotate(node)
            return self.right_shift(node)

    def insert_buffer(self, node):
        """Insert a buffer as the parent of a node

        Args:
            node (Node): The child node
        """
        if not isinstance(node, Node):
            raise TypeError("child must be an Node")
        parent = node.parent
        if parent is None:
            raise ValueError("Cannot insert buffer above root")

        buffer = Node(self.node_defs["buffer"])

        # Disconnect the nodes
        index = parent.children.index(node)
        self.remove_edge(parent, node)

        # Insert the buffer
        self.add_node(buffer)
        self.add_edge(parent, buffer, index)
        self.add_edge(buffer, node, 0)

        # Fix the diagram positions
        buffer[0].y_pos -= 1
        buffer[0].iter_down(lambda x: setattr(x, "y_pos", x.y_pos + 1))

        return buffer

    def remove_buffer(self, buffer):
        """Remove a buffer between two nodes

        Args:
            buffer (Node): The buffer node
        """
        if not isinstance(buffer, Node):
            raise TypeError("buffer must be an Node")
        footprint = node_data[self.node_defs["buffer"]]["footprint"]
        this_footprint = node_data[buffer.value]["footprint"]
        if footprint != this_footprint:
            raise ValueError("buffer must be a buffer node")

        # Disconnect the nodes
        parent = buffer.parent
        child = buffer[0]
        index = parent.children.index(buffer)

        # Remove the buffer
        self.remove_edge(parent, buffer)
        self.remove_edge(buffer, child)
        self.remove_node(buffer)

        # Reconnect the nodes
        self.add_edge(parent, child, index)

        # Fix the diagram positions
        child.y_pos += 1
        child.iter_down(lambda x: setattr(x, "y_pos", x.y_pos - 1))

        return child

    def unrank(
        self, parent, index, rank, width, leafs, mirror=False, lspine=False
    ):
        """Generate a binary tree under a node by unranking it"""

        # The unranking function is symmetrical around the midpoint
        cn = catalan(width)
        mid = catalan_mirror_point(width)
        mirror_test = rank >= mid
        mirror = not mirror if mirror_test else mirror
        rank = cn - 1 - rank if mirror_test else rank

        # Check which kind of node to add
        node_defs = [None, None]
        if "lspine" in self.node_defs and lspine:
            node_defs[0] = self.node_defs["lspine"]
        else:
            node_defs[0] = self.node_defs["cocycle"]
        node_defs[1] = self.node_defs["cocycle"]

        # Initial recursion start case
        if parent is None:
            node = self.root
            # Special case for 1-bit tree
            if len(leafs) == 1:
                parent = node
        # Width reaching zero signals the bottom of the tree
        if width == 0:
            leaf = leafs.pop()
            self.add_edge(parent, leaf, index)
            return leaf
        # Normal operation; add new node
        if parent is not None:
            node = Node(node_defs[index])
            self.add_node(node)
            self.add_edge(parent, node, index)

        # Take advantage of Catalan properties
        i1, i2, ci1 = 0, 0, 0
        for i in range((width + 1) // 2):
            i1, i2 = i, width - i - 1
            ci1 = catalan(i1)
            big_number = ci1 * catalan(i2)
            rem = rank - big_number
            if rem < 0:
                break
            rank = rem

        # Recurse
        if mirror:
            self.unrank(node, 0, rank // ci1, i2, leafs, mirror, lspine)
            self.unrank(node, 1, rank % ci1, i1, leafs, mirror, False)
        else:
            self.unrank(node, 0, rank % ci1, i1, leafs, mirror, lspine)
            self.unrank(node, 1, rank // ci1, i2, leafs, mirror, False)

    def rank(self, node=None, mirror=False):
        """Classifies a binary tree under a node by ranking it"""

        # If node is not specified, start at the root
        if node is None:
            node = self.root

        # Special case for 1-bit tree
        if (node is self.root) and len(node.children) == 1:
            return 0
        # If the node is a leaf, its rank is zero
        if not len(node):
            return 0

        # Calculate info that this node needs
        lchild, rchild = node[0], node[1]
        lwidth = bin(lchild.leafs).count("1") - 1
        rwidth = bin(rchild.leafs).count("1") - 1

        # Calculate info that the children need
        width = lwidth + rwidth + 1
        new_mirror = lwidth >= rwidth if mirror else lwidth > rwidth

        # Account for mirroring
        if new_mirror:
            lchild, rchild = rchild, lchild
            lwidth, rwidth = rwidth, lwidth

        # Get information from the children
        lrank = self.rank(lchild, new_mirror)
        rrank = self.rank(rchild, new_mirror)

        # Calculate rank stub
        rank = lrank + rrank * catalan(lwidth)
        # Add rest of rank
        for i in range(lwidth):
            i1, i2 = i, width - i - 1
            big_number = catalan(i1) * catalan(i2)
            rank += big_number

        # Account for mirroring
        dir_switched = new_mirror != mirror
        rank = catalan(width) - rank - 1 if dir_switched else rank
        return rank

    def _fix_diagram_positions(self):
        """Fix the positions of the nodes in the diagram"""

        height = len(self)
        leafs = self._get_reversed_leafs(self.root)
        # Set x_pos of the leafs to consecutive numbers
        ctr = 0
        for leaf in leafs:
            leaf.x_pos = ctr
            ctr -= 1
        # Adjust other nodes' x_pos based on the leafs
        for d in range(height - 1, -1, -1):
            for node in self._get_row(d):
                if len(node.children) > 0:
                    children = [x for x in node.children if x is not None]
                    num_children = len(children)
                    sum_children = sum([x.x_pos for x in children])
                    avg = sum_children / num_children
                    node.x_pos = avg
                x_pos = node.x_pos
                y_pos = node.y_pos
                diagram_pos = "{0},{1}!".format(x_pos * -1, y_pos * -1)
                self.nodes[node]["pos"] = diagram_pos

    def _check_attr(self, others, *attr):
        """Check if a set of trees share a set of common attributes

        Args:
            others (list): list of trees to check
            attr (strings): The attributes to check

        Returns:
            bool: True if all attributes are the same, False otherwise
        """
        for a in attr:
            if not all([getattr(x, a) == getattr(self, a) for x in others]):
                return False
        return True

    def png(self, out="tree.png"):
        """Generate a PNG representation of the tree using GraphViz"""

        # Correct the positions of the nodes
        self._fix_diagram_positions()

        # Convert the graph to pydot
        pg = nx.drawing.nx_pydot.to_pydot(self)
        pg.set_splines("false")
        pg.set_concentrate("true")

        pg.write_png(out, prog="neato")

    ### NOTE: ALL METHODS BELOW ARE FOR LEGACY SUPPORT ONLY ###

    def reduce_height(self, node, target_height=None, original_node=None):
        """Attempts to reduce the height of the subtree rooted at this node

        Args:
            node (Node): The node generating the subtree
            target_height (int): The target height of the subtree
                If this is not specified, the height is reduced by 1
            original_node (Node, index): Information to refind subtree root
                This is used in recursion, and should not be specified
        """

        def reconstruct_node(parent, index):
            """Reconstruct the original node"""
            if parent is None:
                return self.root
            return parent[index]

        # If the node is a leaf, there is nothing to reduce
        if len(node) == 0:
            return None

        # Save the identity of the original node's parent
        if original_node is None:
            parent = node.parent
            index = None
            if parent is not None:
                index = parent.children.index(node)
            original_node = (parent, index)

        # Avoid repeated height calculations (to some degree)
        children = [c for c in node]
        c_heights = [len(c) for c in children]
        height = 1 + max(c_heights)

        # If the target height is not specified, reduce the height by 1
        if target_height is None:
            target_height = height - 1

        # If the target height is already reached, we are done
        if target_height >= height:
            return reconstruct_node(*original_node)

        # Check whether the height can be reduced
        if 1 << (target_height) < bin(node.leafs).count("1"):
            return None

        # Characterize each child as under_full or over_full
        max_leafs = 1 << (target_height - 1)
        under_full = [max_leafs > bin(c.leafs).count("1") for c in node]
        over_full = [max_leafs < bin(c.leafs).count("1") for c in node]

        # Reduce the height of bad children
        for a in range(len(c_heights)):
            c = children[a]
            # If child is a leaf, we are at the end of an iteration
            if len(c) == 0:
                continue
            # If child is a buffer, remove it
            if c.value == self.node_defs["buffer"]:
                self.remove_buffer(c)
                continue

            # If child is under the requisite height, continue
            if c_heights[a] <= target_height - 1:
                continue
            # If child is over_full and can shift a node left, do so
            elif a > 0 and over_full[a] and under_full[a - 1]:
                self.left_shift(c.leftmost_leaf().parent)
            # If child is over_full and can shift a node right, do so
            elif a < len(c_heights) - 1 and over_full[a] and under_full[a + 1]:
                self.right_shift(c.rightmost_leaf().parent)
            # Otherwise try to iterate down the child
            else:
                self.reduce_height(c, target_height - 1)

        # After iterating, the desired height may not be reached
        # If so, try again. We know it can be done.
        node = reconstruct_node(*original_node)
        return self.reduce_height(node, target_height, original_node)

    # NOTE: If this has not been sufficiently emphasized yet
    # This method is solely here for legacy support
    # It does something very specific, and arguably not generally useful
    # Use if you prefer comfort over efficiency
    def equalize_depths(self, node, desired_height=None):
        """Equalizes the leaf depths of the rooted at this node

        Args:
            node (Node): The node that roots the subtree
            desired_height (int): The desired height of the subtree
                If not specified, this is set to the maximum leaf depth
        """
        # Flag to support legacy diagrams
        no_left = True

        # If the node is a leaf, there is nothing to equalize
        height = len(node)
        if height == 0:
            return None

        # If desired_height is None, set it to the maximum depth
        if desired_height is None:
            desired_height = len(node)

        # If the current depth is less than the desired depth,
        # we can add buffers directly here
        if (not no_left) or node.parent[0] != node:
            for a in range(desired_height - height):
                self.insert_buffer(node)
                desired_height -= 1

        # Iterate over the children
        for c in node:
            # Avoid repeated height calculations (to some degree)
            height = len(c)
            # If the child is proper, we are at the end of an iteration
            # If child is leftmost, for legacy purposes, we cannot add buffers
            if c.is_proper():
                # Insert enough buffers to balance the depth
                if (not no_left) or node[0] != c:
                    for a in range(desired_height - height - 1):
                        self.insert_buffer(c)
                continue
            self.equalize_depths(c, desired_height - 1)

        return node

    def balance(self, node):
        """Balances the subtree rooted at this node

        Note that this does not create a complete tree.
        To do so, refer to the rbalance and lbalance methods.

        Args:
            node (Node): The node to balance
        """
        # If the node is a leaf, we are at the end of an iteration
        if len(node) == 0:
            return node

        # Reduce the height of the subtree until it cannot be further reduced
        old_node = node
        while True:
            node = self.reduce_height(node)
            if node is None:
                node = old_node
                break
            old_node = node
        del old_node

        # Balance each child, recursively
        for c in node:
            self.balance(c)

        return node

    def lbalance(self, node):
        """Balances the subtree rooted at this node to the left

        If the subtree contains buffers, this method will actively destroy them.

        Args:
            node (Node): The node to balance
            original_node (Node, index): Information to refind subtree root
                This is used in recursion, and should not be specified
        """

        def reconstruct_node(parent, index):
            """Reconstruct the original node"""
            if parent is None:
                return self.root
            return parent[index]

        # If the node is a leaf, there is nothing to balance
        if len(node) == 0:
            return None

        # Save the identity of the node's parent
        parent = node.parent
        index = None
        if parent is not None:
            index = parent.children.index(node)
        original_node = (parent, index)

        # First, reduce the subtree's height as much as possible
        node = self.balance(node)

        # If the subtree is proper, there is no difference between right/left
        if node.is_proper():
            return

        full_leafs = 1 << (len(node) - 1)
        lleafs = bin(node[0].leafs).count("1")
        rleafs = bin(node[1].leafs).count("1")

        # Check if the right child has too many leafs
        # If so, it needs to shift leafs to the left
        if lleafs < full_leafs and rleafs > 1:
            self.left_shift(node[1].leftmost_leaf().parent)
            node = reconstruct_node(*original_node)
            self.lbalance(node)
        # Otherwise recurse over the children
        else:
            self.balance(node[0])
            self.lbalance(node[0])
            self.lbalance(node[1])

    def rbalance(self, node):
        """Balances the subtree rooted at this node to the right

        If the subtree contains buffers, this method will actively destroy them.

        Args:
            node (Node): The node to balance
            original_node (Node, index): Information to refind subtree root
                This is used in recursion, and should not be specified
        """

        def reconstruct_node(parent, index):
            """Reconstruct the original node"""
            if parent is None:
                return self.root
            return parent[index]

        # If the node is a leaf, there is nothing to balance
        if len(node) == 0:
            return None

        # Save the identity of the node's parent
        parent = node.parent
        index = None
        if parent is not None:
            index = parent.children.index(node)
        original_node = (parent, index)

        # First, reduce the subtree's height as much as possible
        node = self.balance(node)

        # If the subtree is proper, there is no difference between right/left
        if node.is_proper():
            return

        full_leafs = 1 << (len(node) - 1)
        lleafs = bin(node[0].leafs).count("1")
        rleafs = bin(node[1].leafs).count("1")

        # Check if the left child has too many leafs
        # If so, it needs to shift leafs to the right
        if rleafs < full_leafs and lleafs > 1:
            self.right_shift(node[0].rightmost_leaf().parent)
            node = reconstruct_node(*original_node)
            self.rbalance(node)
        # Otherwise recurse over the children
        else:
            self.balance(node[0])
            self.rbalance(node[0])
            self.rbalance(node[1])

    def LF(self, x, y=None, find_y=False):
        """Performs an LF transform on the specified node, if possible

        This method is maintained solely for backwards compatibility.
        Using this method is morally hazardous. It masks the underlying truth.

        The node is specified using its (x,y) classic coordinate.
        Witholding the y-coordinate will perform the transform on the highest-y
        node that can be transformed.

        If the transform is not possible, the function returns None.
        Otherwise, the function returns the coordinates used to pivot.

        Args:
            x (int): The x-coordinate to use as a pivot for the LF transform
            y (int): The y-coordinate to use as a pivot for the LF transform
            find_y (bool): If True, the y-coordinate will be found automatically
        """
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if y is not None and not isinstance(y, int):
            raise TypeError("y must be an integer")

        # If no y-coordinate is specified, attempt the highest-y node
        # Except for the post-processing node. Arbitrarily.
        # Remember: using this method is morally hazardous.
        if y is None:
            return self.LF(x, len(self) - 2, find_y=True)

        # If the node is not in the tree, either iterate or return None
        if self[x, y] is None:
            if find_y and y > 1:
                return self.LF(x, y - 1, find_y=True)
            else:
                return None

        # Now that the node is known to be in the tree,
        # attempt to apply an LF transform
        node = self[x, y]
        new_node = self.reduce_height(node)
        if new_node is None and find_y:
            return self.LF(x, y - 1, find_y=True)
        return (x, y)

    def FL(self, x, y=None, find_y=False):
        """Performs an FL transform on the specified node, if possible

        This method is maintained solely for backwards compatibility.
        Using this method is morally hazardous. It masks the underlying truth.

        The node is specified using its (x,y) classic coordinate.
        Witholding the y-coordinate will perform the transform on the highest-y
        node that can be transformed.

        If the transform is not possible, the function returns None.
        Otherwise, the function returns the coordinates used to pivot.

        Args:
            x (int): The x-coordinate to use as a pivot for the LF transform
            y (int): The y-coordinate to use as a pivot for the LF transform
            find_y (bool): If True, the y-coordinate will be found automatically
        """
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if y is not None and not isinstance(y, int):
            raise TypeError("y must be an integer")

        # If no y-coordinate is specified, attempt the highest-y node
        # Except for the post-processing node. Arbitrarily.
        # Remember: using this method is morally hazardous.
        if y is None:
            return self.FL(x, len(self) - 2, find_y=True)

        # If the node is not in the tree, either iterate or return None
        if self[x, y] is None:
            if find_y and y > 1:
                return self.FL(x, y - 1, find_y=True)
            else:
                return None

        # Now that the node is known to be in the tree,
        # attempt to apply an FL transform
        node = self[x, y]
        self.insert_buffer(node)
        return (x, y)

    def FT(self, x, y=None, find_y=False):
        """Performs an FT transform on the specified node, if possible

        This method is maintained solely for backwards compatibility.
        Using this method is morally hazardous. It masks the underlying truth.

        The node is specified using its (x,y) classic coordinate.
        Witholding the y-coordinate will perform the transform on the highest-y
        node that can be transformed.

        If the transform is not possible, the function returns None.
        Otherwise, the function returns the coordinates used to pivot.

        Args:
            x (int): The x-coordinate to use as a pivot for the LF transform
            y (int): The y-coordinate to use as a pivot for the LF transform
            find_y (bool): If True, the y-coordinate will be found automatically
        """
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if y is not None and not isinstance(y, int):
            raise TypeError("y must be an integer")

        # If no y-coordinate is specified, attempt the highest-y node
        # Except for the post-processing node. Arbitrarily.
        # Remember: using this method is morally hazardous.
        if y is None:
            return self.FT(x, len(self) - 2, find_y=True)

        # If the node is not in the tree, either iterate or return None
        if self[x, y] is None:
            if find_y and y > 1:
                return self.FT(x, y - 1, find_y=True)
            else:
                return None

        # Now that the node is known to be in the tree,
        # attempt to apply an FT transform
        node = self[x, y]
        new_node = self.left_shift(node[1].leftmost_leaf().parent)
        if new_node is None and find_y:
            return self.FT(x, y - 1, find_y=True)
        return (x, y)

    def TF(self, x, y=None, find_y=False):
        """Performs a TF transform on the specified node, if possible

        This method is maintained solely for backwards compatibility.
        Using this method is morally hazardous. It masks the underlying truth.

        The node is specified using its (x,y) classic coordinate.
        Witholding the y-coordinate will perform the transform on the highest-y
        node that can be transformed.

        If the transform is not possible, the function returns None.
        Otherwise, the function returns the coordinates used to pivot.

        Args:
            x (int): The x-coordinate to use as a pivot for the LF transform
            y (int): The y-coordinate to use as a pivot for the LF transform
            find_y (bool): If True, the y-coordinate will be found automatically
        """
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        if y is not None and not isinstance(y, int):
            raise TypeError("y must be an integer")

        # If no y-coordinate is specified, attempt the highest-y node
        # Except for the post-processing node. Arbitrarily.
        # Remember: using this method is morally hazardous.
        if y is None:
            return self.TF(x, len(self) - 2, find_y=True)

        # If the node is not in the tree, either iterate or return None
        if self[x, y] is None:
            if find_y and y > 1:
                return self.TF(x, y - 1, find_y=True)
            else:
                return None

        # Now that the node is known to be in the tree,
        # attempt to apply an TF transform
        node = self[x, y]
        new_node = self.right_shift(node[0].rightmost_leaf().parent)
        if new_node is None and find_y:
            return self.TF(x, y - 1, find_y=True)
        return (x, y)

    ### NOTE: END LEGACY METHODS ###


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
