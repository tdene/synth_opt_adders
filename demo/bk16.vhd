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
	signal g2, p11, g5, p10, g10, p4, g4, g12, g0, p5, p3, p_lsb, p9, g7, g3, p2, p14, g11, g13, g_lsb, p1, p6, p8, p12, g1, g14, p7, g6, g9, g8, p13 : std_logic;
	signal n1025, n1028, n1030, n1032, n1033, n1035, n1038, n1040, n1042, n1043, n1051, n1065, n48, n49, n50, n51, n1076, n53, n55, n56, n57, n58, n59, n60, n63, n64, n1089, n67, n68, n69, n70, n71, n72, n75, n76, n1101, n79, n80, n81, n82, n83, n84, n87, n88, n91, n92, n93, n94, n95, n96, n97, n1116, n99, n101, n103, n105, n106, n107, n108, n109, n110, n111, n112, n113, n114, n1130, n117, n118, n1141, n121, n122, n125, n126, n129, n130, n131, n132, n133, n135, n136, n137, n138, n139, n140, n141, n143, n145, n147, n149, n151, n153, n155, n157, n158, n159, n160, n161, n163, n164, n165, n167, n169, n171, n172, n173, n174, n175, n176, n177, n178, n179, n180, n699, n709, n716, n725, n728, n731, n734, n736, n739, n741, n744, n746, n748, n750, n752, n754, n756, n758, n760, n767, n774, n784, n794, n812, n826, n839, n844, n845, n847, n848, n851, n853, n854, n856, n859, n861, n864, n863, n866, n869, n871, n874, n876, n879, n881, n883, n884, n892, n905, n915, n925, n936, n947, n955, n969, n984, n998, n1003, n1004, n1006, n1007, n1009, n1010, n1015, n1012, n1013, n1017, n1018, n1020, n1022, n1023 : std_logic;

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
			gin(0) => n1004,
			pin(0) => p0,
			sum(0) => sum[0]
		);
	ppa_post_1_8: ppa_post
		port map (
			gin(0) => n1007,
			pin(0) => p1,
			sum(0) => sum[1]
		);
	ppa_post_2_8: ppa_post
		port map (
			gin(0) => n1010,
			pin(0) => p2,
			sum(0) => sum[2]
		);
	ppa_post_3_8: ppa_post
		port map (
			gin(0) => n1013,
			pin(0) => p3,
			sum(0) => sum[3]
		);
	ppa_post_4_8: ppa_post
		port map (
			gin(0) => n1015,
			pin(0) => p4,
			sum(0) => sum[4]
		);
	ppa_post_5_8: ppa_post
		port map (
			gin(0) => n1018,
			pin(0) => p5,
			sum(0) => sum[5]
		);
	ppa_post_6_8: ppa_post
		port map (
			gin(0) => n1020,
			pin(0) => p6,
			sum(0) => sum[6]
		);
	ppa_post_7_8: ppa_post
		port map (
			gin(0) => n1023,
			pin(0) => p7,
			sum(0) => sum[7]
		);
	ppa_post_8_8: ppa_post
		port map (
			gin(0) => n1025,
			pin(0) => p8,
			sum(0) => sum[8]
		);
	ppa_post_9_8: ppa_post
		port map (
			gin(0) => n1028,
			pin(0) => p9,
			sum(0) => sum[9]
		);
	ppa_post_10_8: ppa_post
		port map (
			gin(0) => n1030,
			pin(0) => p10,
			sum(0) => sum[10]
		);
	ppa_post_11_8: ppa_post
		port map (
			gin(0) => n1033,
			pin(0) => p11,
			sum(0) => sum[11]
		);
	ppa_post_12_8: ppa_post
		port map (
			gin(0) => n1035,
			pin(0) => p12,
			sum(0) => sum[12]
		);
	ppa_post_13_8: ppa_post
		port map (
			gin(0) => n1038,
			pin(0) => p13,
			sum(0) => sum[13]
		);
	ppa_post_14_8: ppa_post
		port map (
			gin(0) => n1040,
			pin(0) => p14,
			sum(0) => sum[14]
		);
	ppa_post_15_8: ppa_post
		port map (
			gin(0) => n1043,
			pin(0) => p15,
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
			gin(0) => n1043,
			gin(1) => g15,
			pin => p15,
			gout => cout
		);

