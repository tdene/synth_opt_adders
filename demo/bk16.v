module adder(cout, sum, a, b, cin);

	input [15:0] a, b;
	input cin;
	output [15:0] sum;
	output cout;

	wire g2, p11, g5, p10, g10, p4, g4, g12, g0, p5, p3, p_lsb, p9, g7, g3, p2, p14, g11, g13, g_lsb, p1, p6, p8, p12, g1, g14, p7, g6, g9, g8, p13;
	wire n1025, n1028, n1030, n1032, n1033, n1035, n1038, n1040, n1042, n1043, n1051, n1065, n48, n49, n50, n51, n1076, n53, n55, n56, n57, n58, n59, n60, n63, n64, n1089, n67, n68, n69, n70, n71, n72, n75, n76, n1101, n79, n80, n81, n82, n83, n84, n87, n88, n91, n92, n93, n94, n95, n96, n97, n1116, n99, n101, n103, n105, n106, n107, n108, n109, n110, n111, n112, n113, n114, n1130, n117, n118, n1141, n121, n122, n125, n126, n129, n130, n131, n132, n133, n135, n136, n137, n138, n139, n140, n141, n143, n145, n147, n149, n151, n153, n155, n157, n158, n159, n160, n161, n163, n164, n165, n167, n169, n171, n172, n173, n174, n175, n176, n177, n178, n179, n180, n699, n709, n716, n725, n728, n731, n734, n736, n739, n741, n744, n746, n748, n750, n752, n754, n756, n758, n760, n767, n774, n784, n794, n812, n826, n839, n844, n845, n847, n848, n851, n853, n854, n856, n859, n861, n864, n863, n866, n869, n871, n874, n876, n879, n881, n883, n884, n892, n905, n915, n925, n936, n947, n955, n969, n984, n998, n1003, n1004, n1006, n1007, n1009, n1010, n1015, n1012, n1013, n1017, n1018, n1020, n1022, n1023;

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

	ppa_post ppa_post_0_8 ( .gin( {n1004} ), .pin( {p0} ), .sum( {sum[0]} ) );
	ppa_post ppa_post_1_8 ( .gin( {n1007} ), .pin( {p1} ), .sum( {sum[1]} ) );
	ppa_post ppa_post_2_8 ( .gin( {n1010} ), .pin( {p2} ), .sum( {sum[2]} ) );
	ppa_post ppa_post_3_8 ( .gin( {n1013} ), .pin( {p3} ), .sum( {sum[3]} ) );
	ppa_post ppa_post_4_8 ( .gin( {n1015} ), .pin( {p4} ), .sum( {sum[4]} ) );
	ppa_post ppa_post_5_8 ( .gin( {n1018} ), .pin( {p5} ), .sum( {sum[5]} ) );
	ppa_post ppa_post_6_8 ( .gin( {n1020} ), .pin( {p6} ), .sum( {sum[6]} ) );
	ppa_post ppa_post_7_8 ( .gin( {n1023} ), .pin( {p7} ), .sum( {sum[7]} ) );
	ppa_post ppa_post_8_8 ( .gin( {n1025} ), .pin( {p8} ), .sum( {sum[8]} ) );
	ppa_post ppa_post_9_8 ( .gin( {n1028} ), .pin( {p9} ), .sum( {sum[9]} ) );
	ppa_post ppa_post_10_8 ( .gin( {n1030} ), .pin( {p10} ), .sum( {sum[10]} ) );
	ppa_post ppa_post_11_8 ( .gin( {n1033} ), .pin( {p11} ), .sum( {sum[11]} ) );
	ppa_post ppa_post_12_8 ( .gin( {n1035} ), .pin( {p12} ), .sum( {sum[12]} ) );
	ppa_post ppa_post_13_8 ( .gin( {n1038} ), .pin( {p13} ), .sum( {sum[13]} ) );
	ppa_post ppa_post_14_8 ( .gin( {n1040} ), .pin( {p14} ), .sum( {sum[14]} ) );
	ppa_post ppa_post_15_8 ( .gin( {n1043} ), .pin( {p15} ), .sum( {sum[15]} ) );

// start of custom pre/post logic

	ppa_pre ppa_pre_cout ( .a_in( a[15] ), .b_in( b[15] ), .pout ( p15 ), .gout ( g15 ) );
	ppa_grey ppa_grey_cout ( .gin ( {g15,n1043} ), .pin ( p15 ), .gout ( cout ) );

