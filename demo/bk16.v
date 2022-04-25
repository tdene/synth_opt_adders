module adder(cout, sum, a, b, cin);

	input [15:0] a, b;
	input cin;
	output [15:0] sum;
	output cout;

	wire p14, p13, p6, p12, p2, g8, p5, g5, p3, g9, p1, p9, p0, g_lsb, g12, p_lsb, g6, g1, g13, g11, p10, g7, g2, g0, g14, p7, p8, g10, g3, g4, p11, p4;
	wire n1025, n1028, n1026, n1029, n1031, n1032, n1034, n1036, n1037, n1039, n1042, n1041, n1044, n1047, n1049, n1051, n1052, n1054, n1057, n1059, n1061, n1062, n48, n49, n50, n51, n52, n54, n55, n1072, n57, n58, n59, n60, n61, n62, n1086, n65, n66, n69, n70, n71, n72, n73, n74, n1097, n77, n78, n81, n82, n83, n84, n85, n86, n1110, n89, n90, n93, n94, n95, n96, n97, n98, n99, n100, n1122, n102, n103, n105, n106, n108, n109, n111, n112, n113, n114, n115, n116, n117, n118, n119, n120, n1137, n123, n124, n127, n128, n1151, n131, n132, n135, n136, n137, n139, n138, n141, n142, n143, n144, n145, n146, n147, n148, n150, n151, n153, n154, n156, n157, n159, n160, n162, n163, n165, n166, n168, n169, n171, n172, n173, n174, n175, n177, n178, n179, n181, n183, n185, n186, n187, n188, n189, n190, n191, n192, n194, n193, n715, n725, n1162, n732, n740, n743, n746, n749, n751, n754, n756, n759, n761, n763, n765, n767, n769, n771, n773, n775, n784, n791, n802, n813, n832, n846, n859, n862, n863, n865, n866, n869, n871, n872, n874, n877, n879, n881, n882, n884, n887, n889, n892, n894, n897, n899, n901, n902, n912, n925, n935, n945, n956, n967, n975, n990, n1005, n1019, n1022, n1023;

// start of pre-processing logic

	ppa_first_pre ppa_first_pre_0_0 ( .cin( {cin} ), .pout( {p_lsb} ), .gout( {g_lsb} ) );
	ppa_pre ppa_pre_1_0 ( .a_in( {a[0]} ), .b_in( {b[0]} ), .pout( {p0} ), .gout( {g0} ) );
	ppa_pre ppa_pre_2_0 ( .a_in( {a[1]} ), .b_in( {b[1]} ), .pout( {p1} ), .gout( {g1} ) );
	ppa_pre ppa_pre_3_0 ( .a_in( {a[2]} ), .b_in( {b[2]} ), .pout( {p2} ), .gout( {g2} ) );
	ppa_pre ppa_pre_4_0 ( .a_in( {a[3]} ), .b_in( {b[3]} ), .pout( {p3} ), .gout( {g3} ) );
	ppa_pre ppa_pre_5_0 ( .a_in( {a[4]} ), .b_in( {b[4]} ), .pout( {p4} ), .gout( {g4} ) );
	ppa_pre ppa_pre_6_0 ( .a_in( {a[5]} ), .b_in( {b[5]} ), .pout( {p5} ), .gout( {g5} ) );
	ppa_pre ppa_pre_7_0 ( .a_in( {a[6]} ), .b_in( {b[6]} ), .pout( {p6} ), .gout( {g6} ) );
	ppa_pre ppa_pre_8_0 ( .a_in( {a[7]} ), .b_in( {b[7]} ), .pout( {p7} ), .gout( {g7} ) );
	ppa_pre ppa_pre_9_0 ( .a_in( {a[8]} ), .b_in( {b[8]} ), .pout( {p8} ), .gout( {g8} ) );
	ppa_pre ppa_pre_10_0 ( .a_in( {a[9]} ), .b_in( {b[9]} ), .pout( {p9} ), .gout( {g9} ) );
	ppa_pre ppa_pre_11_0 ( .a_in( {a[10]} ), .b_in( {b[10]} ), .pout( {p10} ), .gout( {g10} ) );
	ppa_pre ppa_pre_12_0 ( .a_in( {a[11]} ), .b_in( {b[11]} ), .pout( {p11} ), .gout( {g11} ) );
	ppa_pre ppa_pre_13_0 ( .a_in( {a[12]} ), .b_in( {b[12]} ), .pout( {p12} ), .gout( {g12} ) );
	ppa_pre ppa_pre_14_0 ( .a_in( {a[13]} ), .b_in( {b[13]} ), .pout( {p13} ), .gout( {g13} ) );
	ppa_pre ppa_pre_15_0 ( .a_in( {a[14]} ), .b_in( {b[14]} ), .pout( {p14} ), .gout( {g14} ) );

