library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std;

entity adder is
    port (
	a,b : in std_logic_vector(15 downto 0);
	cin : in std_logic;
	cout : out std_logic;
	sum : out std_logic_vector(15 downto 0)
    );
end entity;

architecture pptree of adder is
	signal p0, p5, g4, g0, g8, g14, g11, g7, p8, p3, p_lsb, g_lsb, p1, g12, p10, p4, p2, p13, g1, p6, g10, g9, g5, p12, g13, p9, g2, g6, p11, p7, g3, p14 : std_logic;
	signal n1025, n1026, n204, n1029, n1030, n1033, n1034, n49, n50, n51, n52, n53, n54, n57, n58, n215, n61, n62, n63, n64, n65, n66, n216, n69, n70, n73, n74, n75, n76, n77, n78, n81, n82, n85, n86, n87, n88, n89, n90, n93, n94, n97, n98, n99, n100, n101, n102, n103, n104, n105, n106, n109, n110, n113, n114, n117, n118, n121, n122, n123, n124, n125, n127, n128, n129, n130, n126, n133, n134, n1151, n137, n138, n1147, n1155, n141, n142, n1159, n1148, n145, n146, n1167, n1168, n149, n150, n147, n148, n153, n154, n155, n156, n157, n158, n159, n160, n161, n162, n1179, n165, n166, n169, n170, n1152, n1187, n173, n174, n1191, n1192, n177, n178, n1195, n1196, n181, n182, n1207, n1208, n185, n186, n1156, n1203, n189, n190, n193, n194, n195, n196, n197, n198, n199, n201, n202, n200, n203, n205, n206, n1160, n209, n210, n211, n212, n213, n214, n207, n208, n217, n218, n219, n220, n221, n223, n224, n222, n1163, n1164, n151, n152, n1171, n1172, n1175, n1176, n1180, n1183, n1184, n1369, n1370, n1188, n1373, n1374, n1377, n1378, n1381, n1382, n1385, n1386, n1389, n1390, n1393, n1394, n1397, n1398, n1401, n1402, n1405, n1406, n1409, n1410, n1413, n1414, n1417, n1418, n1421, n1422, n1425, n1426, n1199, n1429, n1430, n1200, n1204, n973, n974, n977, n978, n981, n982, n985, n986, n989, n990, n993, n994, n997, n998, n1001, n1002, n1005, n1006, n1009, n1010, n1013, n1014, n1017, n1018, n1021, n1022 : std_logic;

begin

-- start of pre-processing logic

	ppa_first_pre_0_0: ppa_first_pre
		port map (
			cin(0) => cin,
			pout(0) => p_lsb,
			gout(0) => g_lsb
		);
	ppa_pre_1_0: ppa_pre
		port map (
			a_in(0) => a[0],
			b_in(0) => b[0],
			pout(0) => p0,
			gout(0) => g0
		);
	ppa_pre_2_0: ppa_pre
		port map (
			a_in(0) => a[1],
			b_in(0) => b[1],
			pout(0) => p1,
			gout(0) => g1
		);
	ppa_pre_3_0: ppa_pre
		port map (
			a_in(0) => a[2],
			b_in(0) => b[2],
			pout(0) => p2,
			gout(0) => g2
		);
	ppa_pre_4_0: ppa_pre
		port map (
			a_in(0) => a[3],
			b_in(0) => b[3],
			pout(0) => p3,
			gout(0) => g3
		);
	ppa_pre_5_0: ppa_pre
		port map (
			a_in(0) => a[4],
			b_in(0) => b[4],
			pout(0) => p4,
			gout(0) => g4
		);
	ppa_pre_6_0: ppa_pre
		port map (
			a_in(0) => a[5],
			b_in(0) => b[5],
			pout(0) => p5,
			gout(0) => g5
		);
	ppa_pre_7_0: ppa_pre
		port map (
			a_in(0) => a[6],
			b_in(0) => b[6],
			pout(0) => p6,
			gout(0) => g6
		);
	ppa_pre_8_0: ppa_pre
		port map (
			a_in(0) => a[7],
			b_in(0) => b[7],
			pout(0) => p7,
			gout(0) => g7
		);
	ppa_pre_9_0: ppa_pre
		port map (
			a_in(0) => a[8],
			b_in(0) => b[8],
			pout(0) => p8,
			gout(0) => g8
		);
	ppa_pre_10_0: ppa_pre
		port map (
			a_in(0) => a[9],
			b_in(0) => b[9],
			pout(0) => p9,
			gout(0) => g9
		);
	ppa_pre_11_0: ppa_pre
		port map (
			a_in(0) => a[10],
			b_in(0) => b[10],
			pout(0) => p10,
			gout(0) => g10
		);
	ppa_pre_12_0: ppa_pre
		port map (
			a_in(0) => a[11],
			b_in(0) => b[11],
			pout(0) => p11,
			gout(0) => g11
		);
	ppa_pre_13_0: ppa_pre
		port map (
			a_in(0) => a[12],
			b_in(0) => b[12],
			pout(0) => p12,
			gout(0) => g12
		);
	ppa_pre_14_0: ppa_pre
		port map (
			a_in(0) => a[13],
			b_in(0) => b[13],
			pout(0) => p13,
			gout(0) => g13
		);
	ppa_pre_15_0: ppa_pre
		port map (
			a_in(0) => a[14],
			b_in(0) => b[14],
			pout(0) => p14,
			gout(0) => g14
		);

