import networkx as nx
import pydot

from .ExpressionNode import ExpressionNode as Node
from .ExpressionGraph import ExpressionGraph
from .modules import modules
from .util import lg
from .util import get_matching_port

class ExpressionTree(ExpressionGraph):
    """Defines a tree of binary expressions

    Attributes:
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
                 in_ports,
                 out_ports,
                 name="tree",
                 start_point="serial",
                 radix=2,
                 idem=False,
                 node_defs={}
                ):
        """Initializes the ExpressionTree

        Args:
            width (int): The number of leaves in the tree
            in_ports (list of ((string, int), string)): List of input ports
            out_ports (list of ((string, int), string)): List of output ports
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
            raise TypeError("Tree width must be an integer")
        if width < 1:
            raise ValueError("Tree width must be at least 1")
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
        self.radix = radix
        self.idem = idem
        self.node_defs = node_defs

        # Get node port shapes from the module definitions
        self.in_shape = [x[1] for x in modules[node_defs["pre"]]["ins"]]
        self.out_shape = [x[1] for x in modules[node_defs["root"]]["outs"]]

        self.black_shape = [x[1] for x in modules[node_defs["black"]]["ins"]]
        black_out_shape = [x[1] for x in modules[node_defs["black"]]["outs"]]
        black_out_shape = [self.radix*x for x in black_out_shape]
        if black_out_shape != self.black_shape:
            raise ValueError(("The main recurrence node of the tree"
                              " must have the same input and output shape"))
        del black_out_shape

        # Check that node shapes are compatible with port shapes
        ### NOTE: INPUT SHAPE IS CURRENTLY ASSUMED TO BE [1,1,1,..]
        ### TO-DO: Allow for arbitrary input shape
        ### Need to check whole file for this implicit assumption
        for a in range(len(self.in_shape)):
            if a > len(in_ports)-1 or in_ports[a][0][1] != self.width:
                raise ValueError(("Input port {} of the tree must have the"
                                  " compatible shape with input shape of the"
                                  " pre-processing node").format(a))
        for a in range(len(self.out_shape)):
            if a > len(out_ports)-1 or self.out_shape[a] != out_ports[a][0][1]:
                raise ValueError(("Output port {} of the tree must have the"
                                  " same shape as the output shape of the"
                                  " root node").format(a))

        # Initialize the graph
        super().__init__(name=name,in_ports=in_ports,out_ports=out_ports)

        # Initialize the tree

        ## Initialize the root node
        self.root = Node(node_defs["root"], x_pos = 0, y_pos = 0)
        self.root = self.add_node(self.root)
        ### Connect the root node to the tree's ports
        self._connect_outports(self.root)

        ## Initialize the rest of the tree
        prev_root = self.root
        pre_counter = self.width-1
        while pre_counter > -1:
            for a in range(radix):
                ## Place pre-processing nodes
                if a == 0 or pre_counter < radix-1:
                    # Left spine is special
                    if pre_counter == self.width-1:
                        pre = node_defs.get("lspine_pre", node_defs["pre"])
                    # Right-most pre- may be special
                    elif pre_counter == 0:
                        pre = node_defs.get("first_pre", node_defs["pre"])
                    else:
                        pre = node_defs["pre"]
                    pre_node = Node(pre)
                    self.add_node(pre_node)
                    self.add_edge(prev_root, pre_node, a)
                    self._connect_inports(pre_node, pre_counter)
                    pre_node._recalculate_leafs(leafs=pre_counter)
                    pre_counter -= 1
                else:
                    black_node = Node(node_defs["black"])
                    self.add_node(black_node)
                    self.add_edge(prev_root, black_node, a)
                # Advance prev_root
                if a == radix-1:
                    prev_root = prev_root.children[1]

    def __len__(self):
        """Redefine the len() function to return the depth of the tree"""
        depth = 0
        for n in self.nodes:
            if n.y_pos > depth:
                depth = n.y_pos
        return depth+1

    def __getitem__(self, key):
        """Redefine the [] operator to readily access nodes

        Calling tree[x,y] will return the xth node from the right at depth y
        """
        if isinstance(key, tuple) and len(key) == 2:
            nodes = self._get_row(key[0])
            return nodes[key[1]]
        else:
            return super().__getitem__(key)

    def _get_row(self, depth):
        """Return the nodes at a given depth"""
        nodes = [n for n in self.nodes if n.y_pos == depth]
        return sorted(nodes, key=lambda x: -x.x_pos)

    def _get_leafs(self):
        """Return a list of leaf nodes"""
        leafs = []
        for n in self.nodes:
            if len(n.children) == 0:
                leafs.append(n)
        return sorted(leafs, key=lambda x: -x.x_pos)

    def _connect_outports(self, root):
        """Connect the tree's output ports to the root node"""
        for a in range(len(self.out_shape)):
            port_name = self.out_ports[a][0][0]
            if self.out_shape[a] == 1:
                net_name = "${}".format(port_name)
                root.out_nets[port_name][0] = net_name
                continue
            for b in range(self.out_shape[a]):
                net_name = "${}[{}]".format(port_name,b)
                root.out_nets[port_name][b] = net_name

    def _connect_inports(self, node, index):
        """Connect the tree's input ports to a pre-processing node"""
        for a in range(len(self.in_shape)):
            port_name = self.in_ports[a][0][0]
            net_name = "${}[{}]".format(port_name,index)
            node.in_nets[port_name][0] = net_name

    def add_edge(self, parent, child, index):
        """Adds a directed edge to the tree, from child output to parent input
        All index ports on the parents's port list are connected to the child

        Args:
            parent (Node): The parent node
            child (Node): The child node
            index (int): The index of the parent's input port
        """
        if not isinstance(parent, Node):
            raise TypeError("Parent must be an Node")
        if not isinstance(child, Node):
            raise TypeError("Child must be an Node")
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if index < -self.radix or index > self.radix-1:
            raise ValueError(("Tree nodes may not have more edges"
                              "than the radix of the tree"))

        # Normalize index
        index = index % self.radix

        # Get the parent and child ports
        parent_ports = modules[parent.value]["ins"]
        child_ports = modules[child.value]["outs"]

        # Attempt to connect all ports
        for port in parent_ports:
            if port[2+index] == 0:
                continue
            # This will raise an exception if the port is not found
            matching_port = get_matching_port(port, child_ports)
            # Figure out which bits of the port to connect to
            offset = 0
            for x in range(index):
                offset += port[2+x]
            # Add an edge for each bit of the port
            for b in range(port[2+index]):
                pin1 = (port[0], b+offset)
                pin2 = (matching_port[0], b)
                super().add_edge(parent, pin1, child, pin2)
        
        # Adjust x-pos and y-pos of the child
        ### NOTE: THIS IS HARD-CODED FOR RADIX OF 2
        ### TO-DO: Make this more general
        y_pos = parent.y_pos+1
        x_diff = 1

        if index == 0:
            x_pos = parent.x_pos + x_diff
        elif index == 1:
            x_pos = parent.x_pos - x_diff

        child.x_pos = x_pos
        child.y_pos = y_pos

        diagram_pos = "{0},{1}!".format(x_pos*-1, y_pos*-1)
        self.nodes[child]["pos"] = diagram_pos

    ### NOTE: THIS IS HARD-CODED FOR RADIX OF 2
    ### TO-DO: Make this more general
    def left_rotate(self, node):
        """Rotate a node to the left

        Args:
            node (Node): The node to rotate
        """
        if not isinstance(node, Node):
            raise TypeError("node must be an Node")
        if node.parent is None or len(node.parent.children) != self.radix:
            raise ValueError("Can only rotate nodes with full families")
        if node.parent[1] != node:
            raise ValueError("Can only rotate right children")

        # Get the parent and child nodes
        parent = node.parent
        grandparent = parent.parent
        lchild = node[0]
        rchild = node[1]
        plchild = node.parent[0]
        if grandparent is None:
            thru_root = True
        else:
            thru_root = False
            parent_dir = grandparent.children.index(parent)

        # Adjust the y-pos
        parent.y_pos += 1
        plchild.iter_down(lambda x: setattr(x, "y_pos", x.y_pos+1))
        node.iter_down(lambda x: setattr(x, "y_pos", x.y_pos-1))
        lchild.y_pos += 1

        # Disconnect the nodes
        if not thru_root:
            self.remove_edge(grandparent, parent)
        self.remove_edge(parent, node)
        self.remove_edge(node, lchild)
        if thru_root:
            self.remove_edge(parent, plchild)
            self.remove_edge(node, rchild)

        # If rotating through root, nodes must be morphed
        if thru_root:
            self.remove_node(parent)
            parent = parent.morph(self.node_defs["lspine"])
            self.add_node(parent)

            self.remove_node(node)
            node = node.morph(self.node_defs["root"])
            self.add_node(node)
            self.root = node
            self._connect_outports(self.root)

        # Rotate the nodes
        if not thru_root:
            self.add_edge(grandparent, node, parent_dir)
        if thru_root:
            self.add_edge(parent, plchild, 0)
        self.add_edge(parent, lchild, 1)
        self.add_edge(node, parent, 0)
        if thru_root:
            self.add_edge(node, rchild, 1)

        return node

    ### NOTE: THIS IS HARD-CODED FOR RADIX OF 2
    ### TO-DO: Make this more general
    def right_rotate(self, node):
        """Rotate a node to the right

        Args:
            node (Node): The node to rotate
        """
        if not isinstance(node, Node):
            raise TypeError("node must be an Node")
        if node.parent is None or len(node.parent.children) != self.radix:
            raise ValueError("Can only rotate nodes with full families")
        if node.parent[0] != node:
            raise ValueError("Can only rotate left children")

        # Get the parent and child nodes
        parent = node.parent
        grandparent = parent.parent
        rchild = node[1]
        lchild = node[0]
        prchild = node.parent[1]
        if grandparent is None:
            thru_root = True
        else:
            thru_root = False
            parent_dir = grandparent.children.index(parent)

        # Adjust the y-pos
        parent.y_pos += 1
        prchild.iter_down(lambda x: setattr(x, "y_pos", x.y_pos+1))
        node.iter_down(lambda x: setattr(x, "y_pos", x.y_pos-1))
        rchild.y_pos += 1

        # Disconnect the nodes
        if not thru_root:
            self.remove_edge(grandparent, parent)
        self.remove_edge(parent, node)
        self.remove_edge(node, rchild)
        if thru_root:
            self.remove_edge(parent, prchild)
            self.remove_edge(node, lchild)

        # If rotating through root, nodes must be morphed
        if thru_root:
            self.remove_node(parent)
            parent = parent.morph(self.node_defs["black"])
            self.add_node(parent)

            self.remove_node(node)
            node = node.morph(self.node_defs["root"])
            self.add_node(node)
            self.root = node
            self._connect_outports(self.root)

        # Rotate the nodes
        if not thru_root:
            self.add_edge(grandparent, node, parent_dir)
        self.add_edge(parent, rchild, 0)
        if thru_root:
            self.add_edge(node, lchild, 0)
        self.add_edge(node, parent, 1)
        if thru_root:
            self.add_edge(parent, prchild, 1)

        return node

    def _fix_diagram_positions(self):
        """Fix the positions of the nodes in the diagram"""

        depth = len(self)
        leafs = self._get_leafs()
        # Set x_pos of the leafs to consecutive numbers
        ctr = 0
        for leaf in leafs:
            leaf.x_pos = ctr
            ctr -= 1
        leafs[-1].x_pos -= 1
        # Adjust other nodes' x_pos based on the leafs
        for d in range(depth-1, -1, -1):
            for node in self._get_row(d):
                if len(node.children) > 0:
                    avg = sum([x.x_pos for x in node.children])/self.radix
                    node.x_pos = avg
                x_pos = node.x_pos
                y_pos = node.y_pos
                diagram_pos = "{0},{1}!".format(x_pos*-1, y_pos*-1)
                self.nodes[node]["pos"] = diagram_pos

    def png(self, fname="tree.png"):
        """Generate a PNG representation of the tree using GraphViz"""

        # Correct the positions of the nodes
        self._fix_diagram_positions()
        # Convert the graph to pydot
        pg = nx.drawing.nx_pydot.to_pydot(self)
        pg.set_splines("false")
        pg.set_concentrate("true")

        pg.write_dot(fname.replace(".png", ".dot"))
        pg.write_png(fname, prog="neato")

if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
