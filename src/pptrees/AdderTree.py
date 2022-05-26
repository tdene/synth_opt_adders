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

    def ling_check(self, other, self_node = None, other_node = None):
        """Determine if this tree is strictly left of another

        This is used to determine whether two trees can be stereoscopically combined.
        """
        # Start at the root, if not specified
        if self_node is None and other_node is None:
            self_node = self.root
            other_node = other.root
        # If the leafs are reached, this recursive path has finished
        if not self_node.children or not other_node.children:
            return True
        # Store children of the current nodes
        self_c = self_node.children
        other_c = other_node.children
        # Any leafs in other[0] are not present in self[1]
        if other_c[0].leafs & self_c[1].leafs:
            return False
        # Any leafs in other[1] but not self[1] must be in self[0]
        if self_c[0].leafs - (other_c[1].leafs - self_c[1].leafs) < 0:
            return False
        # Recurse over the children
        return self.ling_check(other, self_c[0], other_c[0]) and \
                self.ling_check(other, self_c[1], other_c[1])

    def stereo_check(self, others):
        """Check if a set of trees can be steroscopically combined

        This implements the ExpressionTree stub method.

        Args:
            others (list): list of trees to check
        """

        # First check that only two trees are being composed
        if len(others) != 1:
            return False
        # Check that they are all AdderTrees
        for other in others:
            if not isinstance(other, AdderTree):
                return False
        # Next, check that their attributes match
        if not self._check_attr(self, other,
                "width", "radix", "idem", "in_shape", "out_shape",
                "in_ports", "out_ports", "blocks"):
            return False
        # Check that no tree has blocks
        if self.blocks:
            return False

        # Finally, check their structure
        return self.ling_check(others[0])


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