-- start of tree row 1

	n49 <= p_lsb;
	n48 <= g_lsb;
	ppa_grey_1_1: ppa_grey
		port map (
			gin(0) => g_lsb,
			gin(1) => g0,
			pin(0) => p_lsb,
			gout(0) => n50
		);
	n699 <= p1;
	n51 <= g1;
	ppa_black_3_1: ppa_black
		port map (
			gin(0) => g1,
			gin(1) => g2,
			pin(0) => p1,
			pin(1) => p2,
			gout(0) => n53,
			pout(0) => n0
		);
	n56 <= p3;
	n55 <= g3;
	ppa_black_5_1: ppa_black
		port map (
			gin(0) => g3,
			gin(1) => g4,
			pin(0) => p3,
			pin(1) => p4,
			gout(0) => n57,
			pout(0) => n58
		);
	n60 <= p5;
	n59 <= g5;
	ppa_black_7_1: ppa_black
		port map (
			gin(0) => g5,
			gin(1) => g6,
			pin(0) => p5,
			pin(1) => p6,
			gout(0) => n63,
			pout(0) => n64
		);
	n68 <= p7;
	n67 <= g7;
	ppa_black_9_1: ppa_black
		port map (
			gin(0) => g7,
			gin(1) => g8,
			pin(0) => p7,
			pin(1) => p8,
			gout(0) => n69,
			pout(0) => n70
		);
	n72 <= p9;
	n71 <= g9;
	ppa_black_11_1: ppa_black
		port map (
			gin(0) => g9,
			gin(1) => g10,
			pin(0) => p9,
			pin(1) => p10,
			gout(0) => n75,
			pout(0) => n76
		);
	n80 <= p11;
	n79 <= g11;
	ppa_black_13_1: ppa_black
		port map (
			gin(0) => g11,
			gin(1) => g12,
			pin(0) => p11,
			pin(1) => p12,
			gout(0) => n81,
			pout(0) => n82
		);
	n84 <= p13;
	n83 <= g13;
	ppa_black_15_1: ppa_black
		port map (
			gin(0) => g13,
			gin(1) => g14,
			pin(0) => p13,
			pin(1) => p14,
			gout(0) => n87,
			pout(0) => n88
		);

-- start of tree row 2

	n92 <= n49;
	n91 <= n48;
	n94 <= n0;
	n93 <= n50;
	n812 <= n699;
	n95 <= n51;
	ppa_grey_3_2: ppa_grey
		port map (
			gin(0) => n50,
			gin(1) => n53,
			pin(0) => n0,
			gout(0) => n96
		);
	n709 <= n56;
	n97 <= n55;
	n936 <= n58;
	n99 <= n57;
	n716 <= n60;
	n101 <= n59;
	ppa_black_7_2: ppa_black
		port map (
			gin(0) => n57,
			gin(1) => n63,
			pin(0) => n58,
			pin(1) => n64,
			gout(0) => n103,
			pout(0) => n0
		);
	n106 <= n68;
	n105 <= n67;
	n108 <= n70;
	n107 <= n69;
	n110 <= n72;
	n109 <= n71;
	ppa_black_11_2: ppa_black
		port map (
			gin(0) => n69,
			gin(1) => n75,
			pin(0) => n70,
			pin(1) => n76,
			gout(0) => n111,
			pout(0) => n112
		);
	n114 <= n80;
	n113 <= n79;
	n118 <= n82;
	n117 <= n81;
	n122 <= n84;
	n121 <= n83;
	ppa_black_15_2: ppa_black
		port map (
			gin(0) => n81,
			gin(1) => n87,
			pin(0) => n82,
			pin(1) => n88,
			gout(0) => n125,
			pout(0) => n126
		);

-- start of tree row 3

	n130 <= n92;
	n129 <= n91;
	n132 <= n94;
	n131 <= n93;
	n969 <= n812;
	n133 <= n95;
	n136 <= n0;
	n135 <= n96;
	n826 <= n709;
	n137 <= n97;
	n1101 <= n936;
	n138 <= n99;
	n839 <= n716;
	n139 <= n101;
	ppa_grey_7_3: ppa_grey
		port map (
			gin(0) => n96,
			gin(1) => n103,
			pin(0) => n0,
			gout(0) => n140
		);
	n767 <= n106;
	n141 <= n105;
	n947 <= n108;
	n143 <= n107;
	n774 <= n110;
	n145 <= n109;
	n1141 <= n112;
	n147 <= n111;
	n784 <= n114;
	n149 <= n113;
	n955 <= n118;
	n151 <= n117;
	n794 <= n122;
	n153 <= n121;
	ppa_black_15_3: ppa_black
		port map (
			gin(0) => n111,
			gin(1) => n125,
			pin(0) => n112,
			pin(1) => n126,
			gout(0) => n155,
			pout(0) => n0
		);

-- start of tree row 4

	n158 <= n130;
	n157 <= n129;
	buffer_node_1_4: buffer_node
		port map (
			gin(0) => n131,
			pin(0) => n132,
			gout(0) => n159,
			pout(0) => n160
		);
	n0 <= n969;
	n161 <= n133;
	buffer_node_3_4: buffer_node
		port map (
			gin(0) => n135,
			pin(0) => n136,
			gout(0) => n163,
			pout(0) => n164
		);
	n984 <= n826;
	n165 <= n137;
	n0 <= n1101;
	n167 <= n138;
	n998 <= n839;
	n169 <= n139;
	buffer_node_7_4: buffer_node
		port map (
			gin(0) => n140,
			pin(0) => n0,
			gout(0) => n171,
			pout(0) => n172
		);
	n892 <= n767;
	n173 <= n141;
	n1116 <= n947;
	n174 <= n143;
	n905 <= n774;
	n175 <= n145;
	n0 <= n1141;
	n176 <= n147;
	n915 <= n784;
	n177 <= n149;
	n1130 <= n955;
	n178 <= n151;
	n925 <= n794;
	n179 <= n153;
	ppa_grey_15_4: ppa_grey
		port map (
			gin(0) => n140,
			gin(1) => n155,
			pin(0) => n0,
			gout(0) => n180
		);

