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
                 width,
                 in_ports=None,
                 out_ports=None,
                 name="adder",
                 start_point="serial",
                 radix=2
                ):
        """Initializes the AdderTree

        Args:
            width (int): The number of leaves in the tree
            in_ports (list of ((string, int), string)): The list of input ports
            out_ports (list of ((string, int), string)): The list of output ports
            name (string): The name of the graph
            start_point (string): The starting structure of the tree
            radix (int): The radix of the tree
        """

        # Initialize the node definitions
        node_defs = {
                "pre"           : "ppa_pre",
                "root"          : "ppa_post",
                "black"         : "ppa_black",
                "grey"          : "ppa_grey",
                "buffer"        : "ppa_buffer",
                "lspine_pre"    : "ppa_pre",
                "first_pre"     : "ppa_first_pre"
                }

        # Provide defaults for in_ports and out_ports
        if in_ports is None or out_ports is None:
            in_ports = [
                        (('a', width), 'a'),
                        (('b', width), 'b')
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
                         radix = radix,
                         node_defs = node_defs
                        )


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
