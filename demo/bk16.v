module adder(cout, sum, a, b, cin);

    input [15:0] a, b;
    input cin;
    output [15:0] sum;
    output cout;

	wire g1, p2, p14, p12, g6, g14, p9, p10, p5, p13, p0, p4, p_lsb, g11, g2, g0, p1, g_lsb, g9, g7, g12, p6, p11, p8, g8, p7, g5, g13, p3, g4, g10, g3;
	wire n1025, n204, n1026, n1029, n1030, n1033, n1034, n49, n50, n51, n52, n53, n54, n57, n58, n215, n61, n62, n63, n64, n65, n66, n216, n69, n70, n73, n74, n75, n76, n77, n78, n81, n82, n85, n86, n87, n88, n89, n90, n93, n94, n97, n98, n99, n100, n101, n102, n103, n104, n105, n106, n109, n110, n113, n114, n117, n118, n121, n122, n123, n124, n125, n127, n128, n129, n130, n126, n1147, n133, n134, n1151, n1152, n137, n138, n1155, n1156, n141, n142, n145, n146, n1148, n149, n150, n1167, n1168, n153, n154, n155, n157, n158, n159, n160, n161, n162, n156, n1179, n165, n166, n1187, n1188, n169, n170, n1191, n1192, n173, n174, n1195, n1196, n177, n178, n1203, n1204, n181, n182, n1207, n1208, n185, n186, n189, n190, n193, n194, n195, n196, n197, n198, n199, n1159, n201, n202, n200, n205, n206, n1160, n203, n209, n210, n211, n212, n213, n214, n207, n208, n217, n218, n219, n220, n221, n222, n223, n224, n1163, n1164, n147, n148, n151, n152, n1171, n1172, n1175, n1176, n1180, n1183, n1184, n1369, n1370, n1373, n1374, n1377, n1378, n1381, n1382, n1385, n1386, n1389, n1390, n1393, n1394, n1397, n1398, n1401, n1402, n1405, n1406, n1409, n1410, n1413, n1414, n1417, n1418, n1421, n1422, n1425, n1426, n1199, n1429, n1430, n1200, n973, n974, n977, n978, n981, n982, n985, n986, n989, n990, n993, n994, n997, n998, n1001, n1002, n1005, n1006, n1009, n1010, n1013, n1014, n1017, n1018, n1021, n1022;

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

	ppa_post ppa_post_0_8 ( .pin( {p0} ), .gin( {n1370} ), .sum( {sum[0]} ) );
	ppa_post ppa_post_1_8 ( .pin( {p1} ), .gin( {n1374} ), .sum( {sum[1]} ) );
	ppa_post ppa_post_2_8 ( .pin( {p2} ), .gin( {n1378} ), .sum( {sum[2]} ) );
	ppa_post ppa_post_3_8 ( .pin( {p3} ), .gin( {n1382} ), .sum( {sum[3]} ) );
	ppa_post ppa_post_4_8 ( .pin( {p4} ), .gin( {n1386} ), .sum( {sum[4]} ) );
	ppa_post ppa_post_5_8 ( .pin( {p5} ), .gin( {n1390} ), .sum( {sum[5]} ) );
	ppa_post ppa_post_6_8 ( .pin( {p6} ), .gin( {n1394} ), .sum( {sum[6]} ) );
	ppa_post ppa_post_7_8 ( .pin( {p7} ), .gin( {n1398} ), .sum( {sum[7]} ) );
	ppa_post ppa_post_8_8 ( .pin( {p8} ), .gin( {n1402} ), .sum( {sum[8]} ) );
	ppa_post ppa_post_9_8 ( .pin( {p9} ), .gin( {n1406} ), .sum( {sum[9]} ) );
	ppa_post ppa_post_10_8 ( .pin( {p10} ), .gin( {n1410} ), .sum( {sum[10]} ) );
	ppa_post ppa_post_11_8 ( .pin( {p11} ), .gin( {n1414} ), .sum( {sum[11]} ) );
	ppa_post ppa_post_12_8 ( .pin( {p12} ), .gin( {n1418} ), .sum( {sum[12]} ) );
	ppa_post ppa_post_13_8 ( .pin( {p13} ), .gin( {n1422} ), .sum( {sum[13]} ) );
	ppa_post ppa_post_14_8 ( .pin( {p14} ), .gin( {n1426} ), .sum( {sum[14]} ) );
	ppa_post ppa_post_15_8 ( .pin( {p15} ), .gin( {n1430} ), .sum( {sum[15]} ) );

