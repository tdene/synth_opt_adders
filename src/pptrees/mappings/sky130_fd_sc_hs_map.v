// Inverter
module inverter
(
    Y, A
);
    output Y;
    input A;

    sky130_fd_sc_hs__inv_1 inverter(.Y(Y), .A(A));

endmodule : inverter

// Buffer
module buffer
(
    Y, A
);
    output Y;
    input A;

    sky130_fd_sc_hs__buf_1 buffer(.X(Y), .A(A));

endmodule: buffer

// NAND2
module nand2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_hs__nand2_1 nand2(.Y(Y), .A(A), .B(B));

endmodule: nand2

// NOR2
module nor2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_hs__nor2_1 nor2(.Y(Y), .A(A), .B(B));

endmodule: nor2

// AND2
module and2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_hs__and2_1 and2(.X(Y), .A(A), .B(B));

endmodule: and2

// OR2
module or2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_hs__or2_1 or2(.X(Y), .A(A), .B(B));

endmodule: or2

// NAND3
module nand3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    sky130_fd_sc_hs__nand3_1 nand3(.Y(Y), .A(A), .B(B), .C(C));

endmodule: nand3

// NOR3
module nor3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    sky130_fd_sc_hs__nor3_1 nor3(.Y(Y), .A(A), .B(B), .C(C));

endmodule: nor3

// AND3
module and3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    sky130_fd_sc_hs__and3_1 and3(.X(Y), .A(A), .B(B), .C(C));

endmodule: and3

// OR3
module or3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    sky130_fd_sc_hs__or3_1 or3(.X(Y), .A(A), .B(B), .C(C));

endmodule: or3

// NAND4
module nand4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    sky130_fd_sc_hs__nand4_1 nand4(.Y(Y), .A(A), .B(B), .C(C), .D(D));

endmodule: nand4

// NOR4
module nor4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    sky130_fd_sc_hs__nor4_1 nor4(.Y(Y), .A(A), .B(B), .C(C), .D(D));

endmodule: nor4

// AND4
module and4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    sky130_fd_sc_hs__and4_1 and4(.X(Y), .A(A), .B(B), .C(C), .D(D));

endmodule: and4

// OR4
module or4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    sky130_fd_sc_hs__or4_1 or4(.X(Y), .A(A), .B(B), .C(C), .D(D));

endmodule: or4

// NAND2B
module nand2b
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_hs__nand2b_1 nand2b(.Y(Y), .A_N(A), .B(B));

endmodule: nand2b

// NOR2B
module nor2b
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_hs__nor2b_1 nor2b(.Y(Y), .A(B), .B_N(A));

endmodule: nor2b

// AO21
module ao21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    sky130_fd_sc_hs__a21o_1 ao21(.X(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule: ao21

// OA21
module oa21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    sky130_fd_sc_hs__o21a_1 oa21(.X(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule: oa21

// AOI21
module aoi21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    sky130_fd_sc_hs__a21oi_1 aoi21(.Y(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule: aoi21

// OAI21
module oai21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    sky130_fd_sc_hs__o21ai_1 oai21(.X(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule: oai21

// AO22
module ao22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    sky130_fd_sc_hs__a22o_1 ao22(.X(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule: ao22

// OA22
module oa22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    sky130_fd_sc_hs__o22a_1 oa22(.X(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule: oa22

// AOI22
module aoi22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    sky130_fd_sc_hs__a22oi_1 aoi22(.Y(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule: aoi22

// OAI22
module oai22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    sky130_fd_sc_hs__o22ai_1 oai22(.Y(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule: oai22

// XOR2
module xor2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_hs__xor2_1 xor2(.X(Y), .A(A), .B(B));

endmodule: xor2

// XNOR2
module xnor2
(
    Y, A, B
);
    output Y;
    input A, B;

    sky130_fd_sc_hs__xnor2_1 xnor2(.Y(Y), .A(A), .B(B));

endmodule: xnor2

// MUX2
module mux2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    sky130_fd_sc_hs__mux2_1 mux2(.X(Y), .S(S), .A0(A), .A1(B));

endmodule: mux2

// MUX2I
module muxi2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    sky130_fd_sc_hs__mux2i_1 muxi2(.Y(Y), .S(S), .A0(A), .A1(B));

endmodule: muxi2
