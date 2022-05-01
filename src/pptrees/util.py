#!/bin/python3


def lg(x):
    """Returns the base-2 logarithm of x, rounded up"""
    return x.bit_length() - 1

def sub_brackets(x):
    """Reformats 'a[0]' to 'a_0'"""
    return x.replace("[", "_").replace("]", "")

def verso_pin(x):
    """Returns the verso version of a pin"""
    return x.replace("out", "in") if "out" in x else x.replace("in", "out")

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
            "entity": "module {0}(\n{1}\n);\n\n",
            "entity_in": "input",
            "entity_out": "output",
            "entity_port": "{0} {2} {1};",
            "port_range": "[{0}:{1}]",
            "arch": "{1}\nendmodule // {0}",
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
                     "end architecture {0}_arch;"),
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
    ports_str = ""
    for port in ins:
        port_range = syntax["port_range"].format(port[1],0) if port[1] else ""
        ports_str += syntax["entity_port"].format(
                        syntax["entity_in"],
                        port[0],
                        port_range)
    for port in outs:
        port_range = syntax["port_range"].format(port[1],0) if port[1] else ""
        ports_str += syntax["entity_port"].format(
                        syntax["entity_out"],
                        port[0],
                        port_range)
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
    ports = [(port[0], syntax.slice_markers(port[1])) for port in ports]
    ports_list = [syntax["inst_port"].format(port[0], port[1]) for port in ports]
    return syntax["inst"].format(name, ",\n".join(ports_list))


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
