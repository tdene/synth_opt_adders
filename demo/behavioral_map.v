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

    assign Y = A;

endmodule

// NAND2
module nand2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(A&B);

endmodule

// NOR2
module nor2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(A|B);

endmodule

// AND2
module and2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = A&B;

endmodule

// OR2
module or2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = A|B;

endmodule

// NAND3
module nand3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    assign Y = ~(A&B&C);

endmodule

// NOR3
module nor3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    assign Y = ~(A|B|C);

endmodule

// AND3
module and3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    assign Y = A&B&C;

endmodule

// OR3
module or3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    assign Y = A|B|C;

endmodule

// NAND4
module nand4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    assign Y = ~(A&B&C&D);

endmodule

// NOR4
module nor4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    assign Y = ~(A|B|C|D);

endmodule

// AND4
module and4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    assign Y = A&B&C&D;

endmodule

// OR4
module or4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    assign Y = A|B|C|D;

endmodule

// NAND2B
module nand2b
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(~A&B);

endmodule

// NOR2B
module nor2b
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(~A|B);

endmodule

// AO21
module ao21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    assign Y = (A0&A1)|B0;

endmodule

// OA21
module oa21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    assign Y = (A0|A1)&B0;

endmodule

// AOI21
module aoi21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    assign Y = ~((A0&A1)|B0);

endmodule

// OAI21
module oai21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    assign Y = ~((A0|A1)&B0);

endmodule

// AO22
module ao22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    assign Y = (A0&A1)|(B0&B1);

endmodule

// OA22
module oa22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    assign Y = (A0|A1)&(B0|B1);

endmodule

// AOI22
module aoi22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    assign Y = ~((A0&A1)|(B0&B1));

endmodule

// OAI22
module oai22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    assign Y = ~((A0|A1)&(B0|B1));

endmodule

// XOR2
module xor2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = A^B;

endmodule

// XNOR2
module xnor2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(A^B);

endmodule

// MUX2
module mux2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    assign Y = S ? B : A;

endmodule

// MUX2I
module muxi2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    assign Y = ~(S ? B : A);

endmodule