// start of post-processing logic

	ppa_post ppa_post_0_8 ( .gin( {n1023} ), .pin( {p0} ), .sum( {sum[0]} ) );
	ppa_post ppa_post_1_8 ( .gin( {n1026} ), .pin( {p1} ), .sum( {sum[1]} ) );
	ppa_post ppa_post_2_8 ( .gin( {n1029} ), .pin( {p2} ), .sum( {sum[2]} ) );
	ppa_post ppa_post_3_8 ( .gin( {n1032} ), .pin( {p3} ), .sum( {sum[3]} ) );
	ppa_post ppa_post_4_8 ( .gin( {n1034} ), .pin( {p4} ), .sum( {sum[4]} ) );
	ppa_post ppa_post_5_8 ( .gin( {n1037} ), .pin( {p5} ), .sum( {sum[5]} ) );
	ppa_post ppa_post_6_8 ( .gin( {n1039} ), .pin( {p6} ), .sum( {sum[6]} ) );
	ppa_post ppa_post_7_8 ( .gin( {n1042} ), .pin( {p7} ), .sum( {sum[7]} ) );
	ppa_post ppa_post_8_8 ( .gin( {n1044} ), .pin( {p8} ), .sum( {sum[8]} ) );
	ppa_post ppa_post_9_8 ( .gin( {n1047} ), .pin( {p9} ), .sum( {sum[9]} ) );
	ppa_post ppa_post_10_8 ( .gin( {n1049} ), .pin( {p10} ), .sum( {sum[10]} ) );
	ppa_post ppa_post_11_8 ( .gin( {n1052} ), .pin( {p11} ), .sum( {sum[11]} ) );
	ppa_post ppa_post_12_8 ( .gin( {n1054} ), .pin( {p12} ), .sum( {sum[12]} ) );
	ppa_post ppa_post_13_8 ( .gin( {n1057} ), .pin( {p13} ), .sum( {sum[13]} ) );
	ppa_post ppa_post_14_8 ( .gin( {n1059} ), .pin( {p14} ), .sum( {sum[14]} ) );
	ppa_post ppa_post_15_8 ( .gin( {n1062} ), .pin( {p15} ), .sum( {sum[15]} ) );

// start of custom pre/post logic

	ppa_pre ppa_pre_cout ( .a_in( a[15] ), .b_in( b[15] ), .pout ( p15 ), .gout ( g15 ) );
	ppa_grey ppa_grey_cout ( .gin ( {g15,n1062} ), .pin ( p15 ), .gout ( cout ) );

// start of tree row 1

	assign n49 = p_lsb;
	assign n48 = g_lsb;
	assign n52 = p1;
	assign n51 = g1;
	ppa_black ppa_black_3_1 ( .gin( {g2,g1} ), .pin( {p2,p1} ), .gout( {n54} ), .pout( {n55} ) );
	assign n58 = p3;
	assign n57 = g3;
	ppa_black ppa_black_5_1 ( .gin( {g4,g3} ), .pin( {p4,p3} ), .gout( {n59} ), .pout( {n60} ) );
	assign n62 = p5;
	assign n61 = g5;
	ppa_black ppa_black_7_1 ( .gin( {g6,g5} ), .pin( {p6,p5} ), .gout( {n65} ), .pout( {n66} ) );
	assign n70 = p7;
	assign n69 = g7;
	ppa_black ppa_black_9_1 ( .gin( {g8,g7} ), .pin( {p8,p7} ), .gout( {n71} ), .pout( {n72} ) );
	assign n74 = p9;
	assign n73 = g9;
	ppa_black ppa_black_11_1 ( .gin( {g10,g9} ), .pin( {p10,p9} ), .gout( {n77} ), .pout( {n78} ) );
	assign n82 = p11;
	assign n81 = g11;
	ppa_black ppa_black_13_1 ( .gin( {g12,g11} ), .pin( {p12,p11} ), .gout( {n83} ), .pout( {n84} ) );
	assign n86 = p13;
	assign n85 = g13;
	ppa_black ppa_black_15_1 ( .gin( {g14,g13} ), .pin( {p14,p13} ), .gout( {n89} ), .pout( {n90} ) );