-- start of post-processing logic

	ppa_post_0_8: ppa_post
		port map (
			pin(0) => p0,
			gin(0) => n1370,
			sum(0) => sum[0]
		);
	ppa_post_1_8: ppa_post
		port map (
			pin(0) => p1,
			gin(0) => n1374,
			sum(0) => sum[1]
		);
	ppa_post_2_8: ppa_post
		port map (
			pin(0) => p2,
			gin(0) => n1378,
			sum(0) => sum[2]
		);
	ppa_post_3_8: ppa_post
		port map (
			pin(0) => p3,
			gin(0) => n1382,
			sum(0) => sum[3]
		);
	ppa_post_4_8: ppa_post
		port map (
			pin(0) => p4,
			gin(0) => n1386,
			sum(0) => sum[4]
		);
	ppa_post_5_8: ppa_post
		port map (
			pin(0) => p5,
			gin(0) => n1390,
			sum(0) => sum[5]
		);
	ppa_post_6_8: ppa_post
		port map (
			pin(0) => p6,
			gin(0) => n1394,
			sum(0) => sum[6]
		);
	ppa_post_7_8: ppa_post
		port map (
			pin(0) => p7,
			gin(0) => n1398,
			sum(0) => sum[7]
		);
	ppa_post_8_8: ppa_post
		port map (
			pin(0) => p8,
			gin(0) => n1402,
			sum(0) => sum[8]
		);
	ppa_post_9_8: ppa_post
		port map (
			pin(0) => p9,
			gin(0) => n1406,
			sum(0) => sum[9]
		);
	ppa_post_10_8: ppa_post
		port map (
			pin(0) => p10,
			gin(0) => n1410,
			sum(0) => sum[10]
		);
	ppa_post_11_8: ppa_post
		port map (
			pin(0) => p11,
			gin(0) => n1414,
			sum(0) => sum[11]
		);
	ppa_post_12_8: ppa_post
		port map (
			pin(0) => p12,
			gin(0) => n1418,
			sum(0) => sum[12]
		);
	ppa_post_13_8: ppa_post
		port map (
			pin(0) => p13,
			gin(0) => n1422,
			sum(0) => sum[13]
		);
	ppa_post_14_8: ppa_post
		port map (
			pin(0) => p14,
			gin(0) => n1426,
			sum(0) => sum[14]
		);
	ppa_post_15_8: ppa_post
		port map (
			pin(0) => p15,
			gin(0) => n1430,
			sum(0) => sum[15]
		);

-- start of custom pre/post logic

    ppa_pre_cout: ppa_pre
	port map (
	    a_in => a(15),
	    b_in => b(15),
	    pout => p15,
	    gout => g15
        );
    ppa_grey_cout: ppa_grey
	port map (
	    gin(0) => n1430,
	    gin(1) => g15,
	    pin => p15,
	    gout => cout
        );

