// Inverter
module inverter
(
    Y, A
);
    output Y;
    input A;

    sky130_fd_sc_ms__inv_1 inverter(.Y(Y), .A(A));

endmodule

// Buffer
module buffer
(
    Y, A
);
    output Y;
    input A;

    sky130_fd_sc_ms__buf_1 buffer(.X(Y), .A(A));

endmodule

// NAND2
module nand2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_ms__nand2_1 nand2(.Y(Y), .A(A), .B(B));

endmodule

// NOR2
module nor2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_ms__nor2_1 nor2(.Y(Y), .A(A), .B(B));

endmodule

// AND2
module and2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_ms__and2_1 and2(.X(Y), .A(A), .B(B));

endmodule

// OR2
module or2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_ms__or2_1 or2(.X(Y), .A(A), .B(B));

endmodule

// NAND3
module nand3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    sky130_fd_sc_ms__nand3_1 nand3(.Y(Y), .A(A), .B(B), .C(C));

endmodule

// NOR3
module nor3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    sky130_fd_sc_ms__nor3_1 nor3(.Y(Y), .A(A), .B(B), .C(C));

endmodule

// AND3
module and3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    sky130_fd_sc_ms__and3_1 and3(.X(Y), .A(A), .B(B), .C(C));

endmodule

// OR3
module or3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    sky130_fd_sc_ms__or3_1 or3(.X(Y), .A(A), .B(B), .C(C));

endmodule

// NAND4
module nand4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    sky130_fd_sc_ms__nand4_1 nand4(.Y(Y), .A(A), .B(B), .C(C), .D(D));

endmodule

// NOR4
module nor4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    sky130_fd_sc_ms__nor4_1 nor4(.Y(Y), .A(A), .B(B), .C(C), .D(D));

endmodule

// AND4
module and4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    sky130_fd_sc_ms__and4_1 and4(.X(Y), .A(A), .B(B), .C(C), .D(D));

endmodule

// OR4
module or4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    sky130_fd_sc_ms__or4_1 or4(.X(Y), .A(A), .B(B), .C(C), .D(D));

endmodule

// NAND2B
module nand2b
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_ms__nand2b_1 nand2b(.Y(Y), .A_N(A), .B(B));

endmodule

// NOR2B
module nor2b
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_ms__nor2b_1 nor2b(.Y(Y), .A(B), .B_N(A));

endmodule

// AO21
module ao21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    sky130_fd_sc_ms__a21o_1 ao21(.X(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule

// OA21
module oa21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    sky130_fd_sc_ms__o21a_1 oa21(.X(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule

// AOI21
module aoi21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    sky130_fd_sc_ms__a21oi_1 aoi21(.Y(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule

// OAI21
module oai21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    sky130_fd_sc_ms__o21ai_1 oai21(.Y(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule

// AO22
module ao22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    sky130_fd_sc_ms__a22o_1 ao22(.X(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule

// OA22
module oa22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    sky130_fd_sc_ms__o22a_1 oa22(.X(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule

// AOI22
module aoi22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    sky130_fd_sc_ms__a22oi_1 aoi22(.Y(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule

// OAI22
module oai22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    sky130_fd_sc_ms__o22ai_1 oai22(.Y(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule

// XOR2
module xor2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_ms__xor2_1 xor2(.X(Y), .A(A), .B(B));

endmodule

// XNOR2
module xnor2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_ms__xnor2_1 xnor2(.Y(Y), .A(A), .B(B));

endmodule

// MUX2
module mux2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    sky130_fd_sc_ms__mux2_1 mux2(.X(Y), .S(S), .A0(A), .A1(B));

endmodule

// MUX2I
module muxi2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    sky130_fd_sc_ms__mux2i_1 muxi2(.Y(Y), .S(S), .A0(A), .A1(B));

endmodule