// start of tree row 2

	assign n94 = n49;
	assign n93 = n48;
	assign n96 = n0;
	assign n95 = n50;
	assign n715 = n52;
	assign n97 = n51;
	assign n100 = n58;
	assign n99 = n57;
	assign n103 = n60;
	assign n102 = n59;
	assign n106 = n62;
	assign n105 = n61;
	ppa_black ppa_black_7_2 ( .gin( {n65,n59} ), .pin( {n66,n60} ), .gout( {n108} ), .pout( {n109} ) );
	assign n112 = n70;
	assign n111 = n69;
	assign n114 = n72;
	assign n113 = n71;
	assign n116 = n74;
	assign n115 = n73;
	ppa_black ppa_black_11_2 ( .gin( {n77,n71} ), .pin( {n78,n72} ), .gout( {n117} ), .pout( {n118} ) );
	assign n120 = n82;
	assign n119 = n81;
	assign n124 = n84;
	assign n123 = n83;
	assign n128 = n86;
	assign n127 = n85;
	ppa_black ppa_black_15_2 ( .gin( {n89,n83} ), .pin( {n90,n84} ), .gout( {n131} ), .pout( {n132} ) );

// start of tree row 3

	assign n136 = n94;
	assign n135 = n93;
	assign n138 = n96;
	assign n137 = n95;
	assign n832 = n715;
	assign n139 = n97;
	assign n142 = n0;
	assign n141 = n98;
	assign n725 = n100;
	assign n143 = n99;
	assign n956 = n103;
	assign n144 = n102;
	assign n732 = n106;
	assign n145 = n105;
	assign n148 = n112;
	assign n147 = n111;
	assign n151 = n114;
	assign n150 = n113;
	assign n154 = n116;
	assign n153 = n115;
	assign n157 = n118;
	assign n156 = n117;
	assign n160 = n120;
	assign n159 = n119;
	assign n163 = n124;
	assign n162 = n123;
	assign n166 = n128;
	assign n165 = n127;
	ppa_black ppa_black_15_3 ( .gin( {n131,n117} ), .pin( {n132,n118} ), .gout( {n168} ), .pout( {n169} ) );

// start of tree row 4

	assign n172 = n136;
	assign n171 = n135;
	ppa_buffer ppa_buffer_1_4 ( .gin( {n137} ), .pin( {n138} ), .gout( {n173} ), .pout( {n174} ) );
	assign n990 = n832;
	assign n175 = n139;
	ppa_buffer ppa_buffer_3_4 ( .gin( {n141} ), .pin( {n142} ), .gout( {n177} ), .pout( {n178} ) );
	assign n846 = n725;
	assign n179 = n143;
	assign n1122 = n956;
	assign n181 = n144;
	assign n859 = n732;
	assign n183 = n145;
	assign n784 = n148;
	assign n187 = n147;
	assign n967 = n151;
	assign n188 = n150;
	assign n791 = n154;
	assign n189 = n153;
	assign n1162 = n157;
	assign n190 = n156;
	assign n802 = n160;
	assign n191 = n159;
	assign n975 = n163;
	assign n192 = n162;
	assign n813 = n166;
	assign n193 = n165;
	ppa_grey ppa_grey_15_4 ( .gin( {n168,n146} ), .pin( {n169} ), .gout( {n194} ) );

// start of tree row 5

	assign n862 = n172;
	assign n740 = n171;
	assign n865 = n174;
	assign n743 = n173;
	ppa_grey ppa_grey_2_5 ( .gin( {n175,n173} ), .pin( {n990} ), .gout( {n746} ) );
	ppa_buffer ppa_buffer_3_5 ( .gin( {n177} ), .pin( {n178} ), .gout( {n749} ), .pout( {n871} ) );
	assign n1005 = n846;
	assign n751 = n179;
	ppa_grey ppa_grey_5_5 ( .gin( {n181,n177} ), .pin( {n1122} ), .gout( {n754} ) );
	assign n1019 = n859;
	assign n756 = n183;
	ppa_buffer ppa_buffer_7_5 ( .gin( {n185} ), .pin( {n186} ), .gout( {n759} ), .pout( {n881} ) );
	assign n912 = n784;
	assign n761 = n187;
	assign n1137 = n967;
	assign n763 = n188;
	assign n925 = n791;
	assign n765 = n189;
	assign n935 = n802;
	assign n769 = n191;
	assign n1151 = n975;
	assign n771 = n192;
	assign n945 = n813;
	assign n773 = n193;
	assign n901 = n0;
	assign n775 = n194;

// start of tree row 6

	assign n1022 = n862;
	assign n863 = n740;
	assign n1025 = n865;
	assign n866 = n743;
	assign n1028 = n868;
	assign n869 = n746;
	assign n1031 = n871;
	assign n872 = n749;
	ppa_grey ppa_grey_4_6 ( .gin( {n751,n749} ), .pin( {n1005} ), .gout( {n874} ) );
	assign n1036 = n876;
	assign n877 = n754;
	ppa_grey ppa_grey_6_6 ( .gin( {n756,n754} ), .pin( {n1019} ), .gout( {n879} ) );
	ppa_buffer ppa_buffer_7_6 ( .gin( {n759} ), .pin( {n881} ), .gout( {n882} ), .pout( {n1041} ) );
	assign n1072 = n912;
	assign n884 = n761;
	ppa_grey ppa_grey_9_6 ( .gin( {n763,n759} ), .pin( {n1137} ), .gout( {n887} ) );
	assign n1086 = n925;
	assign n889 = n765;
	ppa_buffer ppa_buffer_11_6 ( .gin( {n767} ), .pin( {n891} ), .gout( {n892} ), .pout( {n1051} ) );
	assign n1097 = n935;
	assign n894 = n769;
	assign n1110 = n945;
	assign n899 = n773;
	assign n1061 = n901;
	assign n902 = n775;

