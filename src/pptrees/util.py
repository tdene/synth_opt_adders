import os
import re
import uuid


def lg(x):
    """Returns the base-2 logarithm of x, rounded down"""
    return x.bit_length() - 1


def sub_brackets(x):
    """Reformats 'a[0]' to 'a_0'"""
    return x.replace("[", "_").replace("]", "")


def wrap_quotes(original: str):
    """Wrap double quotes around a string"""
    out = original
    if len(original) < 2 or original[0] != '"' or original[-1] != '"':
        out = f'"{out}"'
    return out


def verso_pin(x):
    """Returns the verso version of a pin"""
    return x.replace("out", "in") if "out" in x else x.replace("in", "out")


def catalan(n):
    """Returns the nth Catalan number"""
    if n == 0:
        return 1
    return catalan(n - 1) * (4 * n - 2) // (n + 1)


def catalan_mirror_point(n):
    """Returns the first safe mirror mark for the nth Catalan number"""
    # Get the halfway mark
    half = catalan(n) >> 1
    # If n is odd, there's no clean split
    if n & 1:
        return half + (catalan(n // 2) ** 2) / 2
    # If n is even, there's a clean split
    else:
        return half


def catalan_bounds(n):
    """Returns the first n catalan numbers, minus one"""
    return [catalan(x) - 1 for x in range(n)]


def match_nodes(parent, child, index):
    """Attempts to match the ports of two nodes

    Args:
        parent (Node): The parent node
        child (Node): The child node
        index (int): The index of the parent's input port
    """
    # If no match is found, will return None
    # Otherwise will return a list of pins to be connected
    # List items will be of the format (parent_pin, child_pin)
    ret = []

    # Get the parent and child ports
    parent_ports = parent.node_data["ins"]
    child_ports = child.node_data["outs"]

    # Iterate over all input ports
    for port in parent_ports:
        if port[2 + index] == 0:
            continue
        try:
            # Get the matching output port
            matching_port = get_matching_port(port, child_ports)
        except ValueError:
            return None
        # Figure out which bits of the port to connect
        offset = 0
        for x in range(index):
            offset += port[2 + x]
        # Add the matching pin pairs to the list
        for b in range(port[2 + index]):
            pin1 = (port[0], offset + b)
            pin2 = (matching_port[0], b)
            ret.append((pin1, pin2))

    return ret


def change_in_nets(node, old_nets, new_nets, index):
    """Overwrites the input nets of a node's parent with new nets

    Args:
        node (Node): The node whose in_nets will change
        old_nets (dict): A dictionary that is node.child.out_nets
        new_nets (dict): A dictionary similar to old_nets
    """
    # Loop through all output nets, making a dictionary
    dic = {}
    for k in new_nets:
        new_port = new_nets[k]
        old_port = old_nets[k]
        verso = verso_pin(k)
        # Check if the net is in the node's inputs
        try:
            node_port = node.in_nets[verso]
        except KeyError:
            continue
        # Check if the net is on the correct side of the node's inputs
        flag = False
        for tup in node.node_data["ins"]:
            if tup[0] == verso and tup[2 + index] == 0:
                flag = True
                break
        if flag:
            continue
        # Change the net names
        for a in range(len(new_port)):
            dic[old_port[a]] = new_port[a]
        node_port = [dic.get(x, x) for x in node_port]
        node.in_nets[verso] = node_port
    return node


def get_matching_port(port, other_ports):
    """Returns the port in other_ports that is the verso of port

    Args:
        port (str): The port to find the verso of
        other_ports (list): The list of ports to search
    """
    for other_port in other_ports:
        if port[0] == verso_pin(other_port[0]):
            return other_port
    raise ValueError("No matching port found for {0}".format(port[0]))


def parse_net(x):
    """Converts a net's ID to its name in HDL

    These come in 3 possible flavors:
        - None (unassigned net) -> parsed to n0
        - Integer (assigned net) -> parsed to n`Integer
        - Hardcoded name ($net_name) -> parsed to net_name
    """
    if x is None:
        return "n0"
    if isinstance(x, int):
        return "n" + str(x)
    if "$" in x:
        return x.replace("$", "")
    raise TypeError("net stored in node {0} is invalid".format(repr(x)))


hdl_syntax = {
    "verilog": {
        "entity": "module {0}(\n\t{1}\n);\n",
        "entity_in": "input ",
        "entity_out": "output",
        "entity_port": "{0} {2} {1},",
        "port_range": "[{0}:{1}]",
        "arch": "{1}\nendmodule // {0}\n",
        "inst": "\n\t{1} {0}(\n{2}\n\t);",
        "inst_port": "\t\t.{0}({1})",
        "slice_markers": lambda x: x,
        "wire_def": "wire {0};",
        "comment_string": "// ",
        "file_extension": ".v",
    },
    "vhdl": {
        "entity": "entity {0} is\n\tport (\n{1}\n);\nend entity;\n\n",
        "entity_in": "in",
        "entity_out": "out",
        "entity_port": "\t\t{1} : {0} std_logic{2};\n",
        "port_range": "_vector({0} downto {1})",
        "arch": (
            "architecture {0}_arch of {0} is"
            "\n\tbegin\n{1}\n"
            "end architecture {0}_arch;\n"
        ),
        "inst": ("\t{0}: {1}\n" "\t\tport map (\n{2}\n" "\t\t);"),
        "inst_port": "\t\t{0} => {1}\n",
        "slice_markers": lambda x: x.replace("[", "(")
        .replace("]", ")")
        .replace(":", " downto "),
        "wire_def": "signal {0} : std_logic;",
        "comment_string": "-- ",
        "file_extension": ".vhd",
    },
}


def hdl_entity(name, ins, outs, language="verilog"):
    """Formats an entity declaration

    Args:
        name (str): The name of the entity
        ins (list of (string, int)): A list of input ports
        outs (list of (string, int)): A list of output ports
        language (str): The language in which to generate the HDL
    """
    syntax = hdl_syntax[language]
    ports_str = []
    for port in ins:
        port_range = (
            syntax["port_range"].format(port[1] - 1, 0) if port[1] > 1 else ""
        )
        next_port = syntax["entity_port"].format(
            syntax["entity_in"], port[0], port_range
        )
        ports_str.append(next_port)
    for port in outs:
        port_range = (
            syntax["port_range"].format(port[1] - 1, 0) if port[1] > 1 else ""
        )
        next_port = syntax["entity_port"].format(
            syntax["entity_out"], port[0], port_range
        )
        ports_str.append(next_port)
    ports_str = "\n\t".join(ports_str)[:-1]
    return syntax["entity"].format(name, ports_str)


def hdl_arch(name, body, language="verilog"):
    """Formats an architecture declaration

    Args:
        name (str): The name of the entity
        body (str): The body of the architecture
        language (str): The language in which to generate the HDL
    """
    syntax = hdl_syntax[language]
    if body[-1] == "\n":
        body = body[:-1]
    return syntax["arch"].format(name, body)


def hdl_inst(inst_id, name, ports, language="verilog"):
    """Formats an instance declaration

    Args:
        name (str): The name of the instance
        ports (list of (string, string)): A list of ports to be connected
        language (str): The language in which to generate the HDL
    """
    syntax = hdl_syntax[language]
    ports = [(port[0], syntax["slice_markers"](port[1])) for port in ports]
    ports_list = [
        syntax["inst_port"].format(port[0], port[1]) for port in ports
    ]
    return syntax["inst"].format(inst_id, name, ",\n".join(ports_list))


def sub_ports(hdl, ports):
    """Substitutes port in an HDL string with corresponding module ports"""
    for port in sorted(ports, key=lambda x: natural_keys(x[1]), reverse=True):
        ((local, num), remote) = port
        if num == 1:
            hdl = hdl.replace(local, remote)
        ### NOTE: This is a complete 2 AM hack
        ### It assumes that all ports are zero-indexed, forever
        else:
            remote = remote.split("[")[0]
            hdl = hdl.replace(local, remote)
    return hdl


def atoi(x):
    """Converts a string to an integer"""
    return int(x) if x.isdigit() else x


def natural_keys(text):
    """Human sorting / natural sorting"""
    return [atoi(c) for c in re.split(r"(\d+)", text)]


### NOTE: This needs to be reworked when map files are reworked
### THIS IS A HACK
### Currently it assumes that all lines of map files with logic will contain
### either "assign" or "));"
### And that all lines of map files with ports will contain "Y, "
def parse_mapping(mapping_file):
    """Parses a mapping file and returns a dictionary of mappings"""
    mapping = {}
    with open(mapping_file, "r") as f:
        in_a_module = False
        current_module = None
        for line in f:
            split_line = line.strip().split()
            if len(split_line) == 0:
                continue
            if split_line[0] == "module":
                in_a_module = True
                current_module = split_line[1]
                mapping[current_module] = [[], ""]
            elif split_line[0] == "endmodule":
                in_a_module = False
                current_module = None
            elif in_a_module and "Y, " in line:
                new_split = [x.strip() for x in line.strip().split(",")]
                mapping[current_module][0] = new_split
            elif in_a_module and ("));" in line or "assign" in line):
                mapping[current_module][1] += line
    return mapping


### NOTE: This needs to be reworked when map files are reworked
def merge_mapping_into_cells(hdl, mapping):
    """Merges the definitions found inside a mapping into HDL cells"""
    new_hdl = []
    for line in hdl.split("\n"):
        first_word = None
        split_line = line.strip().split()
        if len(split_line) > 0:
            first_word = split_line[0]
        if first_word in mapping:
            # Extract the nets from the line of HDL
            net_string = re.search(r"\((.*?)\)", line).group(1)
            # Extract the instance name from the line of HDL
            inst_name = re.search(r"U\d+", line).group(0)
            nets = net_string.split(",")
            data = mapping[first_word][1]
            behav = "assign" in data
            new_string = data.replace(f" {first_word}(.", f" {inst_name}(.")
            for a in range(len(nets)):
                net_name = nets[a]
                port_name = mapping[first_word][0][a]
                if not behav:
                    net_name = "({0})".format(net_name)
                    port_name = "({0})".format(port_name)
                new_string = new_string.replace(port_name, net_name)
            new_hdl.append(new_string[:-1])
        else:
            new_hdl.append(line)
    return "\n".join(new_hdl)


def increment_iname(nodes, match_ctr, language="verilog"):
    """Assigns unique names for all cells in the given nodes

    By default, instances are named U0, U1, U2, etc;
                wires are named w0, w1, w2, etc.
    These names need to be made unique.
    """
    # Iterate over all nodes
    for node in nodes:
        # Keep track of name substitutions
        name_sub = {}
        # Get the list of all matches
        match_list = set(re.findall(r"U\d+", node.node_data[language]))
        # Sort the list of all matches in terms of reverse string length
        match_list = sorted(match_list, key=lambda x: -len(x))
        # Substitute the names, using a character unlikely to cause collision
        for old_name in match_list:
            new_name = "$$${0}".format(match_ctr)
            node.node_data[language] = node.node_data[language].replace(
                old_name, new_name
            )
            name_sub[old_name] = new_name.replace("$$$", "U")
            match_ctr += 1
        # Substitute the original "U" character in
        node.node_data[language] = node.node_data[language].replace("$$$", "U")
    return match_ctr


def increment_wname(nodes, match_ctr, language="verilog"):
    """Assigns unique names for all cells in the given nodes

    By default, instances are named U0, U1, U2, etc;
                wires are named w0, w1, w2, etc.
    These names need to be made unique.
    """
    # Iterate over all nodes
    for node in nodes:
        # Keep track of name substitutions
        name_sub = {}
        # Get the list of all matches
        match_list = set(re.findall(r"w\d+", node.node_data[language]))
        # Sort the list of all matches in terms of reverse string length
        match_list = sorted(match_list, key=lambda x: -len(x))
        # Substitute the names, using a character unlikely to cause collision
        for old_name in match_list:
            new_name = "$$${0}".format(match_ctr)
            node.node_data[language] = node.node_data[language].replace(
                old_name, new_name
            )
            name_sub[old_name] = new_name.replace("$$$", "w")
            match_ctr += 1
        # Substitute the original "U" character in
        node.node_data[language] = node.node_data[language].replace("$$$", "w")
    return match_ctr


def display_png(graph, *args, **kwargs):
    """Given a graph, executes its png() method and displays the image

    Args:
        graph (ExpressionGraph): The graph to be rendered
        *args: The arguments to pass to the graph's png() method
        **kwargs: The keyword arguments to pass to the graph's png() method
    """
    # Get a temporary file name
    fname = str(uuid.uuid4()) + ".png"
    # Execute the function
    graph.png(*args, out=fname, **kwargs)
    # Get the PNG data
    ret = open(fname, "rb").read()
    # Delete the PNG file
    os.remove(fname)

    return ret


def display_gif(graphs, *args, **kwargs):
    """Given a list of graphs, executes their png() method and displays a gif

    Args:
        graphs (list of ExpressionGraph): The graphs to be rendered
        *args: The arguments to pass to the graphs' png() method
        **kwargs: The keyword arguments to pass to the graphs' png() method
    """
    # Import PIL.Image here to prevent instant crash on Python 3.6
    import PIL.Image

    # Get temporary file names
    fnames = [str(uuid.uuid4()) + ".png" for _ in range(len(graphs))]
    # Execute the function
    for graph, fname in zip(graphs, fnames):
        graph.png(*args, out=fname, **kwargs)
    # Collect the images
    images = [PIL.Image.open(fname) for fname in fnames]
    # Get maximum width and height
    max_bbox = [0, 0, 0, 0]
    for a in images:
        bbox = a.getbbox()
        if bbox[0] < max_bbox[0]:
            max_bbox[0] = bbox[0]
        if bbox[1] < max_bbox[1]:
            max_bbox[1] = bbox[1]
        if bbox[2] > max_bbox[2]:
            max_bbox[2] = bbox[2]
        if bbox[3] > max_bbox[3]:
            max_bbox[3] = bbox[3]
    for a in range(len(images)):
        im = images[a]
        im = im.crop(max_bbox)
        images[a] = im
    # Save the GIF file
    gif_name = str(uuid.uuid4()) + ".gif"
    images[0].save(
        gif_name,
        save_all=True,
        format="GIF",
        duration=1000,
        loop=0,
        disposal=2,
        transparency=255,
        append_images=images,
    )
    # Get the GIF data
    ret = open(gif_name, "rb").read()
    # Delete the PNG files
    for fname in fnames:
        os.remove(fname)
    # Delete the GIF file
    os.remove(gif_name)

    return ret


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