// start of tree row 1

	assign n49 = p_lsb;
	assign n48 = g_lsb;
	assign n699 = p1;
	assign n51 = g1;
	ppa_black ppa_black_3_1 ( .gin( {g2,g1} ), .pin( {p2,p1} ), .gout( {n53} ), .pout( {n0} ) );
	assign n56 = p3;
	assign n55 = g3;
	ppa_black ppa_black_5_1 ( .gin( {g4,g3} ), .pin( {p4,p3} ), .gout( {n57} ), .pout( {n58} ) );
	assign n60 = p5;
	assign n59 = g5;
	ppa_black ppa_black_7_1 ( .gin( {g6,g5} ), .pin( {p6,p5} ), .gout( {n63} ), .pout( {n64} ) );
	assign n68 = p7;
	assign n67 = g7;
	ppa_black ppa_black_9_1 ( .gin( {g8,g7} ), .pin( {p8,p7} ), .gout( {n69} ), .pout( {n70} ) );
	assign n72 = p9;
	assign n71 = g9;
	ppa_black ppa_black_11_1 ( .gin( {g10,g9} ), .pin( {p10,p9} ), .gout( {n75} ), .pout( {n76} ) );
	assign n80 = p11;
	assign n79 = g11;
	ppa_black ppa_black_13_1 ( .gin( {g12,g11} ), .pin( {p12,p11} ), .gout( {n81} ), .pout( {n82} ) );
	assign n84 = p13;
	assign n83 = g13;
	ppa_black ppa_black_15_1 ( .gin( {g14,g13} ), .pin( {p14,p13} ), .gout( {n87} ), .pout( {n88} ) );

// start of tree row 2

	assign n92 = n49;
	assign n91 = n48;
	assign n94 = n0;
	assign n93 = n50;
	assign n812 = n699;
	assign n95 = n51;
	assign n709 = n56;
	assign n97 = n55;
	assign n936 = n58;
	assign n99 = n57;
	assign n716 = n60;
	assign n101 = n59;
	ppa_black ppa_black_7_2 ( .gin( {n63,n57} ), .pin( {n64,n58} ), .gout( {n103} ), .pout( {n0} ) );
	assign n106 = n68;
	assign n105 = n67;
	assign n108 = n70;
	assign n107 = n69;
	assign n110 = n72;
	assign n109 = n71;
	ppa_black ppa_black_11_2 ( .gin( {n75,n69} ), .pin( {n76,n70} ), .gout( {n111} ), .pout( {n112} ) );
	assign n114 = n80;
	assign n113 = n79;
	assign n118 = n82;
	assign n117 = n81;
	assign n122 = n84;
	assign n121 = n83;
	ppa_black ppa_black_15_2 ( .gin( {n87,n81} ), .pin( {n88,n82} ), .gout( {n125} ), .pout( {n126} ) );

// start of tree row 3

	assign n130 = n92;
	assign n129 = n91;
	assign n132 = n94;
	assign n131 = n93;
	assign n969 = n812;
	assign n133 = n95;
	assign n136 = n0;
	assign n135 = n96;
	assign n826 = n709;
	assign n137 = n97;
	assign n1101 = n936;
	assign n138 = n99;
	assign n839 = n716;
	assign n139 = n101;
	assign n767 = n106;
	assign n141 = n105;
	assign n947 = n108;
	assign n143 = n107;
	assign n774 = n110;
	assign n145 = n109;
	assign n1141 = n112;
	assign n147 = n111;
	assign n784 = n114;
	assign n149 = n113;
	assign n955 = n118;
	assign n151 = n117;
	assign n794 = n122;
	assign n153 = n121;
	ppa_black ppa_black_15_3 ( .gin( {n125,n111} ), .pin( {n126,n112} ), .gout( {n155} ), .pout( {n0} ) );

// start of tree row 4

	assign n158 = n130;
	assign n157 = n129;
	buffer_node buffer_node_1_4 ( .gin( {n131} ), .pin( {n132} ), .gout( {n159} ), .pout( {n160} ) );
	assign n0 = n969;
	assign n161 = n133;
	buffer_node buffer_node_3_4 ( .gin( {n135} ), .pin( {n136} ), .gout( {n163} ), .pout( {n164} ) );
	assign n984 = n826;
	assign n165 = n137;
	assign n0 = n1101;
	assign n167 = n138;
	assign n998 = n839;
	assign n169 = n139;
	assign n892 = n767;
	assign n173 = n141;
	assign n1116 = n947;
	assign n174 = n143;
	assign n905 = n774;
	assign n175 = n145;
	assign n0 = n1141;
	assign n176 = n147;
	assign n915 = n784;
	assign n177 = n149;
	assign n1130 = n955;
	assign n178 = n151;
	assign n925 = n794;
	assign n179 = n153;
	ppa_grey ppa_grey_15_4 ( .gin( {n155,n140} ), .pin( {n0} ), .gout( {n180} ) );

// start of tree row 5

	assign n844 = n158;
	assign n725 = n157;
	assign n847 = n160;
	assign n728 = n159;
	ppa_grey ppa_grey_2_5 ( .gin( {n161,n159} ), .pin( {n160} ), .gout( {n731} ) );
	buffer_node buffer_node_3_5 ( .gin( {n163} ), .pin( {n164} ), .gout( {n734} ), .pout( {n853} ) );
	assign n0 = n984;
	assign n736 = n165;
	ppa_grey ppa_grey_5_5 ( .gin( {n167,n163} ), .pin( {n164} ), .gout( {n739} ) );
	assign n0 = n998;
	assign n741 = n169;
	buffer_node buffer_node_7_5 ( .gin( {n171} ), .pin( {n172} ), .gout( {n744} ), .pout( {n863} ) );
	assign n1051 = n892;
	assign n746 = n173;
	assign n0 = n1116;
	assign n748 = n174;
	assign n1065 = n905;
	assign n750 = n175;
	assign n1076 = n915;
	assign n754 = n177;
	assign n0 = n1130;
	assign n756 = n178;
	assign n1089 = n925;
	assign n758 = n179;
	assign n883 = n0;
	assign n760 = n180;

