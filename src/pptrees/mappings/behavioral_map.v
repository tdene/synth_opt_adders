// Inverter
module inverter
(
    Y, A
);
    output Y;
    input A;

    assign Y = ~A;

endmodule: inverter

// Buffer
module buffer
(
    Y, A
);
    output Y;
    input A;

    assign Y = A;

endmodule: buffer

// NAND2
module nand2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(A&B);

endmodule: nand2

// NOR2
module nor2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(A|B);

endmodule: nor2

// AND2
module and2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = A&B;

endmodule: and2

// OR2
module or2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = A|B;

endmodule: or2

// NAND3
module nand3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    assign Y = ~(A&B&C);

endmodule: nand3

// NOR3
module nor3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    assign Y = ~(A|B|C);

endmodule: nor3

// AND3
module and3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    assign Y = A&B&C;

endmodule: and3

// OR3
module or3
(
    Y, A, B, C
);
    output Y;
    input A, B, C;

    assign Y = A|B|C;

endmodule: or3

// NAND4
module nand4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    assign Y = ~(A&B&C&D);

endmodule: nand4

// NOR4
module nor4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    assign Y = ~(A|B|C|D);

endmodule: nor4

// AND4
module and4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    assign Y = A&B&C&D;

endmodule: and4

// OR4
module or4
(
    Y, A, B, C, D
);
    output Y;
    input A, B, C, D;

    assign Y = A|B|C|D;

endmodule: or4

// NAND2B
module nand2b
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(~A&B);

endmodule: nand2b

// NOR2B
module nor2b
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(~A|B);

endmodule: nor2b

// AO21
module ao21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    assign Y = (A0&A1)|B0;

endmodule: ao21

// OA21
module oa21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    assign Y = (A0|A1)&B0;

endmodule: oa21

// AOI21
module aoi21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    assign Y = ~((A0&A1)|B0);

endmodule: aoi21

// OAI21
module oai21
(
    Y, A0, A1, B0
);
    output Y;
    input A0, A1, B0;

    assign Y = ~((A0|A1)&B0);

endmodule: oai21

// AO22
module ao22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    assign Y = (A0&A1)|(B0&B1);

endmodule: ao22

// OA22
module oa22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    assign Y = (A0|A1)&(B0|B1);

endmodule: oa22

// AOI22
module aoi22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    assign Y = ~((A0&A1)|(B0&B1));

endmodule: aoi22

// OAI22
module oai22
(
    Y, A0, A1, B0, B1
);
    output Y;
    input A0, A1, B0, B1;

    assign Y = ~((A0|A1)&(B0|B1));

endmodule: oai22

// XOR2
module xor2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = A^B;

endmodule: xor2

// XNOR2
module xnor2
(
    Y, A, B
);
    output Y;
    input A, B;

    assign Y = ~(A^B);

endmodule: xnor2

// MUX2
module mux2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    assign Y = S ? B : A;

endmodule: mux2

// MUX2I
module muxi2
(
    Y, S, A, B
);
    output Y;
    input S, A, B;

    assign Y = ~(S ? B : A);

endmodule: muxi2
