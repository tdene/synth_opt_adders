import re
from .modules import *

def lg(x):
    """Returns the base-2 logarithm of x, rounded up"""
    return x.bit_length() - 1

def sub_brackets(x):
    """Reformats 'a[0]' to 'a_0'"""
    return x.replace("[", "_").replace("]", "")

def verso_pin(x):
    """Returns the verso version of a pin"""
    return x.replace("out", "in") if "out" in x else x.replace("in", "out")

def match_nodes(parent, child, index):
    """Attempts to match the ports of two nodes

    Args:
        parent (string): The parent node's module
        child (string): The child node's module
        index (int): The index of the parent's input port
    """
    # If no match is found, will return None
    # Otherwise will return a list of pins to be connected
    # List items will be of the format (parent_pin, child_pin)
    ret = []
    
    # Get the parent and child ports
    parent_ports = modules[parent]["ins"]
    child_ports = modules[child]["outs"]

    # Iterate over all input ports
    for port in parent_ports:
        if port[2+index] == 0:
            continue
        try:
            # Get the matching output port
            matching_port = get_matching_port(port, child_ports)
        except:
            return None
        # Figure out which bits of the port to connect
        offset = 0
        for x in range(index):
            offset += port[2+x]
        # Add the matching pin pairs to the list
        for b in range(port[2+index]):
            pin1 = (port[0], offset+b)
            pin2 = (matching_port[0], b)
            ret.append((pin1, pin2))

    return ret

def get_matching_port(port,other_ports):
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
            "entity": "module {0}(\n\n\t{1}\n\t);\n\n",
            "entity_in": "input",
            "entity_out": "output",
            "entity_port": "{0} {2} {1},",
            "port_range": "[{0}:{1}]",
            "arch": "{1}\nendmodule // {0}\n",
            "inst": "{0} U0(\n{1}\n);",
            "inst_port": ".{0}({1})",
            "slice_markers": lambda x: x,
            "wire_def": "wire {0};",
            "comment_string": "// ",
            "file_extension": ".v"
        },
        "vhdl": {
            "entity": "entity {0} is\n\tport (\n{1}\n);\nend entity;\n\n",
            "entity_in": "in",
            "entity_out": "out",
            "entity_port": "\t\t{1} : {0} std_logic{2};\n",
            "port_range": "_vector({0} downto {1})",
            "arch": ("architecture {0}_arch of {0} is"
                     "\n\tbegin\n{1}\n"
                     "end architecture {0}_arch;\n"),
            "inst": ("\tU0: {0}\n"
                     "\t\tport map (\n{1}\n"
                     "\t\t);"),
            "inst_port": "\t\t{0} => {1}\n",
            "slice_markers":
                lambda x: x.replace("[","(").replace("]",")").replace(":"," downto "),
            "wire_def": "signal {0} : std_logic;",
            "comment_string": "-- ",
            "file_extension": ".vhd"
        }
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
        port_range = syntax["port_range"].format(port[1]-1,0) if port[1]>1 else ""
        next_port = syntax["entity_port"].format(
                                            syntax["entity_in"],
                                            port[0],
                                            port_range
                                            )
        ports_str.append(next_port)
    for port in outs:
        port_range = syntax["port_range"].format(port[1]-1,0) if port[1]>1 else ""
        next_port = syntax["entity_port"].format(
                                            syntax["entity_out"],
                                            port[0],
                                            port_range
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
    return syntax["arch"].format(name, body)

def hdl_inst(name, ports, language="verilog"):
    """Formats an instance declaration

    Args:
        name (str): The name of the instance
        ports (list of (string, string)): A list of ports to be connected
        language (str): The language in which to generate the HDL
    """
    syntax = hdl_syntax[language]
    ports = [(port[0], syntax["slice_markers"](port[1])) for port in ports]
    ports_list = [syntax["inst_port"].format(port[0], port[1]) for port in ports]
    return syntax["inst"].format(name, ",\n".join(ports_list))

def sub_ports(hdl, ports):
    """Substitutes port in an HDL string with corresponding module ports"""
    for port in ports:
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
    return [atoi(c) for c in re.split('(\d+)', text)]

if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
