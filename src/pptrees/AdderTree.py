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
        cocycle_shape (int, int): The shape of the main recurrence node's output

    Attributes inherited from ExpressionGraph:
        name (string): The name of the graph
        next_net (int): The next net name to be used
        next_block (int): The next block name to be used
        blocks (list): The list of blocks in the graph
        in_ports (list of ((string, int), string)): The list of input ports
        out_ports (list of ((string, int), string)): The list of output ports
    """

    def __init__(
        self,
        width=1,
        in_ports=None,
        out_ports=None,
        name="adder",
        start_point=0,
        alias=None,
        radix=2,
        leaf_labels=["g", "gp", "p"],
    ):
        """Initializes the AdderTree

        Args:
            width (int): The number of leaves in the tree
            in_ports (list of ((string, int), string)): List of input ports
            out_ports (list of ((string, int), string)): List of output ports
            name (string): The name of the graph
            start_point (int): The starting Catalan ID of the tree
            alias (string): The name of a desired classic structure
            radix (int): The radix of the tree
        """

        # Initialize the node definitions
        node_defs = {
            "pre": "ppa_pre",
            "root": "ppa_post",
            "cocycle": "ppa_cocycle",
            "buffer": "ppa_buffer",
            "lspine_pre": "ppa_lspine_pre",
            "lspine": "ppa_lspine",
            "small_root": "ppa_small_root",
            "small_pre": "ppa_lspine_pre_simple",
        }

        # Provide defaults for in_ports and out_ports
        if in_ports is None or out_ports is None:
            in_ports = [(("a_in", width), "a"), (("b_in", width), "b")]
            out_ports = [(("sum", 1), "sum")]

        # Initialize the expression tree
        super().__init__(
            width,
            in_ports,
            out_ports,
            name=name,
            start_point=start_point,
            alias=alias,
            radix=radix,
            leaf_labels=leaf_labels,
            idem=True,
            node_defs=node_defs,
        )

    def optimize_nodes(self):
        """Optimizes nodes in the tree by removing unnecessary logic

        This method is meant to be called after the structure of the tree
        has been finalized, and final HDL is desired.

        There is currently no guarantee that this method will allow for further
        modification of the tree structure. Instead, it may cause any and all
        methods that modify the tree, such as rotations and buffer insertions,
        to fail.
        """

        # Call the superclass method
        super().optimize_nodes()

        # Perform specific optimizations

        ## Handle width < 2 case
        if self.width < self.radix:
            return

        ## Go down the right spine and optimize all nodes on it
        node = self.root
        while True:
            if node.value == self.node_defs["cocycle"]:
                node = self.swap_node_def(node, "ppa_rspine")
            if node.value == self.node_defs["buffer"]:
                node = self.swap_node_def(node, "ppa_rspine_buffer")
            if node.value == self.node_defs["pre"]:
                node = self.swap_node_def(node, "ppa_rspine_pre")
            if not node.children:
                break
            node = node[-1]

        ## If there is no lspine, swap out the root
        if (
            not self.root[0].children
            and self.root.value == self.node_defs["root"]
            and self.root[0].value == self.node_defs["lspine_pre"]
        ):
            child = self.root[0]
            other_child = self.root[1]
            self._swap_node_def(self.root, None, None, "ppa_post_nolspine")
            self._swap_node_def(child, self.root, 0, "ppa_lspine_pre_simple")
            self.add_edge(self.root, other_child, 1)

        ## If an lspine node has a leaf as right child, simplify it
        opt_list = []
        for node in self.nodes:
            if self._on_lspine(node) and node.children and node.parent:
                if not node[1].children:
                    opt_list.append(node)
        for node in opt_list:
            if node.value == self.node_defs["lspine"]:
                self.swap_node_def(node, "ppa_lspine_single")


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