-- start of tree row 5

	n844 <= n158;
	n725 <= n157;
	n847 <= n160;
	n728 <= n159;
	ppa_grey_2_5: ppa_grey
		port map (
			gin(0) => n159,
			gin(1) => n161,
			pin(0) => n160,
			gout(0) => n731
		);
	buffer_node_3_5: buffer_node
		port map (
			gin(0) => n163,
			pin(0) => n164,
			gout(0) => n734,
			pout(0) => n853
		);
	n0 <= n984;
	n736 <= n165;
	ppa_grey_5_5: ppa_grey
		port map (
			gin(0) => n163,
			gin(1) => n167,
			pin(0) => n164,
			gout(0) => n739
		);
	n0 <= n998;
	n741 <= n169;
	buffer_node_7_5: buffer_node
		port map (
			gin(0) => n171,
			pin(0) => n172,
			gout(0) => n744,
			pout(0) => n863
		);
	n1051 <= n892;
	n746 <= n173;
	n0 <= n1116;
	n748 <= n174;
	n1065 <= n905;
	n750 <= n175;
	ppa_grey_11_5: ppa_grey
		port map (
			gin(0) => n171,
			gin(1) => n176,
			pin(0) => n172,
			gout(0) => n752
		);
	n1076 <= n915;
	n754 <= n177;
	n0 <= n1130;
	n756 <= n178;
	n1089 <= n925;
	n758 <= n179;
	n883 <= n0;
	n760 <= n180;

-- start of tree row 6

	n1003 <= n844;
	n845 <= n725;
	n1006 <= n847;
	n848 <= n728;
	n1009 <= n850;
	n851 <= n731;
	n1012 <= n853;
	n854 <= n734;
	ppa_grey_4_6: ppa_grey
		port map (
			gin(0) => n734,
			gin(1) => n736,
			pin(0) => n853,
			gout(0) => n856
		);
	n1017 <= n858;
	n859 <= n739;
	ppa_grey_6_6: ppa_grey
		port map (
			gin(0) => n739,
			gin(1) => n741,
			pin(0) => n858,
			gout(0) => n861
		);
	buffer_node_7_6: buffer_node
		port map (
			gin(0) => n744,
			pin(0) => n863,
			gout(0) => n864,
			pout(0) => n1022
		);
	n0 <= n1051;
	n866 <= n746;
	ppa_grey_9_6: ppa_grey
		port map (
			gin(0) => n744,
			gin(1) => n748,
			pin(0) => n863,
			gout(0) => n869
		);
	n0 <= n1065;
	n871 <= n750;
	buffer_node_11_6: buffer_node
		port map (
			gin(0) => n752,
			pin(0) => n873,
			gout(0) => n874,
			pout(0) => n1032
		);
	n0 <= n1076;
	n876 <= n754;
	ppa_grey_13_6: ppa_grey
		port map (
			gin(0) => n752,
			gin(1) => n756,
			pin(0) => n873,
			gout(0) => n879
		);
	n0 <= n1089;
	n881 <= n758;
	n1042 <= n883;
	n884 <= n760;

-- start of tree row 7

	n0 <= n1003;
	n1004 <= n845;
	n0 <= n1006;
	n1007 <= n848;
	n0 <= n1009;
	n1010 <= n851;
	n0 <= n1012;
	n1013 <= n854;
	n0 <= n0;
	n1015 <= n856;
	n0 <= n1017;
	n1018 <= n859;
	n0 <= n0;
	n1020 <= n861;
	n0 <= n1022;
	n1023 <= n864;
	ppa_grey_8_7: ppa_grey
		port map (
			gin(0) => n864,
			gin(1) => n866,
			pin(0) => n1022,
			gout(0) => n1025
		);
	n0 <= n1027;
	n1028 <= n869;
	ppa_grey_10_7: ppa_grey
		port map (
			gin(0) => n869,
			gin(1) => n871,
			pin(0) => n1027,
			gout(0) => n1030
		);
	n0 <= n1032;
	n1033 <= n874;
	ppa_grey_12_7: ppa_grey
		port map (
			gin(0) => n874,
			gin(1) => n876,
			pin(0) => n1032,
			gout(0) => n1035
		);
	n0 <= n1037;
	n1038 <= n879;
	ppa_grey_14_7: ppa_grey
		port map (
			gin(0) => n879,
			gin(1) => n881,
			pin(0) => n1037,
			gout(0) => n1040
		);
	n0 <= n1042;
	n1043 <= n884;

end architecture

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
