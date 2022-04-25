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
	signal p14, p13, p6, p12, p2, g8, p5, g5, p3, g9, p1, p9, p0, g_lsb, g12, p_lsb, g6, g1, g13, g11, p10, g7, g2, g0, g14, p7, p8, g10, g3, g4, p11, p4 : std_logic;
	signal n1025, n1028, n1026, n1029, n1031, n1032, n1034, n1036, n1037, n1039, n1042, n1041, n1044, n1047, n1049, n1051, n1052, n1054, n1057, n1059, n1061, n1062, n48, n49, n50, n51, n52, n54, n55, n1072, n57, n58, n59, n60, n61, n62, n1086, n65, n66, n69, n70, n71, n72, n73, n74, n1097, n77, n78, n81, n82, n83, n84, n85, n86, n1110, n89, n90, n93, n94, n95, n96, n97, n98, n99, n100, n1122, n102, n103, n105, n106, n108, n109, n111, n112, n113, n114, n115, n116, n117, n118, n119, n120, n1137, n123, n124, n127, n128, n1151, n131, n132, n135, n136, n137, n139, n138, n141, n142, n143, n144, n145, n146, n147, n148, n150, n151, n153, n154, n156, n157, n159, n160, n162, n163, n165, n166, n168, n169, n171, n172, n173, n174, n175, n177, n178, n179, n181, n183, n185, n186, n187, n188, n189, n190, n191, n192, n194, n193, n715, n725, n1162, n732, n740, n743, n746, n749, n751, n754, n756, n759, n761, n763, n765, n767, n769, n771, n773, n775, n784, n791, n802, n813, n832, n846, n859, n862, n863, n865, n866, n869, n871, n872, n874, n877, n879, n881, n882, n884, n887, n889, n892, n894, n897, n899, n901, n902, n912, n925, n935, n945, n956, n967, n975, n990, n1005, n1019, n1022, n1023 : std_logic;

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
			gin(0) => n1023,
			pin(0) => p0,
			sum(0) => sum[0]
		);
	ppa_post_1_8: ppa_post
		port map (
			gin(0) => n1026,
			pin(0) => p1,
			sum(0) => sum[1]
		);
	ppa_post_2_8: ppa_post
		port map (
			gin(0) => n1029,
			pin(0) => p2,
			sum(0) => sum[2]
		);
	ppa_post_3_8: ppa_post
		port map (
			gin(0) => n1032,
			pin(0) => p3,
			sum(0) => sum[3]
		);
	ppa_post_4_8: ppa_post
		port map (
			gin(0) => n1034,
			pin(0) => p4,
			sum(0) => sum[4]
		);
	ppa_post_5_8: ppa_post
		port map (
			gin(0) => n1037,
			pin(0) => p5,
			sum(0) => sum[5]
		);
	ppa_post_6_8: ppa_post
		port map (
			gin(0) => n1039,
			pin(0) => p6,
			sum(0) => sum[6]
		);
	ppa_post_7_8: ppa_post
		port map (
			gin(0) => n1042,
			pin(0) => p7,
			sum(0) => sum[7]
		);
	ppa_post_8_8: ppa_post
		port map (
			gin(0) => n1044,
			pin(0) => p8,
			sum(0) => sum[8]
		);
	ppa_post_9_8: ppa_post
		port map (
			gin(0) => n1047,
			pin(0) => p9,
			sum(0) => sum[9]
		);
	ppa_post_10_8: ppa_post
		port map (
			gin(0) => n1049,
			pin(0) => p10,
			sum(0) => sum[10]
		);
	ppa_post_11_8: ppa_post
		port map (
			gin(0) => n1052,
			pin(0) => p11,
			sum(0) => sum[11]
		);
	ppa_post_12_8: ppa_post
		port map (
			gin(0) => n1054,
			pin(0) => p12,
			sum(0) => sum[12]
		);
	ppa_post_13_8: ppa_post
		port map (
			gin(0) => n1057,
			pin(0) => p13,
			sum(0) => sum[13]
		);
	ppa_post_14_8: ppa_post
		port map (
			gin(0) => n1059,
			pin(0) => p14,
			sum(0) => sum[14]
		);
	ppa_post_15_8: ppa_post
		port map (
			gin(0) => n1062,
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
			gin(0) => n1062,
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
			pin(0) => p0,
			gout(0) => n50
		);
	n52 <= p1;
	n51 <= g1;
	ppa_black_3_1: ppa_black
		port map (
			gin(0) => g1,
			gin(1) => g2,
			pin(0) => p1,
			pin(1) => p2,
			gout(0) => n54,
			pout(0) => n55
		);
	n58 <= p3;
	n57 <= g3;
	ppa_black_5_1: ppa_black
		port map (
			gin(0) => g3,
			gin(1) => g4,
			pin(0) => p3,
			pin(1) => p4,
			gout(0) => n59,
			pout(0) => n60
		);
	n62 <= p5;
	n61 <= g5;
	ppa_black_7_1: ppa_black
		port map (
			gin(0) => g5,
			gin(1) => g6,
			pin(0) => p5,
			pin(1) => p6,
			gout(0) => n65,
			pout(0) => n66
		);
	n70 <= p7;
	n69 <= g7;
	ppa_black_9_1: ppa_black
		port map (
			gin(0) => g7,
			gin(1) => g8,
			pin(0) => p7,
			pin(1) => p8,
			gout(0) => n71,
			pout(0) => n72
		);
	n74 <= p9;
	n73 <= g9;
	ppa_black_11_1: ppa_black
		port map (
			gin(0) => g9,
			gin(1) => g10,
			pin(0) => p9,
			pin(1) => p10,
			gout(0) => n77,
			pout(0) => n78
		);
	n82 <= p11;
	n81 <= g11;
	ppa_black_13_1: ppa_black
		port map (
			gin(0) => g11,
			gin(1) => g12,
			pin(0) => p11,
			pin(1) => p12,
			gout(0) => n83,
			pout(0) => n84
		);
	n86 <= p13;
	n85 <= g13;
	ppa_black_15_1: ppa_black
		port map (
			gin(0) => g13,
			gin(1) => g14,
			pin(0) => p13,
			pin(1) => p14,
			gout(0) => n89,
			pout(0) => n90
		);

