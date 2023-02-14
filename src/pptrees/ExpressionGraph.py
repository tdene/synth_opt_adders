import pathlib

import networkx as nx

from .ExpressionNode import ExpressionNode
from .util import (
    hdl_arch,
    hdl_entity,
    hdl_inst,
    hdl_syntax,
    increment_iname,
    increment_wname,
    merge_mapping_into_cells,
    natural_keys,
    parse_mapping,
    parse_net,
    sub_brackets,
    sub_ports,
    wrap_quotes,
)

try:
    from importlib.resources import path as respath
except ImportError:
    from importlib_resources import path as respath


class ExpressionGraph(nx.DiGraph):
    """Defines a di-graph of arithmetic expressions

    The graph is defined as follows:
    - Each node is a module that computes an arithmetic expression
    - Each edge is a net connecting two node_data

    Attributes:
        name (string): The name of the graph
        next_net (int): The next net name to be used
        next_block (int): The next block name to be used
        blocks (list): The list of blocks in the graph
        in_ports (list of ((string, int), string)): The list of input ports
        out_ports (list of ((string, int), string)): The list of output ports
        in_extras (list of ((string, int), string)):
            The list of extra input ports, caused by equivalence classes
        out_extra (list of ((string, int), string)):
            The list of extra output ports, caused by equivalence classes
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
        if any(x is not None for x in [in_ports, out_ports]) and not all(
            x is not None for x in [in_ports, out_ports]
        ):
            raise ValueError(
                ("in_ports and out_ports" "must both be None or both be lists")
            )

        super().__init__()

        self.name = name

        # Save the input and output ports
        self.in_ports = in_ports
        self.out_ports = out_ports
        self.in_extras = []
        self.out_extras = []

        # Procedurally-generated net names start with "n1"
        self.next_net = 1

        # Procedurally-generated block names start with "block1"
        self.next_block = 0
        self.blocks = [None]

        # Provide support for not merging in the mapping file
        self.merge_mapping = True

        # Keep track of whether the graph has been prepared for HDL
        # NOTE: Preparing a graph for HDL may be destructive
        self._prepared = False

    def add_node(self, node, **attr):
        """Adds a node to the graph

        Args:
            node (ExpressionNode): The name of the node to add
            attr (dict): The attributes of the node to add
        """

        if not isinstance(node, ExpressionNode):
            raise TypeError("Node must be an ExpressionNode")

        # Add GraphViz attributes
        kwargs = node.node_data
        kwargs.update(attr)
        kwargs["shape"] = kwargs.get("shape", "square")
        kwargs["fillcolor"] = kwargs.get("fillcolor", "white")
        kwargs["label"] = kwargs.get("label", "")
        kwargs["style"] = kwargs.get("style", "filled")
        kwargs["pos"] = "{0},{1}!".format(node.x_pos * -1, node.y_pos * -1)

        kwargs["verilog"] = wrap_quotes(kwargs.get("verilog", ""))
        kwargs["vhdl"] = wrap_quotes(kwargs.get("vhdl", ""))

        # Add the node to the graph
        node.graph = self
        super().add_node(node, **kwargs)
        return node

    def remove_node(self, node):
        """Removes a node from the graph

        Args:
            node (ExpressionNode): The name of the node to remove
        """

        if not isinstance(node, ExpressionNode):
            raise TypeError("Node must be an ExpressionNode")

        # Remove all edges towards this node
        parent = node.parent
        if parent is not None:
            self.remove_edge(parent, node)

        # Remove all edges away from this node
        for child in node.children:
            if child is not None:
                self.remove_edge(node, child)

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
        net_name = parent.add_child(child, pin1, pin2, proposed_net_name)
        if proposed_net_name == net_name:
            self.next_net += 1

        # Styles the edge for GraphViz visualization
        kwargs = {
            "arrowhead": "none",
            "ins": [pin1],
            "outs": [pin2],
            "edge_nets": [net_name],
        }

        # Initialize weight to parasitc delay
        # This is later modified by logical effort
        kwargs["fanout"] = 1
        kwargs["delay"] = child.node_data["pd"]
        kwargs["weight"] = kwargs["delay"]

        # If the two nodes are already connnected, simply update the pins
        if self.has_edge(parent, child):
            edge_data = self.get_edge_data(parent, child, default=kwargs)
            edge_data["ins"].append(pin1)
            edge_data["outs"].append(pin2)
            edge_data["edge_nets"].append(net_name)
        else:
            # Add the edge to the graph
            super().add_edge(parent, child, **kwargs)

        return self.get_edge_data(parent, child)

    def remove_edge(self, parent, child):
        """Removes an edge from the graph

        Args:
            parent (ExpressionNode): The parent node
            child (ExpressionNode): The child node
        """

        if not isinstance(parent, ExpressionNode):
            raise TypeError("Node1 must be an ExpressionNode")
        if not isinstance(child, ExpressionNode):
            raise TypeError("Node2 must be an ExpressionNode")
        if not self.has_edge(parent, child):
            raise ValueError("Edge does not exist")

        # Save the edge data
        edge_data = self.get_edge_data(parent, child)

        # Remove the edge from the graph
        super().remove_edge(parent, child)

        # Remove the edge from the nodes
        parent.remove_child(child)

        # Return the edge data
        return edge_data

    ### NOTE: Improve the heuristic used herein
    def update_edge_weight(self, parent, child, weight_fun=None):
        """Updates the weight of an edge from parent to child

        Args:
            parent (ExpressionNode): The parent node
            child (ExpressionNode): The child node
        """

        if not isinstance(parent, ExpressionNode):
            raise TypeError("Node1 must be an ExpressionNode")
        if not isinstance(child, ExpressionNode):
            raise TypeError("Node2 must be an ExpressionNode")
        if not self.has_edge(parent, child):
            raise ValueError("Edge does not exist")

        ### This is a bad estimate of delay
        if weight_fun is None:
            edge_data = self.get_edge_data(parent, child)
            weight = edge_data["delay"]
            weight += edge_data["fanout"]
        else:
            weight = weight_fun(parent, child)

        edge_data["weight"] = weight
        return weight

    def critical_path(self):
        """Returns the longest path of the graph"""

        # Get valid nodes
        valid_nodes = [
            node
            for node in self.nodes
            if node.block is None and node.equiv_class.rep is node
        ]

        if len(valid_nodes) < 2:
            return []

        # Get subgraph view with only valid nodes
        subgraph = self.subgraph(valid_nodes)

        # Find the critical path
        return nx.dag_longest_path(subgraph)

    def add_block(self, *nodes, graph_type=None):
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
        if graph_type is None:
            new_block = ExpressionGraph(name="block_{0}".format(block_id))
        else:
            new_block = graph_type(name="block_{0}".format(block_id))
        subgraph = self.subgraph(nodes)
        new_block.add_nodes_from(subgraph.nodes(data=True))
        new_block.add_edges_from(subgraph.edges(data=True))
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
        if (
            block_id not in range(len(self.blocks))
            or self.blocks[block_id] is None
        ):
            raise ValueError("Invalid block ID")

        # Remove the block from the graph
        block = self.blocks[block_id]
        for node in block:
            node.block = None
        self.blocks[block_id] = None

    def reset_blocks(self):
        """Removes all blocks from the graph"""

        # Remove all blocks from the graph
        for block_id in range(len(self.blocks)):
            if self.blocks[block_id] is not None:
                self.remove_block(block_id)

        # Reset the next block name
        self.next_block = 0
        self.blocks = [None]

    def add_best_blocks(self, graph_type=None):
        """Groups nodes into blocks based on critical paths"""

        path = self.critical_path()

        # Add a block
        if len(path) > 1:
            self.add_block(*path, graph_type=graph_type)
            # Recurse
            return self.add_best_blocks(graph_type=graph_type)
        return

    def _get_internal_nets(self, null_flag=False):
        """Returns the internal nets of the graph"""

        # Compatibility issue
        if null_flag:
            return (set(), set())

        # Get all nets in the graph
        in_nets = set()
        out_nets = set()

        # Get the nets from nodes
        for node in self.nodes:
            # Ignore any nodes that are not the representative of their class
            if node.equiv_class.rep is not node:
                continue
            for net in node.in_nets.values():
                in_nets.update([parse_net(x) for x in net])
            for net in node.out_nets.values():
                out_nets.update([parse_net(x) for x in net])

        # Get the nets from blocks
        for block in [x for x in self.blocks if x is not None]:
            block_in_nets, block_out_nets = block._get_internal_nets()
            in_nets.update(block_in_nets)
            out_nets.update(block_out_nets)

        # Filter out the graph's ports, as these are not internal wires
        if self.in_ports is not None:
            in_ports = [x[0][0] for x in self.in_ports]
        else:
            in_ports = []
        if self.out_ports is not None:
            out_ports = [x[0][0] for x in self.out_ports]
        else:
            out_ports = []
        in_extras = [x[0][0] for x in self.in_extras]
        out_extras = [x[0][0] for x in self.out_extras]
        all_ports = in_ports + out_ports + in_extras + out_extras
        in_nets = [x for x in in_nets if x.split("[")[0] not in all_ports]
        out_nets = [x for x in out_nets if x.split("[")[0] not in all_ports]

        return (set(in_nets), set(out_nets))

    def _get_ports(self):
        """Returns the ports of the graph"""

        # If the ports are defined, return them
        if self.in_ports is not None:
            return (
                self.in_ports + self.in_extras,
                self.out_ports + self.out_extras,
            )

        # Otherwise, find them from nodes and blocks
        in_ports, out_ports = self._get_internal_nets()

        # Signals generated inside this graph are not inputs
        in_ports = in_ports - out_ports

        # Form the ports
        # Assume that all these retrieved nets are 1-bit
        in_internal = [(sub_brackets(x), 1) for x in in_ports]
        in_external = list(in_ports)
        in_ports = [(x, y) for x, y in zip(in_internal, in_external)]

        out_internal = [(sub_brackets(x), 1) for x in out_ports]
        out_external = list(out_ports)
        out_ports = [(x, y) for x, y in zip(out_internal, out_external)]

        return (in_ports + self.in_extras, out_ports + self.out_extras)

    def _prepare_for_hdl(
        self,
        mapping="behavioral",
        language="verilog",
        uniquify_names=True,
    ):
        """Prepares the graph for HDL generation

        Note that this process may destructively render the graph unusable

        Args:
            mapping (str): The cell mapping to use for the HDL generation
            language (str): The language in which to generate the HDL
            uniquify_names (str): Whether wire/instance must be uniquified
        """
        # Check if graph has already been prepared
        if self._prepared:
            return

        # Check that the language is supported
        if language not in ["verilog"]:
            raise ValueError("Unsupported hardware-descriptive language")

        # Set language-specific syntax
        syntax = hdl_syntax[language]

        # Merge in mapping file, if requested
        if self.merge_mapping:
            # Parse the mapping file
            file_suffix = syntax["file_extension"]
            map_file = "{0}_map{1}".format(mapping, file_suffix)
            map_path = respath("pptrees.mappings", map_file)
            with map_path as pkg_map_file:
                mapping_dict = parse_mapping(pkg_map_file)
            # Merge mapping info into the nodes
            for node in self:
                node_hdl = node.hdl(language=language)
                node_hdl = node.node_data[language]
                node_hdl = merge_mapping_into_cells(node_hdl, mapping_dict)
                node.node_data[language] = node_hdl

        # Uniquify wire/instance names, if requested
        if uniquify_names:
            increment_iname(self.nodes(), 1, language)
            increment_wname(self.nodes(), 1, language)

        # Generate the list of extra nets caused by equivalence classes
        in_extras = []
        out_extras = []
        for node in self:
            # If the node is part of an equivalence class,
            # and some part of the equivalence class is not in this graph,
            # and the node is not part of a bigger equivalent subtree,
            # bring up its internal wires to the top level
            if (
                any([x not in self for x in node.equiv_class])
                and node.parent.equiv_class.rep is node.parent
            ):

                # If this node is the representative, its wires become outputs
                if node.equiv_class.rep is node:
                    out_extras += [
                        parse_net(wire)
                        for net in node.equiv_class.out_nets.values()
                        for wire in net
                    ]
                # Otherwise, its wires become inputs
                else:
                    in_extras += [
                        parse_net(wire)
                        for net in node.equiv_class.out_nets.values()
                        for wire in net
                    ]
        # Format the list of extra nets caused by equivalence classes
        self.in_extras = [((sub_brackets(x), 1), x) for x in in_extras]
        self.out_extras = [((sub_brackets(x), 1), x) for x in out_extras]

        # Toggle the prepared flag
        self._prepared = True

    # NOTE: This function fails flake8 C901
    # TO-DO: Make this function pass flake8 C901
    def hdl(
        self,
        out=None,
        mapping="behavioral",
        language="verilog",
        flat=False,
        module_name=None,
        uniquify_names=True,
        description_string="start of unnamed graph",
        hdl_comments=True,
        inst_id="U0",
    ):
        """Creates a HDL description of the graph

        Args:
            out (str): The file to write the HDL to
            mapping (str): The cell mapping to use for the HDL generation
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
        )

        # Update module name, if provided
        if module_name is None:
            module_name = self.name

        # Set language-specific syntax
        syntax = hdl_syntax[language]

        # Create the HDL
        hdl = ""
        module_defs = set()

        # Pull in the HDL description of blocks
        block_ctr = 0
        for block_id in range(len(self.blocks)):
            # Skip non-existent blocks
            if self.blocks[block_id] is None:
                continue
            # Get block
            block = self.blocks[block_id]
            # Provide support for not merging in the mapping file
            block.merge_mapping = self.merge_mapping
            # Get block HDL and add it to master HDL
            block_hdl, block_defs, _ = block.hdl(
                mapping=mapping,
                language=language,
                flat=flat,
                module_name="{0}_block_{1}".format(module_name, block_id),
                uniquify_names=False,
                description_string="block {0}".format(block_id),
                hdl_comments=hdl_comments,
                inst_id="U{0}".format(block_ctr),
            )
            hdl += block_hdl
            module_defs.update(block_defs)
            block_ctr += 1

        # Pull in the HDL description of nodes
        for node in self:
            # Check whether the node is in a block, and whether this is it
            # If the node is not inside a block, it's automatically usable
            usable = node.block is None
            # Otherwise, check whether the node is inside THIS block
            if not usable:
                if node.graph.blocks[node.block] is not self:
                    continue
            # Get node HDL and add it to master HDL
            node_hdl = node.hdl(language=language)
            hdl += node_hdl

        ### NOTE: Is this general? Improvements wanted
        ### In general, hard-coding an is_block flag sounds like a bad idea
        is_block = list(self.nodes)[0].graph is not self

        # If the graph is a block, then it has individual ports
        # for each bit of every input and output port.
        # So the HDL should reflect through judicious use of net name fixing
        if is_block and not flat:
            (in_ports, out_ports) = self._get_ports()
            for a in in_ports + out_ports:
                hdl = hdl.replace(a[1], a[0][0])

        # Add wire definitions
        # But if this graph is a block,
        # all wires that are inputs into the module are not internal
        # all wires that are outputs from from the cells are not internal
        # therefore, no wires are internal
        in_wires, out_wires = self._get_internal_nets(null_flag=is_block)
        wires = in_wires | out_wires
        wires = sorted(list(wires), key=natural_keys)
        if len(wires) > 0:
            wire_hdl = syntax["wire_def"].format(", ".join(wires))
        else:
            wire_hdl = ""

        # Assemble the HDL
        if wire_hdl:
            hdl = "\t" + wire_hdl + "\n" + hdl
        if hdl_comments:
            hdl = syntax["comment_string"] + description_string + "\n" + hdl

        # If flat HDL is desired, it can returned here
        if flat:
            (in_ports, out_ports) = self._get_ports()
            hdl = sub_ports(hdl, in_ports + out_ports)
            return hdl, module_defs, hdl

        # Otherwise, return the HDL module definition
        hdl, module_defs, file_out_hdl = self._wrap_hdl(
            hdl, module_defs, language, module_name, inst_id
        )

        # Write the HDL to file
        if out is not None:
            self._write_hdl(file_out_hdl, out)

        return hdl, module_defs, file_out_hdl

    def _wrap_hdl(
        self,
        hdl,
        module_defs,
        language="verilog",
        module_name=None,
        inst_id="U0",
    ):
        """Wraps the HDL in a module definition"""

        # If flat HDL is not desired, wrap the graph in a module
        ## First get in_ports and out_ports
        (in_ports, out_ports) = self._get_ports()
        entity_ins = [x[0] for x in in_ports]
        entity_outs = [x[0] for x in out_ports]
        ## Then create the entity
        entity = hdl_entity(module_name, entity_ins, entity_outs, language)
        ## Then create the architecture
        arch = hdl_arch(module_name, hdl, language)
        ## Add the entity and architecture to the module_defs
        formatted_defs = sorted(list(module_defs), key=natural_keys)
        file_out_hdl = entity + arch + "".join(formatted_defs)
        module_defs.add(entity + arch)
        ## Create an instance of the module
        inst_ports = [[x[0][0], x[1]] for x in in_ports + out_ports]
        inst = hdl_inst(inst_id, module_name, inst_ports, language)
        ## Add the instance to the HDL
        hdl = inst

        return hdl, module_defs, file_out_hdl

    def _write_hdl(
        self,
        file_out_hdl,
        out=None,
    ):
        """Writes the HDL to a file"""
        # Check that output path is valid
        if out is None:
            raise ValueError("Output path must be defined")

        outdir = pathlib.Path(out).resolve().parent
        if not outdir.exists():
            raise ValueError("Output path does not exist")

        with open(out, "w") as f:
            f.write(file_out_hdl)


if __name__ == "__main__":
    raise RuntimeError("This module is not intended to be run directly")
