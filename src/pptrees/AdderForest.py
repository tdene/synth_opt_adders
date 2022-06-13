from .AdderTree import AdderTree
from .ExpressionForest import ExpressionForest


class AdderForest(ExpressionForest):
    """Defines a tree that computes binary addition

    Attributes inherited from ExpressionForest:
        trees (list): A list of expression trees
        tree_type (class): The type of tree this forest contains
        width (int): The number of leaves in the forest
        radix (int): The radix of the tree
        idem (bool): Whether the trees' operators are idempotent
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
        width,
        in_ports=None,
        out_ports=None,
        tree_type=AdderTree,
        name="adder",
        alias=None,
        tree_start_points=None,
        initialized_trees=None,
        radix=2,
    ):
        """Initializes the AdderForest

        There are three arguments that can be used to intialize the forest.
        This is their priority order, from highest to lowest:
            - initialized_trees
            - tree_start_points
            - alias

        Args:
            width (int): The number of leaves in the tree
            in_ports (list of ((string, int), string)): List of input ports
            out_ports (list of ((string, int), string)): List of output ports
            tree_type (class): The type of tree this forest contains
            name (string): The name of the graph
            alias (string): The starting structure of the forest [LEGACY]
            tree_start_points (list of int): Catalan IDs for each tree
            initialized_trees (list): List of trees to initialize the forest
                If this parameter is set,
                the forest will undergo an alternate constructor
            radix (int): The radix of the tree
        """

        # Initialize the node definitions
        node_defs = {
            "pre": "ppa_pre",
            "root": "ppa_post",
            "cocycle": "ppa_cocycle",
            "rspine": "ppa_rspine",
            "buffer": "ppa_buffer",
            "lspine_pre": "ppa_lspine_pre",
            "lspine": "ppa_lspine",
        }

        # Provide defaults for in_ports and out_ports
        if in_ports is None or out_ports is None:
            in_ports = [(("a_in", width), "a_in"), (("b_in", width), "b_in")]
            out_ports = [(("sum", width), "sum")]

        # Initialize the expression tree
        super().__init__(
            width,
            in_ports,
            out_ports,
            tree_type=tree_type,
            name=name,
            alias=alias,
            tree_start_points=tree_start_points,
            initialized_trees=initialized_trees,
            radix=radix,
            node_defs=node_defs,
        )


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