-- start of tree row 1

	n49 <= p_lsb;
	n50 <= g_lsb;
	ppa_black_1_1: ppa_black
		port map (
			gin(0) => g_lsb,
			gin(1) => g0,
			pin(0) => p_lsb,
			pin(1) => p0,
			gout(0) => n52,
			pout(0) => n51
		);
	n53 <= p1;
	n54 <= g1;
	ppa_black_3_1: ppa_black
		port map (
			gin(0) => g1,
			gin(1) => g2,
			pin(0) => p1,
			pin(1) => p2,
			gout(0) => n58,
			pout(0) => n57
		);
	n61 <= p3;
	n62 <= g3;
	ppa_black_5_1: ppa_black
		port map (
			gin(0) => g3,
			gin(1) => g4,
			pin(0) => p3,
			pin(1) => p4,
			gout(0) => n64,
			pout(0) => n63
		);
	n65 <= p5;
	n66 <= g5;
	ppa_black_7_1: ppa_black
		port map (
			gin(0) => g5,
			gin(1) => g6,
			pin(0) => p5,
			pin(1) => p6,
			gout(0) => n70,
			pout(0) => n69
		);
	n73 <= p7;
	n74 <= g7;
	ppa_black_9_1: ppa_black
		port map (
			gin(0) => g7,
			gin(1) => g8,
			pin(0) => p7,
			pin(1) => p8,
			gout(0) => n76,
			pout(0) => n75
		);
	n77 <= p9;
	n78 <= g9;
	ppa_black_11_1: ppa_black
		port map (
			gin(0) => g9,
			gin(1) => g10,
			pin(0) => p9,
			pin(1) => p10,
			gout(0) => n82,
			pout(0) => n81
		);
	n85 <= p11;
	n86 <= g11;
	ppa_black_13_1: ppa_black
		port map (
			gin(0) => g11,
			gin(1) => g12,
			pin(0) => p11,
			pin(1) => p12,
			gout(0) => n88,
			pout(0) => n87
		);
	n89 <= p13;
	n90 <= g13;
	ppa_black_15_1: ppa_black
		port map (
			gin(0) => g13,
			gin(1) => g14,
			pin(0) => p13,
			pin(1) => p14,
			gout(0) => n94,
			pout(0) => n93
		);

-- start of tree row 2

	n97 <= n49;
	n98 <= n50;
	n99 <= n51;
	n100 <= n52;
	n101 <= n53;
	n102 <= n54;
	ppa_black_3_2: ppa_black
		port map (
			gin(0) => n52,
			gin(1) => n58,
			pin(0) => n51,
			pin(1) => n57,
			gout(0) => n104,
			pout(0) => n103
		);
	n105 <= n61;
	n106 <= n62;
	n109 <= n63;
	n110 <= n64;
	n113 <= n65;
	n114 <= n66;
	ppa_black_7_2: ppa_black
		port map (
			gin(0) => n64,
			gin(1) => n70,
			pin(0) => n63,
			pin(1) => n69,
			gout(0) => n118,
			pout(0) => n117
		);
	n121 <= n73;
	n122 <= n74;
	n123 <= n75;
	n124 <= n76;
	n125 <= n77;
	n126 <= n78;
	ppa_black_11_2: ppa_black
		port map (
			gin(0) => n76,
			gin(1) => n82,
			pin(0) => n75,
			pin(1) => n81,
			gout(0) => n128,
			pout(0) => n127
		);
	n129 <= n85;
	n130 <= n86;
	n133 <= n87;
	n134 <= n88;
	n137 <= n89;
	n138 <= n90;
	ppa_black_15_2: ppa_black
		port map (
			gin(0) => n88,
			gin(1) => n94,
			pin(0) => n87,
			pin(1) => n93,
			gout(0) => n142,
			pout(0) => n141
		);

-- start of tree row 3

	n145 <= n97;
	n146 <= n98;
	n147 <= n99;
	n148 <= n100;
	n149 <= n101;
	n150 <= n102;
	n151 <= n103;
	n152 <= n104;
	n153 <= n105;
	n154 <= n106;
	n155 <= n109;
	n156 <= n110;
	n157 <= n113;
	n158 <= n114;
	ppa_black_7_3: ppa_black
		port map (
			gin(0) => n104,
			gin(1) => n118,
			pin(0) => n103,
			pin(1) => n117,
			gout(0) => n160,
			pout(0) => n159
		);
	n161 <= n121;
	n162 <= n122;
	n165 <= n123;
	n166 <= n124;
	n169 <= n125;
	n170 <= n126;
	n173 <= n127;
	n174 <= n128;
	n177 <= n129;
	n178 <= n130;
	n181 <= n133;
	n182 <= n134;
	n185 <= n137;
	n186 <= n138;
	ppa_black_15_3: ppa_black
		port map (
			gin(0) => n128,
			gin(1) => n142,
			pin(0) => n127,
			pin(1) => n141,
			gout(0) => n190,
			pout(0) => n189
		);

