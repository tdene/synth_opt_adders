import re
import networkx as nx

from .ExpressionNode import ExpressionNode
from .modules import modules
from .util import hdl_syntax, hdl_entity, hdl_arch, hdl_inst
from .util import parse_net, sub_brackets

class ExpressionGraph(nx.DiGraph):
    """Defines a di-graph of arithmetic expressions

    The graph is defined as follows:
    - Each node is a module that computes an arithmetic expression
    - Each edge is a net connecting two modules

    Attributes:
        name (string): The name of the graph
        next_net (int): The next net name to be used
        next_block (int): The next block name to be used
        blocks (list): The list of blocks in the graph
        in_ports (list of ((string, int), string)): The list of input ports
        out_ports (list of ((string, int), string)): The list of output ports
    """

    def __init__(self, name="graph", in_ports=None, out_ports=None):
        """Initializes the graph

        Specifying in_ports and out_ports is optional.
        Doing so implies that the graph is already connected inside of a larger
        structure.
        If they are not specified, the graph will finds its own.

        Args:
            name (string): The name of the graph
            in_ports (list of tuples): The list of input ports
            out_ports (list of tuples): The list of output ports
        """

        # Make sure that in_ports and out_ports are both None or both lists
        if any(x is not None for x in [in_ports, out_ports]) and \
                not all(x is not None for x in [in_ports, out_ports]):
            raise ValueError(("in_ports and out_ports"
                "must both be None or both be lists"))

        self.name = name

        # Save the input and output ports
        self.in_ports = in_ports
        self.out_ports = out_ports

        # Procedurally-generated net names start with "n1"
        self.next_net = 1

        # Procedurally-generated block names start with "block1"
        self.next_block = 0
        self.blocks = [None]

        super().__init__()

    def add_node(self, node, **attr):
        """Adds a node to the graph

        Args:
            node (ExpressionNode): The name of the node to add
            attr (dict): The attributes of the node to add
        """

        if not isinstance(node, ExpressionNode):
            raise TypeError("Node must be an ExpressionNode")

        # Add GraphViz attributes
        attr = modules[node.value]
        attr["shape"] = attr.get("shape", "square")
        attr["fillcolor"] = attr.get("fillcolor", "white")
        attr["label"] = attr.get("label", "")
        attr["style"] = attr.get("style", "filled")

        # Add the node to the graph
        super().add_node(node, **attr)
        return node

    def remove_node(self, node):
        """Removes a node from the graph

        Args:
            node (ExpressionNode): The name of the node to remove
        """

        if not isinstance(node, ExpressionNode):
            raise TypeError("Node must be an ExpressionNode")
        
        # Remove the node from the graph
        super().remove_node(node)
        return node

    def add_edge(self, parent, pin1, child, pin2):
        """Adds a directed edge to the graph, from parent to child

        Args:
            parent (ExpressionNode): The name of the first node
            pin1 (tuple): (name, index) of the pin on the first node
            child (ExpressionNode): The name of the second node
            pin2 (tuple): (name, index) of the pin on the second node
        """

        if not isinstance(parent, ExpressionNode):
            raise TypeError("Node1 must be an ExpressionNode")
        if not isinstance(child, ExpressionNode):
            raise TypeError("Node2 must be an ExpressionNode")

        # Connect the nodes
        proposed_net_name = "$n{0}_{1}".format(self.next_net, self.name)
        actual_net_name = parent.add_child(child, pin1, pin2)
        if proposed_net_name == actual_net_name:
            self.next_net += 1

        # Styles the edge for GraphViz visualization
        attr = {
            "arrowhead": "none",
            "headport": "ne",
            "tailport": "sw",
            "ins": [pin1],
            "outs": [pin2],
            "edge_nets": [actual_net_name]
        }

        # Initialize weight to 1
        # This is later modified by logical effort
        attr["weight"] = 1

        # If the two nodes are already connnected, simply update the pins
        if self.has_edge(parent, child):
            edge_data = self.get_edge_data(parent, child, default = attr)
            edge_data["ins"].append(pin1)
            edge_data["outs"].append(pin2)
            edge_data["edge_nets"].append(actual_net_name)
        else:
        # Add the edge to the graph
            super().add_edge(parent, child, **attr)

        return self.get_edge_data(parent, child)

    def add_block(self, *nodes):
        """Creates a new module block of nodes

        This is a sub-graph of nodes that will be flattened together into a
        single monolithic module.

        Args:
            nodes (list): The list of nodes to add to the block
        """
        if not all([isinstance(node, ExpressionNode) for node in nodes]):
            raise TypeError("Nodes must be ExpressionNodes")
        if not all([node.block is None for node in nodes]):
            raise ValueError("Nodes must not already be in a block")

        # If the block is empty, don't create it
        if not nodes:
            return None
        
        # Get the name of the block
        block_id = self.next_block

        # Assign the block to the nodes
        for node in nodes:
            node.block = block_id

        # Create the block
        new_block = self.subgraph(nodes)
        self.blocks[block_id] = new_block
        if block_id == len(self.blocks) - 1:
            self.blocks.append(None)

        # Increment the next block name
        self.next_block = next(
                x for x in range(len(self.blocks)) if self.blocks[x] is None
        )

        return block_id

    def remove_block(self, block_id):
        """Removes a block from the graph

        Args:
            block_id (int): The ID of the block to remove
        """
        if block_id not in range(len(self.blocks)) or self.blocks[block_id] is None:
            raise ValueError("Invalid block ID")

        # Remove the block from the graph
        block = self.blocks[block_id]
        for node in block:
            node.block = None
        self.blocks[block_id] = None

    def reset_blocks(self):
        """Removes all blocks from the graph"""

        # Remove all blocks from the graph
        for block_id in [x for x in self.blocks if x is not None]:
            self.remove_block(block_id)

        # Reset the next block name
        self.next_block = 0
        self.blocks = [None]

    def _get_internal_nets(self):
        """Returns the internal nets of the graph"""

        # Get all nets in the graph
        in_nets = set()
        out_nets = set()

        # Get the nets from nodes
        for node in self.nodes:
            for net in node.in_nets.values():
                in_nets.update([parse_net(net) for x in net])
            for net in node.out_nets.values():
                out_nets.update([parse_net(net) for x in net])

        # Get the nets from blocks
        for block in [x for x in self.blocks if x is not None]:
            block_in_nets, block_out_nets = block._get_internal_nets()
            in_nets.update(block_in_nets)
            out_nets.update(block_out_nets)

        # If the graph has pre-defined ports, filter them out
        if self.in_ports is not None:
            in_ports = [x[0] for x in in_ports[0]]
            in_nets = [x for x in in_nets if x.split("[")[0] not in in_ports]
            out_ports = [x[0] for x in out_ports[0]]
            out_nets = [x for x in out_nets if x.split("[")[0] not in out_ports]

        return (set(in_nets), set(out_nets))

    def _get_ports(self):
        """Returns the ports of the graph"""

        # If the ports are defined, return them
        if self.in_ports is not None:
            return (self.in_ports, self.out_ports)

        # Otherwise, find them from nodes and blocks
        in_ports, out_ports = self._get_internal_nets()

        # Signals generated inside this graph are not inputs
        in_ports = in_ports - out_ports

        # Form the ports
        # Assume that all these retrieved nets are 1-bit
        in_internal = [(sub_brackets(x),1) for x in in_ports]
        in_external = list(in_ports)
        in_ports = (in_internal, in_external)

        out_internal = [(sub_brackets(x),1) for x in out_ports]
        out_external = list(out_ports)
        out_ports = (out_internal, out_external)

        return (in_ports, out_ports)

    def hdl(
        self,
        language="verilog",
        flat=False,
        full_flat=False,
        module_name=None,
        description_string="start of unnamed graph"
    ):
        """Creates a HDL description of the graph

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
        # Check that the language is supported
        if language not in ["verilog", "vhdl"]:
            raise ValueError("Unsupported hardware-descriptive language")

        # If module name is not defined, set it to graph's name
        if module_name is None:
            module_name = self.name

        # Set language-specific syntax
        syntax = hdl_syntax[language]

        # Create the HDL

        hdl = ""
        module_defs = set()

        # Pull in the HDL description of blocks
        for block_id in range(len(self.blocks)):
            if self.blocks[block_id] is None:
                continue
            block = self.blocks[block_id]

            block_hdl, block_defs = block.hdl(
                    language=language,
                    flat=full_flat,
                    full_flat=True,
                    module_name=module_name + "_block_" + str(block_id),
                    description_string="block {0}".format(block_id)
            )

            hdl += block_hdl
            module_defs.update(block_defs)

        # Pull in the HDL description of nodes outside of blocks
        for node in self:
            if node.block is not None:
                continue
            node_hdl, node_defs = node.hdl(
                    language=language,
                    flat=full_flat
            )

            hdl += node_hdl
            module_defs.update(node_defs)

        # This HDL description will have multiple instances in it
        # By default, util.hdl_inst names all instances "U0"
        # These names need to be made unique
        U_count = 0
        for U in re.finditer(r"U\d+", hdl):
            hdl = hdl[:U.start()] + "U" + str(U_count) + hdl[U.end():]
            U_count += 1

        # Add wire definitions
        in_wires, out_wires = self._get_internal_nets()
        wires = in_wires | out_wires

        wire_hdl = syntax["wire_def"].format(",".join(wires))

        # Assemble the HDL
        hdl = syntax["comment_string"] + description_string + "\n" + \
                wire_hdl + "\n" + hdl

        # If flat HDL is desired, it can returned here
        if flat:
            return hdl, module_defs

        # If flat HDL is not desired, wrap the graph in a module
        ## First get in_ports and out_ports
        (in_ports, out_ports) = self._get_ports()
        ## Then create the entity
        entity = hdl_entity(module_name, in_ports[0], out_ports[0], language)
        ## Then create the architecture
        arch = hdl_arch(module_name, hdl, language)
        ## Add the entity and architecture to the module_defs
        module_defs.add(entity+arch)
        ## Create an instance of the module
        inst_ports = [[x[0][0],x[1]] for x in ins + outs]
        inst = hdl_inst(module_name, inst_ports, language)

        return hdl, module_defs

if __name__ == "__main__":
    raise RuntimeError("This module is not intended to be run directly")