// start of tree row 7

	assign n0 = n1022;
	assign n1023 = n863;
	assign n0 = n1025;
	assign n1026 = n866;
	assign n0 = n1028;
	assign n1029 = n869;
	assign n0 = n1031;
	assign n1032 = n872;
	assign n0 = n0;
	assign n1034 = n874;
	assign n0 = n1036;
	assign n1037 = n877;
	assign n0 = n0;
	assign n1039 = n879;
	assign n0 = n1041;
	assign n1042 = n882;
	ppa_grey ppa_grey_8_7 ( .gin( {n884,n882} ), .pin( {n1072} ), .gout( {n1044} ) );
	assign n0 = n1046;
	assign n1047 = n887;
	ppa_grey ppa_grey_10_7 ( .gin( {n889,n887} ), .pin( {n1086} ), .gout( {n1049} ) );
	assign n0 = n1051;
	assign n1052 = n892;
	ppa_grey ppa_grey_12_7 ( .gin( {n894,n892} ), .pin( {n1097} ), .gout( {n1054} ) );
	assign n0 = n1056;
	assign n1057 = n897;
	assign n0 = n1061;
	assign n1062 = n902;
	block_1 block_1_instance ( .n109 ( n109 ), .n108 ( n108 ), .n1162 ( n1162 ), .n1151 ( n1151 ), .n771 ( n771 ), .n767 ( n767 ), .n1059 ( n1059 ), .n98 ( n98 ), .n54 ( n54 ), .n190 ( n190 ), .n185 ( n185 ), .sum_14 ( sum[14] ), .n55 ( n55 ), .p14 ( p14 ), .n0 ( n0 ), .n50 ( n50 ), .p0 ( p0 ), .cin ( cin ), .n897 ( n897 ), .g0 ( g0 ), .g_lsb ( g_lsb ), .p_lsb ( p_lsb ), .n1110 ( n1110 ), .n899 ( n899 ), .n186 ( n186 ), .n146 ( n146 ) );


endmodule

module ppa_black(gin, pin, gout, pout);

	input [1:0] gin, pin;
	output gout, pout;

	and2 U1(pout,pin[1],pin[0]);
	ao21 U2(gout,gin[0],pin[1],gin[1]);

endmodule

module ppa_grey(gin, pin, gout);

	input[1:0] gin;
	input pin;
	output gout;

	ao21 U1(gout,gin[0],pin,gin[1]);

endmodule

module ppa_pre(a_in, b_in, pout, gout);

	input a_in, b_in;
	output pout, gout;

	xor2 U1(pout,a_in,b_in);
	and2 U2(gout,a_in,b_in);

endmodule

module ppa_first_pre(cin, pout, gout);

	input cin;
	output pout, gout;

	assign pout=1'b0;
	assign gout=cin;

endmodule

module ppa_post(pin, gin, sum);

	input pin, gin;
	output sum;

	xor2 U1(sum,pin,gin);

endmodule

module ppa_buffer(pin, gin, pout, gout);

	input pin, gin;
	output pout, gout;

	buffer U1(pout,pin);
	buffer U2(gout,gin);

endmodule

module block_1( n109, n108, n1162, n1151, n771, n767, n1059, n98, n54, n190, n185, sum_14, n55, p14, n0, n50, p0, cin, n897, g0, g_lsb, p_lsb, n1110, n899, n186, n146);

	input n55, p14, n109, n108, n1162, n0, p0, cin, n1151, n771, g0, n1110, n899, n54, n190;
	output n50, n186, n897, g_lsb, n767, n1059, p_lsb, sum_14, n98, n185, n146;
	ao21 U1(n767,n185,n1162,n190);
	ao21 U1(n897,n767,n1151,n771);
	ao21 U1(n50,g_lsb,p0,g0);
	ao21 U1(n146,n98,n109,n108);
	buffer U1(n186,n0);
	buffer U2(n185,n146);
	ao21 U1(n1059,n897,n1110,n899);
	assign p_lsb=1'b0;
	assign g_lsb=cin;
	xor2 U1(sum_14,p14,n1059);
	ao21 U1(n98,n50,n55,n54);

endmodule
