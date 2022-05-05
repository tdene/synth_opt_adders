from .ExpressionTree import ExpressionTree
from .ExpressionGraph import ExpressionGraph

class ExpressionForest(ExpressionGraph):
    """Defines a forest of binary expression trees

    Attributes:
        trees (list): A list of expression trees
        tree_type (class): The type of tree this forest contains
        width (int): The number of leaves in the forest
        radix (int): The radix of the tree
        idem (bool): Whether the trees' operators are idempotent
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
                 in_ports,
                 out_ports,
                 tree_type=ExpressionTree,
                 name="forest",
                 start_point="serial",
                 radix=2,
                 idem=False,
                 node_defs={}
                ):
        """Initializes the ExpressionForest

        Args:
            width (int): The number of leaves in the forest
            in_ports (list of ((string, int), string)): List of input ports
            out_ports (list of ((string, int), string)): List of output ports
            tree_type (class): The type of tree to use
            name (string): The name of the graph
            start_point (string): The starting structure of the tree
            radix (int): The radix of the tree
            idem (bool): Whether the tree's main operator is idempotent
            node_defs (dict): A dictionary that must define these nodes:
                - "pre": Pre-processing node
                - "root": Root node
                - "black": Main expression node used in the tree
                - "buffer": Buffer node

            Optional node definitions include but are not limited to:
                - "grey": Black node that feeds into the root node
                - "lspine": Nodes that lie along the left spine of the tree
                - "lspine_pre": Pre- node that feeds into the left spine
                - "first_pre": Right-most pre-processing node
        """
        if not isinstance(width, int):
            raise TypeError("Forest width must be an integer")
        if width < 1:
            raise ValueError("Forest width must be at least 1")
        if start_point not in ["serial", "rbalanced", "balanced"]:
            error = "Tree start point {0} is not implemented"
            error = error.format(start_point)
            raise NotImplementedError(error)
        if not isinstance(radix, int):
            raise TypeError("Tree radix must be an integer")
        if not isinstance(name, str):
            raise TypeError("Tree name must be a string")
        if not isinstance(idem, bool):
            raise TypeError("Tree idempotency must be a boolean")
        if not isinstance(node_defs, dict):
            raise TypeError("Tree node definitions must be a dictionary")
        for required in ["pre", "root", "black", "buffer"]:
            if required not in node_defs:
                raise ValueError(("Tree node definitions must contain"
                                  " the node {}").format(required))

        # Save constructor arguments
        self.width = width
        self.tree_type = tree_type
        self.radix = radix
        self.idem = idem
        self.node_defs = node_defs

        # Initialize the graph
        super().__init__(name=name,in_ports=in_ports,out_ports=out_ports)

        # Initialize the trees
        self.trees = []
        ### NOTE: TREE OUTPUT SHAPE IS CURRENTLY ASSUMED TO BE [1,1,1,..]
        ### TO-DO: Allow for arbitrary input shape
        ### Need to check whole file for this implicit assumption
        tree_out_ports = [((x[0][0],1),x[1]) for x in out_ports]

        for a in range(1,width+1):
            ### NOTE: INPUT SHAPE IS CURRENTLY ASSUMED TO BE [1,1,1,..]
            ### TO-DO: Allow for arbitrary input shape
            ### Need to check whole file for this implicit assumption
            tree_in_ports = [((x[0][0],a),x[1]) for x in in_ports]

            t = self.tree_type(
                    a,
                    tree_in_ports,
                    tree_out_ports,
                    name="tree_{}".format(a),
                    start_point=start_point,
                    radix=radix,
            )
            self.trees.append(t)


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