-- start of tree row 4

	n193 <= n145;
	n194 <= n146;
	buffer_node_1_4: buffer_node
		port map (
			gin(0) => n148,
			pin(0) => n147,
			gout(0) => n196,
			pout(0) => n195
		);
	n197 <= n149;
	n198 <= n150;
	buffer_node_3_4: buffer_node
		port map (
			gin(0) => n152,
			pin(0) => n151,
			gout(0) => n200,
			pout(0) => n199
		);
	n201 <= n153;
	n202 <= n154;
	n203 <= n155;
	n204 <= n156;
	n205 <= n157;
	n206 <= n158;
	buffer_node_7_4: buffer_node
		port map (
			gin(0) => n160,
			pin(0) => n159,
			gout(0) => n208,
			pout(0) => n207
		);
	n209 <= n161;
	n210 <= n162;
	n211 <= n165;
	n212 <= n166;
	n213 <= n169;
	n214 <= n170;
	n215 <= n173;
	n216 <= n174;
	n217 <= n177;
	n218 <= n178;
	n219 <= n181;
	n220 <= n182;
	n221 <= n185;
	n222 <= n186;
	ppa_black_15_4: ppa_black
		port map (
			gin(0) => n160,
			gin(1) => n190,
			pin(0) => n159,
			pin(1) => n189,
			gout(0) => n224,
			pout(0) => n223
		);

-- start of tree row 5

	n973 <= n193;
	n974 <= n194;
	n977 <= n195;
	n978 <= n196;
	ppa_black_2_5: ppa_black
		port map (
			gin(0) => n196,
			gin(1) => n198,
			pin(0) => n195,
			pin(1) => n197,
			gout(0) => n982,
			pout(0) => n981
		);
	buffer_node_3_5: buffer_node
		port map (
			gin(0) => n200,
			pin(0) => n199,
			gout(0) => n986,
			pout(0) => n985
		);
	n989 <= n201;
	n990 <= n202;
	ppa_black_5_5: ppa_black
		port map (
			gin(0) => n200,
			gin(1) => n204,
			pin(0) => n199,
			pin(1) => n203,
			gout(0) => n994,
			pout(0) => n993
		);
	n997 <= n205;
	n998 <= n206;
	buffer_node_7_5: buffer_node
		port map (
			gin(0) => n208,
			pin(0) => n207,
			gout(0) => n1002,
			pout(0) => n1001
		);
	n1005 <= n209;
	n1006 <= n210;
	n1009 <= n211;
	n1010 <= n212;
	n1013 <= n213;
	n1014 <= n214;
	ppa_black_11_5: ppa_black
		port map (
			gin(0) => n208,
			gin(1) => n216,
			pin(0) => n207,
			pin(1) => n215,
			gout(0) => n1018,
			pout(0) => n1017
		);
	n1021 <= n217;
	n1022 <= n218;
	n1025 <= n219;
	n1026 <= n220;
	n1029 <= n221;
	n1030 <= n222;
	n1033 <= n223;
	n1034 <= n224;

-- start of tree row 6

	n1147 <= n973;
	n1148 <= n974;
	n1151 <= n977;
	n1152 <= n978;
	n1155 <= n981;
	n1156 <= n982;
	n1159 <= n985;
	n1160 <= n986;
	ppa_black_4_6: ppa_black
		port map (
			gin(0) => n986,
			gin(1) => n990,
			pin(0) => n985,
			pin(1) => n989,
			gout(0) => n1164,
			pout(0) => n1163
		);
	n1167 <= n993;
	n1168 <= n994;
	ppa_black_6_6: ppa_black
		port map (
			gin(0) => n994,
			gin(1) => n998,
			pin(0) => n993,
			pin(1) => n997,
			gout(0) => n1172,
			pout(0) => n1171
		);
	buffer_node_7_6: buffer_node
		port map (
			gin(0) => n1002,
			pin(0) => n1001,
			gout(0) => n1176,
			pout(0) => n1175
		);
	n1179 <= n1005;
	n1180 <= n1006;
	ppa_black_9_6: ppa_black
		port map (
			gin(0) => n1002,
			gin(1) => n1010,
			pin(0) => n1001,
			pin(1) => n1009,
			gout(0) => n1184,
			pout(0) => n1183
		);
	n1187 <= n1013;
	n1188 <= n1014;
	buffer_node_11_6: buffer_node
		port map (
			gin(0) => n1018,
			pin(0) => n1017,
			gout(0) => n1192,
			pout(0) => n1191
		);
	n1195 <= n1021;
	n1196 <= n1022;
	ppa_black_13_6: ppa_black
		port map (
			gin(0) => n1018,
			gin(1) => n1026,
			pin(0) => n1017,
			pin(1) => n1025,
			gout(0) => n1200,
			pout(0) => n1199
		);
	n1203 <= n1029;
	n1204 <= n1030;
	n1207 <= n1033;
	n1208 <= n1034;