// start of tree row 6

	assign n1003 = n844;
	assign n845 = n725;
	assign n1006 = n847;
	assign n848 = n728;
	assign n1009 = n850;
	assign n851 = n731;
	assign n1012 = n853;
	assign n854 = n734;
	ppa_grey ppa_grey_4_6 ( .gin( {n736,n734} ), .pin( {n853} ), .gout( {n856} ) );
	assign n1017 = n858;
	assign n859 = n739;
	ppa_grey ppa_grey_6_6 ( .gin( {n741,n739} ), .pin( {n858} ), .gout( {n861} ) );
	buffer_node buffer_node_7_6 ( .gin( {n744} ), .pin( {n863} ), .gout( {n864} ), .pout( {n1022} ) );
	assign n0 = n1051;
	assign n866 = n746;
	ppa_grey ppa_grey_9_6 ( .gin( {n748,n744} ), .pin( {n863} ), .gout( {n869} ) );
	assign n0 = n1065;
	assign n871 = n750;
	buffer_node buffer_node_11_6 ( .gin( {n752} ), .pin( {n873} ), .gout( {n874} ), .pout( {n1032} ) );
	assign n0 = n1076;
	assign n876 = n754;
	assign n0 = n1089;
	assign n881 = n758;
	assign n1042 = n883;
	assign n884 = n760;

// start of tree row 7

	assign n0 = n1003;
	assign n1004 = n845;
	assign n0 = n1006;
	assign n1007 = n848;
	assign n0 = n1009;
	assign n1010 = n851;
	assign n0 = n1012;
	assign n1013 = n854;
	assign n0 = n0;
	assign n1015 = n856;
	assign n0 = n1017;
	assign n1018 = n859;
	assign n0 = n0;
	assign n1020 = n861;
	assign n0 = n1022;
	assign n1023 = n864;
	ppa_grey ppa_grey_8_7 ( .gin( {n866,n864} ), .pin( {n1022} ), .gout( {n1025} ) );
	assign n0 = n1027;
	assign n1028 = n869;
	ppa_grey ppa_grey_10_7 ( .gin( {n871,n869} ), .pin( {n1027} ), .gout( {n1030} ) );
	assign n0 = n1032;
	assign n1033 = n874;
	ppa_grey ppa_grey_12_7 ( .gin( {n876,n874} ), .pin( {n1032} ), .gout( {n1035} ) );
	assign n0 = n1037;
	assign n1038 = n879;
	assign n0 = n1042;
	assign n1043 = n884;
	block_1 block_1_instance ( .p_lsb ( p_lsb ), .p0 ( p0 ), .n879 ( n879 ), .n50 ( n50 ), .g0 ( g0 ), .n103 ( n103 ), .p14 ( p14 ), .n1040 ( n1040 ), .n0 ( n0 ), .b_0 ( b[0] ), .n756 ( n756 ), .n881 ( n881 ), .n172 ( n172 ), .sum_14 ( sum[14] ), .n1037 ( n1037 ), .n873 ( n873 ), .n171 ( n171 ), .n176 ( n176 ), .n140 ( n140 ), .n96 ( n96 ), .a_0 ( a[0] ), .g_lsb ( g_lsb ), .n752 ( n752 ), .n53 ( n53 ) );


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

module ppa_black(gin, pin, gout, pout);

	input [1:0] gin, pin;
	output gout, pout;

	and2 U1(pout,pin[1],pin[0]);
	ao21 U2(gout,gin[0],pin[1],gin[1]);

endmodule

module buffer_node(pin, gin, pout, gout);

	input pin, gin;
	output pout, gout;

	buffer U1(pout,pin);
	buffer U2(gout,gin);

endmodule

module ppa_post(pin, gin, sum);

	input pin, gin;
	output sum;

	xor2 U1(sum,pin,gin);

endmodule

module block_1( p_lsb, p0, n879, n50, g0, n103, p14, n1040, n0, b_0, n756, n881, n172, sum_14, n1037, n873, n171, n176, n140, n96, a_0, g_lsb, n752, n53);

	input p_lsb, n176, n103, p14, a_0, n53, n0, b_0, n756, n881, g_lsb, n1037, n873;
	output p0, n140, n96, n879, n50, n1040, n172, sum_14, n752, n171, g0;
	ao21 U1(n140,n96,n0,n103);
	xor2 U1(p0,a_0,b_0);
	and2 U2(g0,a_0,b_0);
	buffer U1(n172,n0);
	buffer U2(n171,n140);
	xor2 U1(sum_14,p14,n1040);
	ao21 U1(n752,n171,n172,n176);
	ao21 U1(n96,n50,n0,n53);
	ao21 U1(n879,n752,n873,n756);
	ao21 U1(n50,g_lsb,p_lsb,g0);
	ao21 U1(n1040,n879,n1037,n881);

endmodule
