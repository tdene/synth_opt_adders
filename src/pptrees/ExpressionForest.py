import re

from .ExpressionTree import ExpressionTree
from .ExpressionGraph import ExpressionGraph
from .modules import *
from .util import lg

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
        if start_point not in ["serial", "sklansky",
                "kogge-stone", "brent-kung"]:
            error = "Forest start point {0} is not implemented"
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
                    name="tree_{}".format(a-1),
                    radix=radix
            )
            self.trees.append(t)

        # Initialize the graph
        super().__init__(name=name,in_ports=in_ports,out_ports=out_ports)

        # Transform the forest towards the starting point
        if start_point == "serial":
            pass
        elif start_point == "sklansky":
            for t in self.trees[1:]:
                t.rbalance(t.root[1])
        elif start_point == "kogge-stone":
            for t in self.trees[1:]:
                t.lbalance(t.root[1], with_buffers=True)
        elif start_point == "brent-kung":
            for t in self.trees[1:]:
                t.rbalance(t.root[1])

    def __getitem__(self, key):
        """Returns the tree at the given index

        Args:
            key (int): The index of the tree to return

        Returns:
            ExpressionTree: The tree at the given index
        """
        return self.trees[key]

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
            for i2 in range(i1):
                t2 = self.trees[i2]
                for n1 in t1.nodes:
                    for n2 in t2.nodes:
                        if n1.equiv(n2):
                            n1.set_equiv(n2)

    ### NOTE: Where this logic belongs is an open question
    def find_parallel_tracks(self):
        """Finds parallel tracks amongst the forest's trees"""
        for i1 in reversed(range(len(self.trees))):
            t1 = self.trees[i1]
            for i2 in range(i1):
                t2 = self.trees[i2]
                for n1 in t1.nodes:
                    for n2 in t2.nodes:
                        if n1.tracks(n2):
                            n1.set_tracks(n2)

    ### NOTE: Improve fanout estimate
    def _calc_node_fanout(self, node, tree):
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
        # Grab the node's equivalence class
        ec = node.equiv_class
        # If node is not ec's representative, do nothing
        if ec[0] is not node:
            return
        # If node is root, do noting
        if node.parent is None:
            return

        # Count the fanout
        ctr = set()
        for n in ec:
            ctr.add(n.parent.equiv_class[0])
        fanout = len(ctr)

        # Modify the relevant edge's data
        e_data = tree.get_edge_data(node.parent,node)
        index = node.parent.children.index(node)
        g = modules[node.value]["le"][index]
        ### This is a bad estimate of fanout's effect on delay
        e_data["fanout"] = g*fanout
        tree.update_edge_weight(node.parent, node)

        return fanout

    def calculate_fanout(self):
        """Calculates the fanout of all nodes in the forest

        See the description of _calc_node_fanout for details
        """
        # Calculate equivalence classes
        self.find_equivalent_nodes()

        for t in self.trees:
            for n in t:
                self._calc_node_fanout(n,t)

    ### NOTE: Improve cross-coupling capacitance estimate
    def _calc_node_tracks(self, node, tree):
        """Estimates the delay caused by parallel wires for a node

        A node has tracks of k if:
         - node is the representative of an equivalence class
         - There are k nodes in the forest such that
            - They are the heads of their own equivalence classes
            - node.y_pos = other.y_pos
            - node < other, other < node.parent, node.parent < other.parent
            or
            - node > other, node < other.parent, other.parent > node.parent
        """
        # Grab the node's tracks class
        tr = node.tracks_class
        # If node is not its equivalence class representative, do nothing
        if node.equiv_class[0] is not node:
            return
        # If node is root, do noting
        if node.parent is None:
            return

        # Count the tracks
        tracks = len(tr)

        # Modify the relevant edge's data
        e_data = tree.get_edge_data(node.parent,node)
        ### This is a bad estimate of tracks' effect on delay
        e_data["tracks"] = tracks
        tree.update_edge_weight(node.parent, node)

        return tracks

    def calculate_tracks(self):
        """Calculates the tracks of all nodes in the forest

        See the description of _calc_node_tracks for details
        """
        # Calculate equivalence classes
        self.find_equivalent_nodes()

        for t in self.trees:
            for n in t:
                self._calc_node_tracks(n,t)

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

    ### NOTE: ALL METHODS BELOW ARE FOR LEGACY SUPPORT ONLY ###

    def LF(self, x, y = None):
        """Performs an LF transform on the specified node in all trees

        This is node by calling on the corresponding method in the Tree class.
        See the disclaimer inside the docstring of the ExpressionTree method.
        """

        # Try to first apply transform on most significant tree
        # Once a valid transform is applied, use x,y for all other trees
        for t in reversed(list(self.trees)):
            if x < t.width-1:
                attempt = t.LF(x, y)
                if attempt is not None:
                    x, y = attempt
        return x, y

    def FL(self, x, y = None):
        """Performs an FL transform on the specified node in all trees

        This is node by calling on the corresponding method in the Tree class.
        See the disclaimer inside the docstring of the ExpressionTree method.
        """

        # Try to first apply transform on most significant tree
        # Once a valid transform is applied, use x,y for all other trees
        for t in reversed(list(self.trees)):
            if x < t.width-1:
                attempt = t.FL(x, y)
                if attempt is not None:
                    x, y = attempt
        return x, y

    def TF(self, x, y = None):
        """Performs a TF transform on the specified node in all trees

        This is node by calling on the corresponding method in the Tree class.
        See the disclaimer inside the docstring of the ExpressionTree method.
        """

        # Try to first apply transform on most significant tree
        # Once a valid transform is applied, use x,y for all other trees
        for t in reversed(list(self.trees)):
            if x < t.width-1:
                attempt = t.TF(x, y)
                if attempt is not None:
                    x, y = attempt
        return x, y

    def FT(self, x, y = None):
        """Performs an FT transform on the specified node in all trees

        This is node by calling on the corresponding method in the Tree class.
        See the disclaimer inside the docstring of the ExpressionTree method.
        """

        # Try to first apply transform on most significant tree
        # Once a valid transform is applied, use x,y for all other trees
        for t in reversed(list(self.trees)):
            if x < t.width-1:
                attempt = t.FT(x, y)
                if attempt is not None:
                    x, y = attempt
        return x, y

    def decouple_fanout(self, node):
        """Decouples the fanout of the specified node in all trees"""

        # Decouple fanout from most significant to least
        ec = sorted(node.equiv_class,
                key = lambda x: x.graph.width, reverse=True)
        ctr = 0
        ec = [x for x in ec \
                if x.parent is None or x.parent.equiv_class[0] == x.parent]
        ec = sorted(ec, key = lambda x: x.graph.width, reverse=True)
        for n in ec:
            parent = n.parent
            if parent is None:
                continue
            # The last connection, to the root, does not benefit from buffer
            if parent.parent == None:
                ctr -= 1
            index = parent.children.index(n)
            for a in range(ctr):
                for p in parent.equiv_class:
                    t = p.graph
                    t.insert_buffer(p[index])
            ctr += 1

    def decouple_all_fanout(self):
        """Decouples the fanout of all nodes in all trees"""
        for t in reversed(self.trees):
            print('new_tree')
            targets = []
            for n in t:
                targets.append(n)
        for n in targets:
            self.decouple_fanout(n)


    ### NOTE: END LEGACY METHODS ###

if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
