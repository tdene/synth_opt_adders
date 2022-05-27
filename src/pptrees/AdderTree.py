from .ExpressionNode import ExpressionNode as Node
from .ExpressionTree import ExpressionTree

class AdderTree(ExpressionTree):
    """Defines a tree that computes binary addition

    Attributes inherited from ExpressionTree:
        root (ExpressionNode): The root node of the tree
        width (int): The number of leaves in the tree
        radix (int): The radix of the tree
        idem (bool): Whether the tree's main operator is idempotent
        node_defs (dict): A dictionary that defines the tree's nodes
        in_shape (list of int): The shape of each leaf node's input
        out_shape (list of int): The shape of the root node's output
        black_shape (int, int): The shape of the main recurrence node's output

    Attributes inherited from ExpressionGraph:
        name (string): The name of the graph
        next_net (int): The next net name to be used
        next_block (int): The next block name to be used
        blocks (list): The list of blocks in the graph
        in_ports (list of ((string, int), string)): The list of input ports
        out_ports (list of ((string, int), string)): The list of output ports
    """	

    def __init__(self,
                 width=1,
                 in_ports=None,
                 out_ports=None,
                 name="adder",
                 start_point=0,
                 alias=None,
                 radix=2,
                 leaf_labels=["c","gp","p"]
                ):
        """Initializes the AdderTree

        Args:
            width (int): The number of leaves in the tree
            in_ports (list of ((string, int), string)): The list of input ports
            out_ports (list of ((string, int), string)): The list of output ports
            name (string): The name of the graph
            start_point (int): The starting Catalan ID of the tree
            alias (string): The name of a desired classic structure
            radix (int): The radix of the tree
        """

        # Initialize the node definitions
        node_defs = {
                "pre"           : "ppa_pre",
                "root"          : "ppa_post",
                "black"         : "ppa_black",
                "grey"          : "ppa_grey",
                "buffer"        : "ppa_buffer",
                "lspine_pre"    : "ppa_lspine_pre",
                "lspine"        : "ppa_lspine"
                }

        # Provide defaults for in_ports and out_ports
        if in_ports is None or out_ports is None:
            in_ports = [
                        (('a_in', width), 'a'),
                        (('b_in', width), 'b')
                       ]
            out_ports = [
                         (('sum', 1), 'sum')
                        ]

        # Initialize the expression tree
        super().__init__(width,
                         in_ports,
                         out_ports,
                         name = name,
                         start_point = start_point,
                         alias = alias,
                         radix = radix,
                         leaf_labels = leaf_labels,
                         idem = True,
                         node_defs = node_defs
                        )

    ### The methods below have to do with steroscopic composition ###

    def _ling_check(self, other, self_node = None, other_node = None):
        """Determine if this tree can be stereoscopically combined with another"""

        # Start at the root, if not specified
        if self_node is None and other_node is None:
            self_node = self.root
            other_node = other.root
        # If the leafs are reached, this recursive path has finished
        if not self_node.children or not other_node.children:
            return (True, [])
        # If other_node is a buffer, just skip it
        if other_node.value == self.node_defs["buffer"]:
            return self._ling_check(other, self_node, other_node[0])
        # Any leafs in other[0] are not present in self[1]
        if other_node[0].leafs & self_node[1].leafs:
            return (False, None)
        # Any leafs in other[1] but not self[1] must BE self[0] or self[0][1]
        # If the latter is the case, auto-add a buffer
        # unless we've already reached leafs or a buffer
        pushed_left = other_node[1].leafs & ~self_node[1].leafs
        next_selfc0 = self_node[0]
        buffers = []
        if pushed_left and self_node[0].leafs != pushed_left:
            if not self_node[0].children:
                return (False, None)
            elif self_node[0][1].leafs != pushed_left:
                return (False, None)
            next_selfc0 = self_node[0][0]
            if other_node[0].children and other_node[0].value != self.node_defs["buffer"]:
                buffers.append(other_node[0])
        # Recurse over the children
        # But be ready to insert buffers if needed
        ret0, buf0 = self._ling_check(other, next_selfc0, other_node[0])
        if not ret0:
            return (False, None)
        buffers.extend(buf0)
        ret1, buf1 = self._ling_check(other, self_node[1], other_node[1])
        if not ret1:
            return (False, None)
        buffers.extend(buf1)
        return (True, buffers)

    def stereo_check(self, others):
        """Check if a set of trees can be steroscopically combined

        This implements the ExpressionTree stub method.

        Args:
            others (list): list of trees to check
        """

        # If others is not a list, make it a list
        if not isinstance(others, list):
            others = [others]

        # First check that only two trees are being composed
        if len(others) != 1:
            return False
        # Check that they are all AdderTrees
        for other in others:
            if not isinstance(other, AdderTree):
                return False
        # Next, check that their attributes match
        if not self._check_attr(others,
                "width", "radix", "idem", "in_shape", "out_shape",
                "in_ports", "out_ports", "blocks"):
            return False
        # Check that no tree has blocks
        if any([x is not None for x in self.blocks]):
            return False

        # Finally, check their structure
        return self._ling_check(others[0])

    def _ling_combine(self, other, target, buffers, self_node = None, other_node = None):
        """Stereoscopically combine two trees"""

        # Start at the root, if not specified
        if self_node is None and other_node is None:
            self_node = self.root
            other_node = other.root
        # Assign shorthand names for the nodes
        p = self_node
        g = other_node

        # Overlapping roots
        ## If both nodes are root, create a root
        if not p.parent or not g.parent:
            if p.parent or g.parent:
                raise ValueError("Non-matching roots; impossible error message.")
            new_node = Node(node_defs["root"], x_pos = 0, y_pos = 0)
            target.root = new_node
            target.add_node(new_node)
            target._connect_outports(new_node)

        # Overlapping leafs
        ## If both nodes are leafs,

        self._ling_combine(other, target, self_node[0], other_node[0])
        self._ling_combine(other, target, self_node[1], other_node[1])

    def stereo_combine(self, others):
        """Stereoscopically combine a set of trees into a single tree

        This implements the ExpressionTree stub method.

        Args:
            others (list): list of trees to combine
        """

        # First check that the trees can be combined
        check, buffers = self.stereo_check(others)
        if not check:
            raise ValueError("Trees cannot be combined")

        # Next, combine the trees
        ret = AdderTree(
                width = self.width,
                in_ports = self.in_ports,
                out_ports = self.out_ports,
                name = self.name,
                no_shape = True,
                radix = self.radix,
                node_defs = node_defs
                )

        self._ling_combine(others[0], ret, buffers)

        # Return the combined tree
        return ret

if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