// start of custom pre/post logic

    ppa_pre ppa_pre_cout ( .a_in( a[15] ), .b_in( b[15] ), .pout ( p15 ), .gout ( g15 ) );
    ppa_grey ppa_grey_cout ( .gin ( {g15,n1430} ), .pin ( p15 ), .gout ( cout ) );

// start of tree row 1

	assign n49 = p_lsb;
	assign n50 = g_lsb;
	assign n53 = p1;
	assign n54 = g1;
	ppa_black ppa_black_3_1 ( .gin( {g2,g1} ), .pin( {p2,p1} ), .gout( {n58} ), .pout( {n57} ) );
	assign n61 = p3;
	assign n62 = g3;
	ppa_black ppa_black_5_1 ( .gin( {g4,g3} ), .pin( {p4,p3} ), .gout( {n64} ), .pout( {n63} ) );
	assign n65 = p5;
	assign n66 = g5;
	ppa_black ppa_black_7_1 ( .gin( {g6,g5} ), .pin( {p6,p5} ), .gout( {n70} ), .pout( {n69} ) );
	assign n73 = p7;
	assign n74 = g7;
	ppa_black ppa_black_9_1 ( .gin( {g8,g7} ), .pin( {p8,p7} ), .gout( {n76} ), .pout( {n75} ) );
	assign n77 = p9;
	assign n78 = g9;
	ppa_black ppa_black_11_1 ( .gin( {g10,g9} ), .pin( {p10,p9} ), .gout( {n82} ), .pout( {n81} ) );
	assign n85 = p11;
	assign n86 = g11;
	ppa_black ppa_black_13_1 ( .gin( {g12,g11} ), .pin( {p12,p11} ), .gout( {n88} ), .pout( {n87} ) );
	assign n89 = p13;
	assign n90 = g13;
	ppa_black ppa_black_15_1 ( .gin( {g14,g13} ), .pin( {p14,p13} ), .gout( {n94} ), .pout( {n93} ) );

// start of tree row 2

	assign n97 = n49;
	assign n98 = n50;
	assign n99 = n51;
	assign n100 = n52;
	assign n101 = n53;
	assign n102 = n54;
	assign n105 = n61;
	assign n106 = n62;
	assign n109 = n63;
	assign n110 = n64;
	assign n113 = n65;
	assign n114 = n66;
	ppa_black ppa_black_7_2 ( .gin( {n70,n64} ), .pin( {n69,n63} ), .gout( {n118} ), .pout( {n117} ) );
	assign n121 = n73;
	assign n122 = n74;
	assign n123 = n75;
	assign n124 = n76;
	assign n125 = n77;
	assign n126 = n78;
	ppa_black ppa_black_11_2 ( .gin( {n82,n76} ), .pin( {n81,n75} ), .gout( {n128} ), .pout( {n127} ) );
	assign n129 = n85;
	assign n130 = n86;
	assign n133 = n87;
	assign n134 = n88;
	assign n137 = n89;
	assign n138 = n90;
	ppa_black ppa_black_15_2 ( .gin( {n94,n88} ), .pin( {n93,n87} ), .gout( {n142} ), .pout( {n141} ) );

// start of tree row 3

	assign n145 = n97;
	assign n146 = n98;
	assign n147 = n99;
	assign n148 = n100;
	assign n149 = n101;
	assign n150 = n102;
	assign n151 = n103;
	assign n152 = n104;
	assign n153 = n105;
	assign n154 = n106;
	assign n155 = n109;
	assign n156 = n110;
	assign n157 = n113;
	assign n158 = n114;
	assign n161 = n121;
	assign n162 = n122;
	assign n165 = n123;
	assign n166 = n124;
	assign n169 = n125;
	assign n170 = n126;
	assign n173 = n127;
	assign n174 = n128;
	assign n177 = n129;
	assign n178 = n130;
	assign n181 = n133;
	assign n182 = n134;
	assign n185 = n137;
	assign n186 = n138;
	ppa_black ppa_black_15_3 ( .gin( {n142,n128} ), .pin( {n141,n127} ), .gout( {n190} ), .pout( {n189} ) );