-- start of tree row 2

	n94 <= n49;
	n93 <= n48;
	n96 <= n0;
	n95 <= n50;
	n715 <= n52;
	n97 <= n51;
	ppa_grey_3_2: ppa_grey
		port map (
			gin(0) => n50,
			gin(1) => n54,
			pin(0) => n55,
			gout(0) => n98
		);
	n100 <= n58;
	n99 <= n57;
	n103 <= n60;
	n102 <= n59;
	n106 <= n62;
	n105 <= n61;
	ppa_black_7_2: ppa_black
		port map (
			gin(0) => n59,
			gin(1) => n65,
			pin(0) => n60,
			pin(1) => n66,
			gout(0) => n108,
			pout(0) => n109
		);
	n112 <= n70;
	n111 <= n69;
	n114 <= n72;
	n113 <= n71;
	n116 <= n74;
	n115 <= n73;
	ppa_black_11_2: ppa_black
		port map (
			gin(0) => n71,
			gin(1) => n77,
			pin(0) => n72,
			pin(1) => n78,
			gout(0) => n117,
			pout(0) => n118
		);
	n120 <= n82;
	n119 <= n81;
	n124 <= n84;
	n123 <= n83;
	n128 <= n86;
	n127 <= n85;
	ppa_black_15_2: ppa_black
		port map (
			gin(0) => n83,
			gin(1) => n89,
			pin(0) => n84,
			pin(1) => n90,
			gout(0) => n131,
			pout(0) => n132
		);

-- start of tree row 3

	n136 <= n94;
	n135 <= n93;
	n138 <= n96;
	n137 <= n95;
	n832 <= n715;
	n139 <= n97;
	n142 <= n0;
	n141 <= n98;
	n725 <= n100;
	n143 <= n99;
	n956 <= n103;
	n144 <= n102;
	n732 <= n106;
	n145 <= n105;
	ppa_grey_7_3: ppa_grey
		port map (
			gin(0) => n98,
			gin(1) => n108,
			pin(0) => n109,
			gout(0) => n146
		);
	n148 <= n112;
	n147 <= n111;
	n151 <= n114;
	n150 <= n113;
	n154 <= n116;
	n153 <= n115;
	n157 <= n118;
	n156 <= n117;
	n160 <= n120;
	n159 <= n119;
	n163 <= n124;
	n162 <= n123;
	n166 <= n128;
	n165 <= n127;
	ppa_black_15_3: ppa_black
		port map (
			gin(0) => n117,
			gin(1) => n131,
			pin(0) => n118,
			pin(1) => n132,
			gout(0) => n168,
			pout(0) => n169
		);

-- start of tree row 4

	n172 <= n136;
	n171 <= n135;
	ppa_buffer_1_4: ppa_buffer
		port map (
			gin(0) => n137,
			pin(0) => n138,
			gout(0) => n173,
			pout(0) => n174
		);
	n990 <= n832;
	n175 <= n139;
	ppa_buffer_3_4: ppa_buffer
		port map (
			gin(0) => n141,
			pin(0) => n142,
			gout(0) => n177,
			pout(0) => n178
		);
	n846 <= n725;
	n179 <= n143;
	n1122 <= n956;
	n181 <= n144;
	n859 <= n732;
	n183 <= n145;
	ppa_buffer_7_4: ppa_buffer
		port map (
			gin(0) => n146,
			pin(0) => n0,
			gout(0) => n185,
			pout(0) => n186
		);
	n784 <= n148;
	n187 <= n147;
	n967 <= n151;
	n188 <= n150;
	n791 <= n154;
	n189 <= n153;
	n1162 <= n157;
	n190 <= n156;
	n802 <= n160;
	n191 <= n159;
	n975 <= n163;
	n192 <= n162;
	n813 <= n166;
	n193 <= n165;
	ppa_grey_15_4: ppa_grey
		port map (
			gin(0) => n146,
			gin(1) => n168,
			pin(0) => n169,
			gout(0) => n194
		);