-- start of tree row 7

	n1369 <= n1147;
	n1370 <= n1148;
	n1373 <= n1151;
	n1374 <= n1152;
	n1377 <= n1155;
	n1378 <= n1156;
	n1381 <= n1159;
	n1382 <= n1160;
	n1385 <= n1163;
	n1386 <= n1164;
	n1389 <= n1167;
	n1390 <= n1168;
	n1393 <= n1171;
	n1394 <= n1172;
	n1397 <= n1175;
	n1398 <= n1176;
	ppa_black_8_7: ppa_black
		port map (
			gin(0) => n1176,
			gin(1) => n1180,
			pin(0) => n1175,
			pin(1) => n1179,
			gout(0) => n1402,
			pout(0) => n1401
		);
	n1405 <= n1183;
	n1406 <= n1184;
	ppa_black_10_7: ppa_black
		port map (
			gin(0) => n1184,
			gin(1) => n1188,
			pin(0) => n1183,
			pin(1) => n1187,
			gout(0) => n1410,
			pout(0) => n1409
		);
	n1413 <= n1191;
	n1414 <= n1192;
	ppa_black_12_7: ppa_black
		port map (
			gin(0) => n1192,
			gin(1) => n1196,
			pin(0) => n1191,
			pin(1) => n1195,
			gout(0) => n1418,
			pout(0) => n1417
		);
	n1421 <= n1199;
	n1422 <= n1200;
	ppa_black_14_7: ppa_black
		port map (
			gin(0) => n1200,
			gin(1) => n1204,
			pin(0) => n1199,
			pin(1) => n1203,
			gout(0) => n1426,
			pout(0) => n1425
		);
	n1429 <= n1207;
	n1430 <= n1208;

end architecture

entity ppa_black is
	port (
		gin : in std_logic_vector(1 downto 0);
		gout : out std_logic;
		pin : in std_logic_vector(1 downto 0);
		pout : out std_logic
	);
end entity;

architecture behavior of ppa_black is
begin

U1: and2
	port map (
		A => pin(0),
		B => pin(1),
		Y => pout
	);

U2: ao21
	port map (
		A0 => gin(0),
		A1 => pin(1),
		B0 => gin(1),
		Y => gout
	);

end architecture;

entity ppa_first_pre is
	port (
		cin : in std_logic;
		pout : out std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_first_pre is
begin

	pout <= '0';
	gout <= cin;

end architecture;

entity ppa_pre is
	port (
		a_in : in std_logic;
		b_in : in std_logic;
		pout : out std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_pre is
begin

U1: xor2
	port map (
		A => a_in,
		B => b_in,
		Y => pout
	);

U2: and2
	port map (
		A => a_in,
		B => b_in,
		Y => gout
	);

end architecture;

entity buffer_node is
	port (
		pin : in std_logic;
		pout : out std_logic;
		gin : in std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of buffer_node is
begin

U1: buffer
	port map (
		A => pin,
		Y => pout
	);

U2: buffer
	port map (
		A => gin,
		Y => gout
	);

end architecture;

entity ppa_post is
	port (
		pin : in std_logic;
		gin : in std_logic;
		sum : out std_logic
	);
end entity;

architecture behavior of ppa_post is
begin

U1: xor2
	port map (
		A => pin,
		B => gin,
		Y => sum
	);

end architecture;

entity ppa_grey is
	port (
		gin : in std_logic_vector(1 downto 0);
		gout : out std_logic;
		pin : in std_logic
	);
end entity;

architecture behavior of ppa_grey is
begin

U1: ao21
	port map (
		A0 => gin(0),
		A1 => pin,
		B0 => gin(1),
		Y => gout
	);

end architecture;
