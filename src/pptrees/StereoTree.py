from .ExpressionNode import ExpressionNode as Node
from .ExpressionGraph import ExpressionGraph
from .ExpressionTree import ExpressionTree

class StereoTree(ExpressionTree):
    """Defines a stereoscopic combination of two trees of binary expressions

    This is represented by two ExpressionTree's that are overlaid on top of each other.

    Currently it is unsafe to perform transformations on stereoscopic combinations of
        trees, due to lack of theoretical thought or practical checks. As such,
        all transformation methods are disabled in this class.

    Attributes:
        stereo_trees (list): A list of the ExpressionTree's being combined
        stereo_map (function): A function defining how stereoscopic combination works

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

    def __init__(self, stereo_trees, stereo_map):
        """Initializes the StereoTree

        Args:
            stereo_trees (list): A list of the ExpressionTree's being combined
            stereo_map (function): A function defining how stereoscopic combination works

        The trees being combined must have nearly identical characterstics:
            - The same number of leaves
            - The same radix
            - The same idempotency property
            - The same in_shape and out_shape
            - The same in_ports and out_ports

        Furthermore, the trees must not have remapped nodes or been subdivided into blocks
        """

        # Save constructor arguments
        self.stereo_trees = stereo_trees
        self.stereo_map = stereo_map

        # Check and save tree attributes
        self.width = self.check_attr('width')
        self.radix = self.check_attr('radix')
        self.idem = self.check_attr('idem')
        self.in_shape = self.check_attr('in_shape')
        self.out_shape = self.check_attr('out_shape')
        self.in_ports = self.check_attr('in_ports')
        self.out_ports = self.check_attr('out_ports')
        self.blocks = self.check_attr('blocks')
        if self.blocks:
            raise ValueError('StereoTree cannot be pre-divided into blocks')

        # Map the nodes
        self.root = None
        self.stereo_init()

        # Connect the root node to the tree's ports
        self._connect_outports(self.root)
        # Connect the leafs to the tree's ports
        leafs = self._get_leafs()
        for a in range(len(leafs)):
            self._connect_inports(leafs[a], a)

    def check_attr(self, attr):
        """Checks the attribute of the trees being combined

        Args:
            attr (string): The attribute to check

        Returns:
            The attribute of the trees being combined

        Raises:
            ValueError: If the attribute is not the same for all trees
        """
        attr_list = [getattr(tree, attr) for tree in self.stereo_trees]
        if len(set(attr_list)) != 1:
            raise ValueError('StereoTree: ' + attr + ' must be the same for all trees')
        return attr_list[0]

    def stereo_init(self, node = []):
        """Stereoscopically combines all nodes using the stereo_map attribute"""

        # Start at the root node
        if not node:
            node = [x.root for x in self.stereo_trees]
            stereo_def = self.stereo_map(node)
            stereo_node = Node(stereo_def, x_pos = 0, y_pos = 0)
            self.root = stereo_node
        # Once started, just run the function normally on nodes
        else:
            stereo_def = self.stereo_map(node)
            stereo_node = Node(stereo_def)

        # Add the node to the tree
        self.add_node(stereo_node)

        # Recurse through the tree
        get_child = lambda node, c: node[c] if (node and node.children[c:]) else None
        for c in self.radix:
            children = [get_child(n,c) for n in node]
            # If there are no children, continue
            if not any(children):
                continue
            # Otherwise, recurse
            stereo_child = self.stereo_init(children)
            # Connect the child to the parent
            self.add_edge(stereo_node, stereo_child, c)

        # Return the node
        return stereo_node

    def left_rotate(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def right_rotate(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def left_shift(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def right_shift(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def balance(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def lbalance(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def rbalance(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def LF(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def FL(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def FT(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

    def TF(self, node):
        """Disabled method"""
        raise NotImplementedError('StereoTree structure cannot be modified')

if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
