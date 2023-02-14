from .ExpressionGraph import ExpressionGraph
from .ExpressionTree import ExpressionTree
from .util import (
    display_gif,
    hdl_syntax,
    increment_iname,
    increment_wname,
    natural_keys,
    wrap_quotes,
)


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
        cocycle_shape (int, int): The shape of the main recurrence node's output
        equiv_classes (list of EquivClass): The equivalence classes of the graph

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
        width,
        in_ports,
        out_ports,
        tree_type=ExpressionTree,
        name="forest",
        alias=None,
        tree_start_points=None,
        initialized_trees=None,
        radix=2,
        idem=False,
        node_defs={},
    ):
        """Initializes the ExpressionForest

        There are three arguments that can be used to intialize the forest.
        This is their priority order, from highest to lowest:
            - initialized_trees
            - tree_start_points
            - alias

        Args:
            width (int): The number of leaves in the forest
            in_ports (list of ((string, int), string)): List of input ports
            out_ports (list of ((string, int), string)): List of output ports
            tree_type (class): The type of tree to use
            name (string): The name of the graph
            alias (string): The starting structure of the forest [LEGACY]
            tree_start_points (list of int): Catalan IDs for each tree
            initialized_trees (list): A list of trees to initialize the forest
                If this parameter is set,
                the forest will undergo an alternate constructor
            radix (int): The radix of the tree
            idem (bool): Whether the tree's main operator is idempotent
            node_defs (dict): A dictionary that must define these nodes:
                - "pre": Pre-processing node
                - "root": Root node
                - "cocycle": Main expression node used in the tree
                - "buffer": Buffer node

            Optional node definitions include but are not limited to:
                - "rspine": Nodes that lie along the right spine of the tree
                - "lspine": Nodes that lie along the left spine of the tree
                - "lspine_pre": Pre- node that feeds into the left spine
                - "first_pre": Right-most pre-processing node
        """
        if not isinstance(width, int):
            raise TypeError("Forest width must be an integer")
        if width < 1:
            raise ValueError("Forest width must be at least 1")
        if alias not in [
            None,
            "serial",
            "ripple",
            "ripple-carry",
            "sklansky",
            "kogge-stone",
            "brent-kung",
        ]:
            error = "Forest start point {0} is not implemented.\n"
            error += "Consider using non-legacy start points.\n"
            error += "These correspond to the trees' Catalan IDs."
            error = error.format(alias)
            raise NotImplementedError(error)
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

        # If both kinds of start points are specified,
        # Use the non-legacy kind
        if alias is not None and tree_start_points is not None:
            alias = None

        # Save constructor arguments
        self.width = width
        self.tree_type = tree_type
        self.radix = radix
        self.idem = idem
        self.node_defs = node_defs

        # If initialized trees are provided, simply use them
        if isinstance(initialized_trees, list):
            if len(initialized_trees) != width:
                raise ValueError("Number of trees in a forest must equal width")
            self.trees = initialized_trees
            super().__init__(name=name, in_ports=in_ports, out_ports=out_ports)
            self.equiv_classes = set()
            return

        # Otherwise, initialize the trees
        self.trees = []

        for a in range(1, width + 1):
            ### NOTE: INPUT SHAPE IS CURRENTLY ASSUMED TO BE [1,1,1,..]
            ### TO-DO: Allow for arbitrary input shape
            ### Need to check whole file for this implicit assumption
            if a == 1:
                bit_s = "[{0}]".format(a - 1)
            else:
                bit_s = "[{0}:0]".format(a - 1)
            tree_in_ports = [((x[0][0], a), x[1] + bit_s) for x in in_ports]

            ### NOTE: TREE OUTPUT SHAPE IS CURRENTLY ASSUMED TO BE [1,1,1,..]
            ### TO-DO: Allow for arbitrary input shape
            ### Need to check whole file for this implicit assumption
            bit_s = "[{0}]".format(a - 1)
            tree_out_ports = [((x[0][0], 1), x[1] + bit_s) for x in out_ports]

            if tree_start_points is not None and len(tree_start_points) > a - 1:
                catalan_id = tree_start_points[a - 1]
            else:
                catalan_id = 0

            t = self.tree_type(
                width=a,
                in_ports=tree_in_ports,
                out_ports=tree_out_ports,
                name="tree_{}".format(a - 1),
                radix=radix,
                start_point=catalan_id,
            )
            self.trees.append(t)

        # Initialize the graph
        super().__init__(name=name, in_ports=in_ports, out_ports=out_ports)
        self.equiv_classes = set()

        # If tree_start_points was provided, ignore the alias
        if tree_start_points is not None:
            return

        # Transform the forest towards the starting point
        if alias in ["serial", "ripple", "ripple-carry"]:
            pass
        elif alias == "sklansky":
            for t in self.trees[2:]:
                t.rbalance(t.root[1])
        elif alias == "kogge-stone":
            for t in self.trees[2:]:
                t.lbalance(t.root[1])
                t.equalize_depths(t.root[1])
        elif alias == "brent-kung":
            for t in self.trees[2:]:
                t.rbalance(t.root[1])
                while not t.root[1][0].is_proper():
                    t.right_rotate(t.root[1][0])

    def __getitem__(self, key):
        """Returns the tree at the given index

        Args:
            key (int): The index of the tree to return

        Returns:
            ExpressionTree: The tree at the given index
        """
        return self.trees[key]

    def __iter__(self):
        """Iterates over the trees in the forest"""
        return iter(self.trees)

    def _repr_png_(self):
        """Automatically display diagrams in a Notebook"""
        return display_gif(self.trees)

    ### NOTE: Equivalence requires nodes to be fully equivalent
    ### It is possible for two nodes to be partially equivalent
    ### For example, if their subtrees are identical
    ### But one node's expression is a subset of the other
    ### Such as (+,-) vs (+) or (-)
    ### This should be accounted for
    def find_equivalent_nodes(self):
        """Finds equivalent nodes amongst the forest's trees"""
        for i1 in reversed(range(len(self.trees))):
            t1 = self.trees[i1]
            for n1 in t1.nodes:
                self.equiv_classes.add(n1.equiv_class)
            for i2 in range(i1):
                t2 = self.trees[i2]
                for n1 in t1.nodes:
                    for n2 in t2.nodes:
                        # Try to merge equivalence classes
                        old_ec = n2.equiv_class
                        new_ec = n1.equiv_class
                        if old_ec.equiv(new_ec):
                            new_ec.merge(old_ec, check_equiv=False)
                            if old_ec in self.equiv_classes:
                                self.equiv_classes.remove(old_ec)
                            self.equiv_classes.add(new_ec)
        for ec in self.equiv_classes:
            ec._recalculate_parents()
        self.mark_equivalent_nodes()

    def mark_equivalent_nodes(self):
        """Mark all redundant nodes with stripes on diagrams"""
        for t in self.trees:
            for n in t.nodes:
                if n.equiv_class.rep is not n:
                    if t.nodes(data=True)[n].get("gradientangle", "0") == "135":
                        continue
                    col = t.nodes(data=True)[n]["fillcolor"]
                    t.nodes(data=True)[n]["orig_color"] = col
                    new_col = wrap_quotes("red;0.5:{0};0.5".format(col))
                    t.nodes(data=True)[n]["fillcolor"] = new_col
                    t.nodes(data=True)[n]["gradientangle"] = "135"

    def reset_equivalent_nodes(self):
        """Resets the equivalence classes of all nodes"""
        self.unmark_equivalent_nodes()
        for ec in self.equiv_classes:
            ec.reset()

    def unmark_equivalent_nodes(self):
        """Remove stripes from all redundant nodes on diagrams"""
        for t in self.trees:
            for n in t.nodes:
                if t.nodes(data=True)[n].get("gradientangle", "0") == "135":
                    col = t.nodes(data=True)[n]["fillcolor"]
                    old_col = t.nodes(data=True)[n].get("orig_color", col)
                    t.nodes(data=True)[n]["fillcolor"] = old_col
                    t.nodes(data=True)[n]["gradientangle"] = "0"

    ### NOTE: Improve fanout estimate
    def _calc_node_fanout(self, node):
        """Estimates the delay caused by fanout for a node

        A node has fanout of k if:
         - node is the representative of an equivalence class
         - There are k nodes in the forest such that
             - They belong to node's equivalence class
             - Their parents belong to unique equivalence classes

        For example, if an equivalence class contains the nodes
        n1, n2, n3, n4; with n1 being the representative
        And there is an equivalence relation between n1.parent and n2.parent
        but not between any other parents

        n1 has a fan-out of 3
        The other nodes do not matter
        """
        tree = node.graph
        # Grab the node's equivalence class
        ec = node.equiv_class
        # If node is not ec's representative, do nothing
        if ec.rep is not node:
            return
        # If node is root, do noting
        if node.parent is None:
            return

        # Count the fanout
        fanout = len(ec.parents)

        # Modify the relevant edge's data
        e_data = tree.get_edge_data(node.parent, node)
        index = node.parent.children.index(node)
        g = node.node_data["le"][index]
        ### This is a bad estimate of fanout's effect on delay
        e_data["fanout"] = g * fanout
        tree.update_edge_weight(node.parent, node)

        return fanout

    def calculate_fanout(self):
        """Calculates the fanout of all nodes in the forest

        See the description of _calc_node_fanout for details
        """
        for t in self.trees:
            for n in t:
                self._calc_node_fanout(n)

    def decouple_fanout(self, node, tree):
        """Decouples the fanout of the specified node in the specified tree"""

        # Check if arguments are valid
        if not (node in node.graph):
            raise ValueError("Node is not in its graph. Impossible error.")
        if not (node.graph in self.trees):
            raise ValueError(
                "Node graph is not in this forest. Impossible error."
            )
        if not (tree in self.trees):
            raise ValueError("Trying to decouple fanout in an invalid tree.")

        # Look inside the node's equivalence class for an other_node from tree
        other_node = None
        ec = node.equiv_class
        for a in ec:
            if a.graph is tree:
                other_node = a
                break
        if other_node is None:
            raise ValueError("Trying to decouple fanout in innapropriate tree.")

        # Decouple fanout
        buffer = tree.insert_buffer(other_node)

        # Fix equivalence classes
        for p in ec.parents:
            # Try to add new buffer to other equivalence classes
            try:
                p.merge(buffer.equiv_class)
            except ValueError:
                pass
        ec.parents.add(buffer)

        # Fix fanout
        for a in ec:
            self._calc_node_fanout(a)
        for a in buffer.equiv_class:
            self._calc_node_fanout(a)

    def optimize_nodes(self):
        """Greedily attempt to swap in nodes with same footprint

        All node node_data have a footprint attribute clarifying which node_data
        refer to the same node concept. All node node_data also have a priority
        attribute, used to determine which module is most "optimal".

        This method attempts to raise the total optimality of the forest by
        swapping in higher-priority node_data.

        This can probably be safely executed at any point in time, but it is
        advisable to only execute this once no more rotations will take place.

        Args:
            node (Node): The root node of the sub-tree to optimize
        """
        for t in self.trees:
            t.optimize_nodes()

    def add_best_blocks(self, graph_type=None):
        """Calls upon the Trees' add_best_blocks methods"""
        for t in self.trees:
            t.add_best_blocks(graph_type=graph_type)

    def _prepare_for_hdl(
        self,
        mapping="behavioral",
        language="verilog",
        uniquify_names=True,
        optimization=1,
    ):
        """Prepares the graph for HDL generation

        Note that this process may destructively render the graph unusable

        Args:
            mapping (str): The cell mapping to use for the HDL generation
            language (str): The language in which to generate the HDL
            description_string (str): String commend to prepend to the HDL
            uniquify_names (str): Whether wire/instance must be uniquified
        """
        # Check if graph has already been prepared
        if self._prepared:
            return

        # Optimize HDL of nodes in the forest of trees
        if optimization > 0:
            self.optimize_nodes()
        self.find_equivalent_nodes()
        if optimization > 1:
            self.calculate_fanout()
            self.add_best_blocks()

        # Uniquify wire/instance names, if requested
        if uniquify_names:
            reps = [ec.rep for ec in self.equiv_classes]
            increment_iname(reps, 1, language)
            increment_wname(reps, 1, language)

        # Toggle the prepared flag
        self._prepared = True

    def hdl(
        self,
        out=None,
        optimization=1,
        mapping="behavioral",
        language="verilog",
        flat=False,
        module_name=None,
        uniquify_names=True,
        description_string="start of unnamed graph",
        hdl_comments=True,
        inst_id="U0",
    ):
        """Creates a HDL description of the forest

        Args:
            out (str): The file to write the HDL to
            optimization (int): The optimizaton level to use
                optimization = 0: No optimization
                optimization = 1: Remove some redundant logic out of nodes
                optimization = 2: Perform previous optimization, then partition
                the HDL into smaller blocks which synthesis tools can handle
                better.
            mapping (str): The technology mapping to use
            language (str): The language in which to generate the HDL
            flat (bool): If True, flatten the graph's HDL
            module_name (str): The name of the module to generate
            uniquify_names (str): Whether wire/instance must be uniquified
            description_string (str): String commend to prepend to the HDL
            hdl_comments (bool): Whether to include comments in the HDL
            inst_id (str): The name of an instance of this graph HDL

        Returns:
            str: HDL module definition representing the graph
            list: Set of HDL module definitions used in the graph

        """
        self._prepare_for_hdl(
            mapping=mapping,
            language=language,
            uniquify_names=uniquify_names,
            optimization=optimization,
        )

        # Update module name, if provided
        if module_name is None:
            module_name = self.name

        # Set language-specific syntax
        syntax = hdl_syntax[language]

        # Create the HDL
        hdl = []
        module_defs = set()

        # Get set of the forest's port names
        inp, outp = self._get_ports()
        self_port_names = set([x[0][0] for x in inp + outp])
        # Keep track of inter-tree wire connections
        wires = set()
        # Get HDL for each tree
        tree_ctr = 0
        for t in reversed(self.trees):
            # Get the graph's HDL
            desc = "{}_forest {}".format(self.name, t.name)
            t_hdl, t_module_defs, _ = t.hdl(
                language=language,
                mapping=mapping,
                flat=flat,
                module_name="{0}_{1}".format(module_name, t.name),
                uniquify_names=False,
                description_string=desc,
                hdl_comments=hdl_comments,
                inst_id="U{0}".format(tree_ctr),
            )
            # Track all inter-tree wires connections
            # as long as they are not already ports of the forest
            inp, outp = t._get_ports()
            tree_ports = inp + outp
            wires |= set(
                [x[0][0] for x in tree_ports if x[0][0] not in self_port_names]
            )

            # Add the tree's HDL to the forest's HDL
            hdl.append(t_hdl)
            module_defs |= t_module_defs
            tree_ctr += 1

        # Instantiate all wires that connect to the trees
        wires = sorted(list(wires), key=natural_keys)
        if len(wires) > 0:
            wire_hdl = syntax["wire_def"].format(", ".join(wires))
            hdl = [f"\t{wire_hdl}\n"] + hdl

        hdl = "".join(hdl)

        hdl, module_defs, file_out_hdl = self._wrap_hdl(
            hdl, module_defs, language, module_name
        )
        if out is not None:
            self._write_hdl(file_out_hdl, out)

        return hdl, module_defs, file_out_hdl

    def gif(self, out="forest.gif"):
        with open(out, "wb") as fout:
            fout.write(self._repr_png_())

    ### NOTE: ALL METHODS BELOW ARE FOR LEGACY SUPPORT ONLY ###

    def LF(self, x, y=None):
        """Performs an LF transform on the specified node in all trees

        This is node by calling on the corresponding method in the Tree class.
        See the disclaimer inside the docstring of the ExpressionTree method.
        """

        # Try to first apply transform on most significant tree
        # Once a valid transform is applied, use x,y for all other trees
        for t in reversed(list(self.trees)):
            if x < t.width - 1:
                attempt = t.LF(x, y)
                if attempt is not None:
                    x, y = attempt
        return x, y

    def FL(self, x, y=None):
        """Performs an FL transform on the specified node in all trees

        This is node by calling on the corresponding method in the Tree class.
        See the disclaimer inside the docstring of the ExpressionTree method.
        """

        # Try to first apply transform on most significant tree
        # Once a valid transform is applied, use x,y for all other trees
        for t in reversed(list(self.trees)):
            if x < t.width - 1:
                attempt = t.FL(x, y)
                if attempt is not None:
                    x, y = attempt
        return x, y

    def TF(self, x, y=None):
        """Performs a TF transform on the specified node in all trees

        This is node by calling on the corresponding method in the Tree class.
        See the disclaimer inside the docstring of the ExpressionTree method.
        """

        # Try to first apply transform on most significant tree
        # Once a valid transform is applied, use x,y for all other trees
        for t in reversed(list(self.trees)):
            if x < t.width - 1:
                attempt = t.TF(x, y)
                if attempt is not None:
                    x, y = attempt
        return x, y

    def FT(self, x, y=None):
        """Performs an FT transform on the specified node in all trees

        This is node by calling on the corresponding method in the Tree class.
        See the disclaimer inside the docstring of the ExpressionTree method.
        """

        # Try to first apply transform on most significant tree
        # Once a valid transform is applied, use x,y for all other trees
        for t in reversed(list(self.trees)):
            if x < t.width - 1:
                attempt = t.FT(x, y)
                if attempt is not None:
                    x, y = attempt
        return x, y

    def legacy_decouple_node_fanout(self, node, maximum_fanout=2):
        """Decouples the fanout of the specified node in all trees"""

        # Get node's equivalence class
        ec = node.equiv_class
        # Filter out nodes whose parents are equivalent
        ec = [
            x
            for x in ec
            if x.parent is None or x.parent.equiv_class.rep is x.parent
        ]
        # Decouple fanout
        ctr = 0
        for a in range(len(ec)):
            n = ec[a]
            parent = n.parent
            if parent is None:
                continue
            # The last connection does not benefit from extra buffer
            if a == len(ec) - 1:
                ctr -= 1
            index = parent.children.index(n)
            for b in range(ctr // (maximum_fanout - 1)):
                for p in parent.equiv_class:
                    t = p.graph
                    t.insert_buffer(p[index])
            ctr += 1

    def decouple_all_fanout(self, maximum_fanout=2):
        """Decouples the fanout of all nodes in all trees"""
        targets = []
        for t in reversed(self.trees[1:]):
            for n in t:
                if (n.parent is not None) and (n.equiv_class.rep is n):
                    targets.append(n)
        for n in targets:
            self.legacy_decouple_node_fanout(n, maximum_fanout)

    ### NOTE: END LEGACY METHODS ###


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
