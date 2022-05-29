from .ExpressionNode import ExpressionNode as Node
from .ExpressionTree import ExpressionTree
from .util import lg

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

        # self is the p / t tree
        # other is the g tree

        # Start at the root, if not specified
        if self_node is None and other_node is None:
            self_node = self.root
            other_node = other.root
        # If the leafs are reached, this recursive path has finished
        if not self_node.children or not other_node.children:
            return (True, [])
        # If other_node is a buffer, here are what bad things could happen:
        # - There are leafs in other that are also present in self[1]
        #   aka there are g's ahead of p's
        # If nothing bad happens, skip the buffer
        if other_node.value == self.node_defs["buffer"]:
            if other_node.leafs & self_node[1].leafs:
                return (False, None)
            return self._ling_check(other, self_node, other_node[0])
        # If self_node is a buffer, here are what bad things could happen:
        # - There are leafs in other[0] that are not present in self
        #   aka there are g's ahead of p's
        # If nothing bad happens, skip the buffer
        if self_node.value == self.node_defs["buffer"]:
            if other_node[0].leafs & self_node.leafs:
                return (False, None)
            return self._ling_check(other, self_node[0], other_node)
        # Any leafs in other[0] are not present in self[1]
        # aka there are no g's ahead of p's
        if other_node[0].leafs & self_node[1].leafs:
            return (False, None)
        # Any leafs in other[1] but not self[1] must BE self[0] or self[0][1]
        # aka any factorization is resolved immediately
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

    def _ling_combine(self, other, target,
            self_node = None, other_node = None,
            parent = None, index = None,
            pending = False):
        """Stereoscopically combine two trees"""

        # self is the p / t tree
        # other is the g tree

        # Start at the root, if not specified
        if self_node is None and other_node is None:
            self_node = self.root
            other_node = other.root
        # Assign shorthand names for the nodes
        p = self_node
        g = other_node
        new_node = None

        # Check if this location creates a factorization
        factor = None
        next_pending = False
        if not pending:
            if len(p.children) == self.radix:
                if len(g.children) == self.radix:
                    factor = p[0].leafs == (g[1].leafs & ~p[1].leafs)
                    if not factor and (g[1].leafs & ~p[1].leafs):
                        next_pending = True
                elif len(g.children) == 1:
                    raise NotImplementedError("How did you get here? 1")
                    factor = p[0].leafs == (g.leafs & ~p[1].leafs)

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
        ## they should be the same leaf???
        if not p.children and not g.children:
            if p.leafs != g.leafs:
                raise ValueError("Non-matching leafs; impossible error message.")
            new_node = Node(node_defs[p.value])
            # Right-most leaf may be special
            if self._on_lspine(p) and "first_pre" in self.node_defs:
                stem = self.leaf_labels[0]
            # Left-most leaf may be special
            elif self._on_rspine(p) and "lspine_pre" in self.node_defs:
                stem = self.leaf_labels[2]
            else:
                stem = self.leaf_labels[1]
            label = "{0}[{1}]".format(stem, lg(p.leafs)-1)
            new_node = target.add_node(new_node, label = label)
            target._connect_inports(new_node, lg(p.leafs)-1)
            new_node._recalculate_leafs(leafs=p.leafs)

        # Overlapping recurrence nodes
        ## If both nodes are recurrence nodes,
        ## if there is no pending or current de-factorization, just combine them
        if p.value == self.node_defs["black"] and g.value == self.node_defs["black"]:
            if (not factor) and (not pending):
                new_node = Node(node_defs[p.value])
                target.add_node(new_node)
                target.add_edge(parent, new_node, index)
        # resolve current factorization
        if factor:
            if g[0].children:
                raise NotImplementedError("How did you get here? 2")
            new_node = Node("ppa_black_ling")
            target.add_node(new_node)
            target.add_edge(parent, new_node, index)

            new_leaf = Node("ppa_pre_sp")
            label = "{0}[{1}]".format(other.leaf_labels[1], lg(g[0].leafs)-1)
            new_leaf = target.add_node(new_leaf, label = label)
            target.add_edge(new_node, new_leaf, 0)
            target._connect_inports(new_leaf, lg(g[0].leafs)-1)
            new_leaf._recalculate_leafs(leafs=g[0].leafs)

            new_node_2 = Node("ppa_defactor_left")
            target.add_node(new_node_2)
            target.add_edge(new_node, new_node_2, 1)

            self._ling_combine(other, target, p[0], None, new_node_2, 0)
            self._ling_combine(other, target, p[1], g[1], new_node_2, 1)
            return

        if pending:
            if len(g.children) != 1:
                raise NotImplementedError("How did you get here? 3")









        self._ling_combine(other, target, self_node[0], other_node[0])
        self._ling_combine(other, target, self_node[1], other_node[1])

    def stereo_combine(self, others):
        """Stereoscopically combine a set of trees into a single tree

        This implements the ExpressionTree stub method.

        Args:
            others (list): list of trees to combine
        """

        # First check that the trees can be combined
        check, _ = self.stereo_check(others)
        if not check:
            raise ValueError("Trees cannot be combined")

        # Next, combine the trees
        leaf_labels = self.leaf_labels
        # g, t -> gt
        leaf_labels[1] = others[0].leaf_labels[1] + self.leaf_labels[1]
        # Add to node_defs
        ret = AdderTree(
                width = self.width,
                in_ports = self.in_ports,
                out_ports = self.out_ports,
                name = self.name,
                no_shape = True,
                radix = self.radix,
                node_defs = node_defs
                )

        self._ling_combine(others[0], ret)

        # Return the combined tree
        return ret

if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