// start of tree row 4

	assign n193 = n145;
	assign n194 = n146;
	buffer_node buffer_node_1_4 ( .gin( {n148} ), .pin( {n147} ), .gout( {n196} ), .pout( {n195} ) );
	assign n197 = n149;
	assign n198 = n150;
	buffer_node buffer_node_3_4 ( .gin( {n152} ), .pin( {n151} ), .gout( {n200} ), .pout( {n199} ) );
	assign n201 = n153;
	assign n202 = n154;
	assign n203 = n155;
	assign n204 = n156;
	assign n205 = n157;
	assign n206 = n158;
	assign n209 = n161;
	assign n210 = n162;
	assign n211 = n165;
	assign n212 = n166;
	assign n213 = n169;
	assign n214 = n170;
	assign n215 = n173;
	assign n216 = n174;
	assign n217 = n177;
	assign n218 = n178;
	assign n219 = n181;
	assign n220 = n182;
	assign n221 = n185;
	assign n222 = n186;
	ppa_black ppa_black_15_4 ( .gin( {n190,n160} ), .pin( {n189,n159} ), .gout( {n224} ), .pout( {n223} ) );

// start of tree row 5

	assign n973 = n193;
	assign n974 = n194;
	assign n977 = n195;
	assign n978 = n196;
	ppa_black ppa_black_2_5 ( .gin( {n198,n196} ), .pin( {n197,n195} ), .gout( {n982} ), .pout( {n981} ) );
	buffer_node buffer_node_3_5 ( .gin( {n200} ), .pin( {n199} ), .gout( {n986} ), .pout( {n985} ) );
	assign n989 = n201;
	assign n990 = n202;
	ppa_black ppa_black_5_5 ( .gin( {n204,n200} ), .pin( {n203,n199} ), .gout( {n994} ), .pout( {n993} ) );
	assign n997 = n205;
	assign n998 = n206;
	buffer_node buffer_node_7_5 ( .gin( {n208} ), .pin( {n207} ), .gout( {n1002} ), .pout( {n1001} ) );
	assign n1005 = n209;
	assign n1006 = n210;
	assign n1009 = n211;
	assign n1010 = n212;
	assign n1013 = n213;
	assign n1014 = n214;
	assign n1021 = n217;
	assign n1022 = n218;
	assign n1025 = n219;
	assign n1026 = n220;
	assign n1029 = n221;
	assign n1030 = n222;
	assign n1033 = n223;
	assign n1034 = n224;

// start of tree row 6

	assign n1147 = n973;
	assign n1148 = n974;
	assign n1151 = n977;
	assign n1152 = n978;
	assign n1155 = n981;
	assign n1156 = n982;
	assign n1159 = n985;
	assign n1160 = n986;
	ppa_black ppa_black_4_6 ( .gin( {n990,n986} ), .pin( {n989,n985} ), .gout( {n1164} ), .pout( {n1163} ) );
	assign n1167 = n993;
	assign n1168 = n994;
	ppa_black ppa_black_6_6 ( .gin( {n998,n994} ), .pin( {n997,n993} ), .gout( {n1172} ), .pout( {n1171} ) );
	buffer_node buffer_node_7_6 ( .gin( {n1002} ), .pin( {n1001} ), .gout( {n1176} ), .pout( {n1175} ) );
	assign n1179 = n1005;
	assign n1180 = n1006;
	ppa_black ppa_black_9_6 ( .gin( {n1010,n1002} ), .pin( {n1009,n1001} ), .gout( {n1184} ), .pout( {n1183} ) );
	assign n1187 = n1013;
	assign n1188 = n1014;
	buffer_node buffer_node_11_6 ( .gin( {n1018} ), .pin( {n1017} ), .gout( {n1192} ), .pout( {n1191} ) );
	assign n1195 = n1021;
	assign n1196 = n1022;
	assign n1203 = n1029;
	assign n1204 = n1030;
	assign n1207 = n1033;
	assign n1208 = n1034;

