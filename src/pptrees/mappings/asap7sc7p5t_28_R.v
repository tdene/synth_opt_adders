// Inverter
module inverter
(
    Y, A
);
    output Y;
    input A;

    INVx2_ASAP7_75t_R inverter(.Y(Y), .A(A));

endmodule

// Buffer
module buffer
(
    Y, A
);
    output Y;
    input A;

    BUFx2_ASAP7_75t_R buffer(.X(Y), .A(A));

endmodule

// NAND2
module nand2
(
    Y, A, B
);
    output Y;
    input A, B;

    NAND2x2_ASAP7_75t_R nand2(.Y(Y), .A(A), .B(B));

endmodule

// NOR2
module nor2
(
    Y, A, B
);
    output Y;
    input A, B;

    NOR2x2_ASAP7_75t_R nor2(.Y(Y), .A(A), .B(B));

endmodule

// AND2
module and2
(
    Y, A, B
);
    output Y;
    input A, B;

    AND2x2_ASAP7_75t_R and2(.X(Y), .A(A), .B(B));

endmodule

// OR2
module or2
(
    Y, A, B
);
    output Y;
    input A, B;

    OR2x2_ASAP7_75t_R or2(.X(Y), .A(A), .B(B));

endmodule

// NAND3
module nand3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    NAND3x2_ASAP7_75t_R nand3(.Y(Y), .A(A), .B(B), .C(C));

endmodule

// NOR3
module nor3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    NOR3x2_ASAP7_75t_R nor3(.Y(Y), .A(A), .B(B), .C(C));

endmodule

// AND3
module and3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    AND3x2_ASAP7_75t_R and3(.X(Y), .A(A), .B(B), .C(C));

endmodule

// OR3
module or3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    OR3x2_ASAP7_75t_R or3(.X(Y), .A(A), .B(B), .C(C));

endmodule

// NAND4
module nand4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    NAND4x2_ASAP7_75t_R nand4(.Y(Y), .A(A), .B(B), .C(C), .D(D));

endmodule

// NOR4
module nor4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    NOR4x2_ASAP7_75t_R nor4(.Y(Y), .A(A), .B(B), .C(C), .D(D));

endmodule

// AND4
module and4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    AND4x2_ASAP7_75t_R and4(.X(Y), .A(A), .B(B), .C(C), .D(D));

endmodule

// OR4
module or4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    OR4x2_ASAP7_75t_R or4(.X(Y), .A(A), .B(B), .C(C), .D(D));

endmodule

// NAND2B
module nand2b
(
    Y, A, B
);
    output Y;
    input A, B;

    wire tmp;

    INVx2_ASAP7_75t_R inverter(.Y(tmp), .A(A));
    NAND2x2_ASAP7_75t_R nand2(.Y(Y), .A(tmp), .B(B));

endmodule

// NOR2B
module nor2b
(
    Y, A, B
);
    output Y;
    input A, B;

    wire tmp;

    INVx2_ASAP7_75t_R inverter(.Y(tmp), .A(A));
    NAND2x2_ASAP7_75t_R nor2(.Y(Y), .A(tmp), .B(B));

endmodule

// AO21
module ao21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    AO21x2_ASAP7_75t_R ao21(.X(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule

// OA21
module oa21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    OA21x2_ASAP7_75t_R oa21(.X(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule

// AOI21
module aoi21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    AOI21x2_ASAP7_75t_R aoi21(.Y(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule

// OAI21
module oai21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    OAI21x2_ASAP7_75t_R oai21(.X(Y), .A1(A0), .A2(A1), .B1(B0));

endmodule

// AO22
module ao22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    AO22x2_ASAP7_75t_R ao22(.X(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule

// OA22
module oa22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    OA22x2_ASAP7_75t_R oa22(.X(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule

// AOI22
module aoi22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    AOI22x2_ASAP7_75t_R aoi22(.Y(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule

// OAI22
module oai22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    OAI22x2_ASAP7_75t_R oai22(.Y(Y), .A1(A0), .A2(A1), .B1(B0), .B2(B1));

endmodule

// XOR2
module xor2
(
    Y, A, B
);
    output Y;
    input A, B;

    XOR2x2_ASAP7_75t_R xor2(.X(Y), .A(A), .B(B));

endmodule

// XNOR2
module xnor2
(
    Y, A, B
);
    output Y;
    input A, B;

    XNOR2x2_ASAP7_75t_R xnor2(.Y(Y), .A(A), .B(B));

endmodule

// MUX2
module mux2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    wire tmp, tmp2;

    INVx2_ASAP7_75t_R inverter(.Y(tmp), .A(S));
    AOI22x2_ASAP7_75t_R aoi22(.Y(tmp2), .A1(S), .A2(A1), .B1(tmp), .B2(B1));
    INVx2_ASAP7_75t_R inverter(.Y(Y), .A(tmp2));

endmodule

// MUX2I
module muxi2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    wire tmp;

    INVx2_ASAP7_75t_R inverter(.Y(tmp), .A(S));
    AOI22x2_ASAP7_75t_R aoi22(.Y(Y), .A1(S), .A2(A1), .B1(tmp), .B2(B1));

endmodule
