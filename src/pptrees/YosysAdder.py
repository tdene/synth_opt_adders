from .AdderForest import AdderForest
from .AdderTree import AdderTree


class YosysAdder(AdderForest):
    """Defines a tree that computes binary addition and can be fed into a Yosys plugin"""

    def __init__(
        self,
        width,
        in_ports=None,
        out_ports=None,
        tree_type=AdderTree,
        name="adder",
        alias=None,
        tree_start_points=None,
        radix=2,
    ):
        super().__init__(
            width,
            in_ports=in_ports,
            out_ports=out_ports,
            tree_type=tree_type,
            name=name,
            alias=alias,
            tree_start_points=tree_start_points,
            radix=radix,
        )

    def hdl(
        self,
        out=None,
        mapping="behavioral",
        language="verilog",
        flat=False,
        block_flat=False,
        cell_flat=True,
        merge_mapping=True,
        top_module=None,
        description_string="start of unnamed graph",
    ):

        hdl, module_defs, file_out_hdl = super().hdl(
            out=None,
            mapping=mapping,
            language=language,
            flat=flat,
            block_flat=block_flat,
            cell_flat=cell_flat,
            merge_mapping=merge_mapping,
            module_name=top_module,
            description_string=description_string,
        )
        # If module name is not defined, set it to graph's name
        if top_module is None:
            top_module = self.name

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
""".format(
            top_module
        )

        file_out_hdl = alu_hdl + file_out_hdl

        if out is not None:
            self._write_hdl(file_out_hdl, out, language, mapping, merge_mapping)

        return hdl, module_defs, file_out_hdl


if __name__ == "__main__":
    raise RuntimeError("This file is importable, but not executable")
