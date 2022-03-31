from .modules import modules
from .adder_tree import adder_tree
from .prefix_graph import prefix_node as node
import pathlib
import shutil
import importlib

class yosys_alu(adder_tree):
    """Class that generates parallel prefix adder trees"""

    def __init__(self,width,network="ripple"):
        """Initializes a parallel prefix tree adder to be used by a Yosys $alu mapping pass

        Refer to the adder_tree's docstring for a full description.
        """
        super().__init__(width,network)

    def yosys_map(self,out=None,mapping="behavioral"):
        """Writes out map files used to translate the HDL"""

        # Check that output path is valid
        if out is None:
            raise ValueError("output path must be specified")
        outdir = pathlib.Path(out).resolve()
        if not outdir.exists():
            raise FileNotFoundError("desired path for hdl map files is invalid")

        file_suffix = ".v"

        # Locate mapping file and check its existence
        with importlib.resources.path("pptrees","mappings") as pkg_map_dir:
            pkg_map_file = pkg_map_dir / (mapping+'_map'+file_suffix)
            local_map_file = outdir / (mapping+'_map'+file_suffix)

            if not pkg_map_file.is_file():
                raise ValueError("unsupported mapping requested")

            # Copy mapping file from package to local directory
            shutil.copy(pkg_map_file,local_map_file)

        # Create file that contains all module definitions
        module_def_text = "".join([modules[x]['verilog'] for x in modules])

        # Write to file
        with open(outdir / "modules.v",'w') as f:
            print(module_def_text,file=f)

    def hdl(self,out=None,mapping="behavioral",top_module="adder"):
        """Generates HDL that can be used by Yosys $alu mapping pass"""

        # Check that output path is valid
        if out is not None:
            outdir = pathlib.Path(out).resolve().parent
            if not outdir.exists():
                raise FileNotFoundError("desired path for hdl output is invalid")

        # Set language-specific variables
        end_string = "\nendmodule\n"
        comment_string = "\n// start of tree row {0}\n"
        file_suffix = ".v"

        # Write out a module fitting the Yosys $alu
        alu_hdl = """(* techmap_celltype = "$alu" *)
module _{0}_alu (A, B, CI, BI, X, Y, CO);
    parameter A_SIGNED = 0;
    parameter B_SIGNED = 0;
    parameter A_WIDTH = 1;
    parameter B_WIDTH = 1;
    parameter Y_WIDTH = 1;

    (* force_downto *)
    input [A_WIDTH-1:0] A;
    (* force_downto *)
    input [B_WIDTH-1:0] B;
    (* force_downto *)
    output [Y_WIDTH-1:0] X, Y;

    input CI, BI;
    (* force_downto *)
    output [Y_WIDTH-1:0] CO;

    (* force_downto *)
    wire [Y_WIDTH-1:0] AA = A_buf;
    (* force_downto *)
    wire [Y_WIDTH-1:0] BB = BI ? ~B_buf : B_buf;

    (* force_downto *)
    wire [Y_WIDTH-1:0] A_buf, B_buf;
    \$pos #(.A_SIGNED(A_SIGNED), .A_WIDTH(A_WIDTH), .Y_WIDTH(Y_WIDTH)) A_conv (.A(A), .Y(A_buf));
    \$pos #(.A_SIGNED(B_SIGNED), .A_WIDTH(B_WIDTH), .Y_WIDTH(Y_WIDTH)) B_conv (.A(B), .Y(B_buf));

    assign X = 0;
    assign CO[Y_WIDTH-2:0] = 0;
    {0} U1(.cout(CO[Y_WIDTH-1]), .sum(Y), .a(AA), .b(BB), .cin(CI));
endmodule
""".format(top_module)

        # Pull in HDL preamble, as defined by child class 
        preamble_hdl, preamble_defs = self._hdl_preamble(language='verilog',top_module=top_module)

        # Pull in the body of the HDL
        body_hdl, body_defs = self._hdl_body(language='verilog',comment_string=comment_string)

        # Pull in HDL of blocks
        block_hdl, block_defs = self._hdl_blocks(language='verilog')

        hdl = preamble_hdl + body_hdl + block_hdl + [end_string]

        # Format into string
        hdl = alu_hdl + '\n'.join(hdl)

        # Write to file
        if out is not None:
            
            with open(out,'w') as f:
                print(hdl,file=f)

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
