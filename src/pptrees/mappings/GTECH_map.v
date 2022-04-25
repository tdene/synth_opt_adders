// Inverter
module inverter
(
    Y, A
);
    output Y;
    input A;

    assign Y = ~A;

endmodule

// Buffer
module buffer
(
    Y, A
);
    output Y;
    input A;

    GTECH_BUF buffer(.A(A), .Z(Y));

endmodule

// NAND2
module nand2
(
    Y, A, B
);
    output Y;
    input A, B;

    GTECH_NAND2 nand2(.A(A), .B(B), .Z(Y));

endmodule

// NOR2
module nor2
(
    Y, A, B
);
    output Y;
    input A, B;

    GTECH_NOR2 nor2(.A(A), .B(B), .Z(Y));

endmodule

// AND2
module and2
(
    Y, A, B
);
    output Y;
    input A, B;

    GTECH_AND2 and2(.A(A), .B(B), .Z(Y));

endmodule

// OR2
module or2
(
    Y, A, B
);
    output Y;
    input A, B;

    GTECH_OR2 or2(.A(A), .B(B), .Z(Y));

endmodule

// NAND3
module nand3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    GTECH_NAND3 nand3(.A(A), .B(B), .C(C), .Z(Y));

endmodule

// NOR3
module nor3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    GTECH_NOR3 nor3(.A(A), .B(B), .C(C), .Z(Y));

endmodule

// AND3
module and3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    GTECH_AND3 and3(.A(A), .B(B), .C(C), .Z(Y));

endmodule

// OR3
module or3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    GTECH_OR3 or3(.A(A), .B(B), .C(C), .Z(Y));

endmodule

// NAND4
module nand4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    GTECH_NAND4 nand4(.A(A), .B(B), .C(C), .D(D), .Z(Y));

endmodule

// NOR4
module nor4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    GTECH_NOR4 nor4(.A(A), .B(B), .C(C), .D(D), .Z(Y));

endmodule

// AND4
module and4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    GTECH_AND4 and4(.A(A), .B(B), .C(C), .D(D), .Z(Y));

endmodule

// OR4
module or4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    GTECH_OR4 or4(.A(A), .B(B), .C(C), .D(D), .Z(Y));

endmodule

// NAND2B
module nand2b
(
    Y, A, B
);
    output Y;
    input A, B;

    GTECH_AND_NOT nand2b(.A(B), .B(A), .Z(Y));

endmodule

// NOR2B
module nor2b
(
    Y, A, B
);
    output Y;
    input A, B;

    GTECH_OR_NOT nor2b(.A(B), .B(A), .Z(Y));

endmodule

// AO21
module ao21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    GTECH_AO21 ao21(.A(A0), .B(A1), .C(B0), .Z(Y));

endmodule

// OA21
module oa21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    GTECH_OA21 oa21(.A(A0), .B(A1), .C(B0), .Z(Y));

endmodule

// AOI21
module aoi21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    GTECH_AOI21 aoi21(.A(A0), .B(A1), .C(B0), .Z(Y));

endmodule

// OAI21
module oai21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    GTECH_OAI21 oai21(.A(A0), .B(A1), .C(B0), .Z(Y));

endmodule

// AO22
module ao22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    GTECH_AO22 ao22(.A(A0), .B(A1), .C(B0), .D(B1), .Z(Y));

endmodule

// OA22
module oa22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    GTECH_OA22 oa22(.A(A0), .B(A1), .C(B0), .D(B1), .Z(Y));

endmodule

// AOI22
module aoi22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    GTECH_AOI22 aoi22(.A(A0), .B(A1), .C(B0), .D(B1), .Z(Y));

endmodule

// OAI22
module oai22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    GTECH_OAI22 oai22(.A(A0), .B(A1), .C(B0), .D(B1), .Z(Y));

endmodule

// XOR2
module xor2
(
    Y, A, B
);
    output Y;
    input A, B;

    GTECH_XOR2 xor2(.A(A), .B(B), .Z(Y));

endmodule

// XNOR2
module xnor2
(
    Y, A, B
);
    output Y;
    input A, B;

    GTECH_XNOR2 xnor2(.A(A), .B(B), .Z(Y));

endmodule

// MUX2
module mux2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    GTECH_MUX2 mux2(.A(A), .B(B), .S(S), .Z(Y));

endmodule

// MUX2I
module muxi2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    GTECH_MUXI2 muxi2(.A(A), .B(B), .S(S), .Z(Y));

endmodule