-- start of tree row 5

	n862 <= n172;
	n740 <= n171;
	n865 <= n174;
	n743 <= n173;
	ppa_grey_2_5: ppa_grey
		port map (
			gin(0) => n173,
			gin(1) => n175,
			pin(0) => n990,
			gout(0) => n746
		);
	ppa_buffer_3_5: ppa_buffer
		port map (
			gin(0) => n177,
			pin(0) => n178,
			gout(0) => n749,
			pout(0) => n871
		);
	n1005 <= n846;
	n751 <= n179;
	ppa_grey_5_5: ppa_grey
		port map (
			gin(0) => n177,
			gin(1) => n181,
			pin(0) => n1122,
			gout(0) => n754
		);
	n1019 <= n859;
	n756 <= n183;
	ppa_buffer_7_5: ppa_buffer
		port map (
			gin(0) => n185,
			pin(0) => n186,
			gout(0) => n759,
			pout(0) => n881
		);
	n912 <= n784;
	n761 <= n187;
	n1137 <= n967;
	n763 <= n188;
	n925 <= n791;
	n765 <= n189;
	ppa_grey_11_5: ppa_grey
		port map (
			gin(0) => n185,
			gin(1) => n190,
			pin(0) => n1162,
			gout(0) => n767
		);
	n935 <= n802;
	n769 <= n191;
	n1151 <= n975;
	n771 <= n192;
	n945 <= n813;
	n773 <= n193;
	n901 <= n0;
	n775 <= n194;

-- start of tree row 6

	n1022 <= n862;
	n863 <= n740;
	n1025 <= n865;
	n866 <= n743;
	n1028 <= n868;
	n869 <= n746;
	n1031 <= n871;
	n872 <= n749;
	ppa_grey_4_6: ppa_grey
		port map (
			gin(0) => n749,
			gin(1) => n751,
			pin(0) => n1005,
			gout(0) => n874
		);
	n1036 <= n876;
	n877 <= n754;
	ppa_grey_6_6: ppa_grey
		port map (
			gin(0) => n754,
			gin(1) => n756,
			pin(0) => n1019,
			gout(0) => n879
		);
	ppa_buffer_7_6: ppa_buffer
		port map (
			gin(0) => n759,
			pin(0) => n881,
			gout(0) => n882,
			pout(0) => n1041
		);
	n1072 <= n912;
	n884 <= n761;
	ppa_grey_9_6: ppa_grey
		port map (
			gin(0) => n759,
			gin(1) => n763,
			pin(0) => n1137,
			gout(0) => n887
		);
	n1086 <= n925;
	n889 <= n765;
	ppa_buffer_11_6: ppa_buffer
		port map (
			gin(0) => n767,
			pin(0) => n891,
			gout(0) => n892,
			pout(0) => n1051
		);
	n1097 <= n935;
	n894 <= n769;
	ppa_grey_13_6: ppa_grey
		port map (
			gin(0) => n767,
			gin(1) => n771,
			pin(0) => n1151,
			gout(0) => n897
		);
	n1110 <= n945;
	n899 <= n773;
	n1061 <= n901;
	n902 <= n775;

-- start of tree row 7

	n0 <= n1022;
	n1023 <= n863;
	n0 <= n1025;
	n1026 <= n866;
	n0 <= n1028;
	n1029 <= n869;
	n0 <= n1031;
	n1032 <= n872;
	n0 <= n0;
	n1034 <= n874;
	n0 <= n1036;
	n1037 <= n877;
	n0 <= n0;
	n1039 <= n879;
	n0 <= n1041;
	n1042 <= n882;
	ppa_grey_8_7: ppa_grey
		port map (
			gin(0) => n882,
			gin(1) => n884,
			pin(0) => n1072,
			gout(0) => n1044
		);
	n0 <= n1046;
	n1047 <= n887;
	ppa_grey_10_7: ppa_grey
		port map (
			gin(0) => n887,
			gin(1) => n889,
			pin(0) => n1086,
			gout(0) => n1049
		);
	n0 <= n1051;
	n1052 <= n892;
	ppa_grey_12_7: ppa_grey
		port map (
			gin(0) => n892,
			gin(1) => n894,
			pin(0) => n1097,
			gout(0) => n1054
		);
	n0 <= n1056;
	n1057 <= n897;
	ppa_grey_14_7: ppa_grey
		port map (
			gin(0) => n897,
			gin(1) => n899,
			pin(0) => n1110,
			gout(0) => n1059
		);
	n0 <= n1061;
	n1062 <= n902;

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

entity ppa_buffer is
	port (
		pin : in std_logic;
		pout : out std_logic;
		gin : in std_logic;
		gout : out std_logic
	);
end entity;

architecture behavior of ppa_buffer is
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