// start of tree row 7

	assign n1369 = n1147;
	assign n1370 = n1148;
	assign n1373 = n1151;
	assign n1374 = n1152;
	assign n1377 = n1155;
	assign n1378 = n1156;
	assign n1381 = n1159;
	assign n1382 = n1160;
	assign n1385 = n1163;
	assign n1386 = n1164;
	assign n1389 = n1167;
	assign n1390 = n1168;
	assign n1393 = n1171;
	assign n1394 = n1172;
	assign n1397 = n1175;
	assign n1398 = n1176;
	ppa_black ppa_black_8_7 ( .gin( {n1180,n1176} ), .pin( {n1179,n1175} ), .gout( {n1402} ), .pout( {n1401} ) );
	assign n1405 = n1183;
	assign n1406 = n1184;
	ppa_black ppa_black_10_7 ( .gin( {n1188,n1184} ), .pin( {n1187,n1183} ), .gout( {n1410} ), .pout( {n1409} ) );
	assign n1413 = n1191;
	assign n1414 = n1192;
	ppa_black ppa_black_12_7 ( .gin( {n1196,n1192} ), .pin( {n1195,n1191} ), .gout( {n1418} ), .pout( {n1417} ) );
	assign n1421 = n1199;
	assign n1422 = n1200;
	assign n1429 = n1207;
	assign n1430 = n1208;
	block_1 block_1_instance ( .n1203 ( n1203 ), .n52 ( n52 ), .g_lsb ( g_lsb ), .n57 ( n57 ), .n1426 ( n1426 ), .n1200 ( n1200 ), .n1199 ( n1199 ), .n160 ( n160 ), .n1017 ( n1017 ), .sum_14 ( sum[14] ), .n1204 ( n1204 ), .p0 ( p0 ), .n208 ( n208 ), .n51 ( n51 ), .n159 ( n159 ), .n58 ( n58 ), .n118 ( n118 ), .n215 ( n215 ), .p14 ( p14 ), .p_lsb ( p_lsb ), .n104 ( n104 ), .g0 ( g0 ), .cin ( cin ), .n117 ( n117 ), .n1025 ( n1025 ), .n1425 ( n1425 ), .n103 ( n103 ), .n207 ( n207 ), .n1026 ( n1026 ), .n1018 ( n1018 ), .n216 ( n216 ) );


endmodule

module buffer_node(pin, gin, pout, gout);

	input pin, gin;
	output pout, gout;

	buffer U1(pout,pin);
	buffer U2(gout,gin);

endmodule

module ppa_grey(gin, pin, gout);

	input[1:0] gin;
	input pin;
	output gout;

	ao21 U1(gout,gin[0],pin,gin[1]);

endmodule

module ppa_black(gin, pin, gout, pout);

	input [1:0] gin, pin;
	output gout, pout;

	and2 U1(pout,pin[1],pin[0]);
	ao21 U2(gout,gin[0],pin[1],gin[1]);

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

module block_1( n1203, n52, g_lsb, n57, n1426, n1200, n1199, n160, n1017, sum_14, n1204, p0, n208, n51, n159, n58, n118, n215, p14, p_lsb, n104, g0, cin, n117, n1025, n1425, n103, n207, n1026, n1018, n216);

	input n1203, n58, n57, n215, p14, n118, g0, cin, n117, n1025, n1026, n1204, p0, n216;
	output n208, n52, n207, n51, g_lsb, n159, n1426, p_lsb, n104, n1200, n1425, n1199, n1017, n103, n160, sum_14, n1018;
	and2 U1(n1017,n215,n207);
	ao21 U2(n1018,n208,n215,n216);
	and2 U1(n51,p0,p_lsb);
	ao21 U2(n52,g_lsb,p0,g0);
	and2 U1(n1425,n1203,n1199);
	ao21 U2(n1426,n1200,n1203,n1204);
	and2 U1(n1199,n1025,n1017);
	ao21 U2(n1200,n1018,n1025,n1026);
	assign p_lsb=1'b0;
	assign g_lsb=cin;
	and2 U1(n103,n57,n51);
	ao21 U2(n104,n52,n57,n58);
	buffer U1(n207,n159);
	buffer U2(n208,n160);
	and2 U1(n159,n117,n103);
	ao21 U2(n160,n104,n117,n118);
	xor2 U1(sum_14,p14,n1426);

endmodule
