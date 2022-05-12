import re

from .ExpressionTree import ExpressionTree
from .ExpressionGraph import ExpressionGraph
from .modules import *

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

        # Initialize the trees
        self.trees = []

        for a in range(1,width+1):
            ### NOTE: INPUT SHAPE IS CURRENTLY ASSUMED TO BE [1,1,1,..]
            ### TO-DO: Allow for arbitrary input shape
            ### Need to check whole file for this implicit assumption
            if a == 1:
                bit_s = "[{0}]".format(a-1)
            else:
                bit_s = "[{0}:0]".format(a-1)
            tree_in_ports = [((x[0][0],a),x[1]+bit_s) for x in in_ports]

            ### NOTE: TREE OUTPUT SHAPE IS CURRENTLY ASSUMED TO BE [1,1,1,..]
            ### TO-DO: Allow for arbitrary input shape
            ### Need to check whole file for this implicit assumption
            bit_s = "[{0}]".format(a-1)
            tree_out_ports = [((x[0][0],1),x[1]+bit_s) for x in out_ports]

            t = self.tree_type(
                    a,
                    tree_in_ports,
                    tree_out_ports,
                    name="tree_{}".format(a),
                    start_point=start_point,
                    radix=radix,
            )
            self.trees.append(t)

        # Initialize the graph
        super().__init__(name=name,in_ports=in_ports,out_ports=out_ports)

    def find_equivalent_nodes(self):
        """Finds identical nodes amongst the forest's trees"""
        for i1 in reversed(range(len(self.trees))):
            t1 = self.trees[i1]
            for i2 in range(i1):
                t2 = self.trees[i2]
                for n1 in t1.nodes:
                    for n2 in t2.nodes:
                        if n1.equiv(n2):
                            n2.virtual = n1.out_nets
                            self.increase_fanout(t1,n1)

    def increase_fanout(self,tree,node):
        """Increases the fanout of a node in a tree"""

        e_data = tree.get_edge_data(node.parent,node)
        index = node.parent.children.index(node)
        g = modules[node.value]["le"][index]
        e_data["weight"] += g 

    def hdl(
        self,
        out=None,
        mapping="behavioral",
        language="verilog",
        flat=False,
        full_flat=False,
        module_name=None,
        description_string="start of unnamed graph"
    ):
        """Creates a HDL description of the forest

        Args:
            language (str): The language in which to generate the HDL
            flat (bool): If True, flatten the graph's HDL
            full_flat (bool): If True, flatten all modules in the graph's HDL
            module_name (str): The name of the module to generate
            description_string (str): String commend to prepend to the HDL

        Returns:
            str: HDL module definition representing the graph
            list: Set of HDL module definitions used in the graph

        """
        # If module name is not defined, set it to graph's name
        if module_name is None:
            module_name = self.name

        hdl = []
        module_defs = set()
        # This HDL description will have multiple cell-internal wires
        # By default, these are named w*
        # These names need to be made unique
        w_ctr = 0
        for t in reversed(self.trees):
            desc = "{}_forest {}".format(self.name, t.name)
            t_hdl, t_module_defs = t.hdl(
                            language=language,
                            flat=flat,
                            full_flat=full_flat,
                            description_string=desc)
            w = re.findall(r"w\d+", t_hdl)
            for x in set(w):
                t_hdl = t_hdl.replace(x, "w{}".format(w_ctr))
                w_ctr += 1
            hdl.append(t_hdl)
            module_defs |= t_module_defs
        hdl = "\n".join(hdl)

        # This HDL description will have multiple instances in it
        # By default, util.hdl_inst names all instances "U0"
        # These names need to be made unique
        U_count = 0
        good_hdl = ""
        while True:
            # Find the next instance name
            U = re.search(r"U\d+", hdl)
            if U is None:
                break
            # Replace it with the next name
            good_hdl += hdl[:U.start()] + "U" + str(U_count)
            hdl = hdl[U.end():]
            U_count += 1
        hdl = good_hdl + hdl

        hdl, module_defs, file_out_hdl = self._wrap_hdl(hdl, module_defs,
                language, module_name)
        if out is not None:
            self._write_hdl(file_out_hdl, out, language, mapping)

if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
