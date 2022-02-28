library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity and2 is
  port (
    A : in std_logic;
    B : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of and2 is
begin
  Y <= A and B;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity and3 is
  port (
    A : in std_logic;
    B : in std_logic;
    C : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of and3 is
begin
  Y <= A and B and C;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity and4 is
  port (
    A : in std_logic;
    B : in std_logic;
    C : in std_logic;
    D : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of and4 is
begin
  Y <= A and B and C and D;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ao21 is
  port (
    A0 : in std_logic;
    A1 : in std_logic;
    B0 : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of ao21 is
begin
  Y <= (A0 and A1) or B0;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ao22 is
  port (
    A0 : in std_logic;
    A1 : in std_logic;
    B0 : in std_logic;
    B1 : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of ao22 is
begin
  Y <= (A0 and A1) or (B0 and B1);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity aoi21 is
  port (
    A0 : in std_logic;
    A1 : in std_logic;
    B0 : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of aoi21 is
begin
  Y <= not ((A0 and A1) or B0);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity aoi22 is
  port (
    A0 : in std_logic;
    A1 : in std_logic;
    B0 : in std_logic;
    B1 : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of aoi22 is
begin
  Y <= not ((A0 and A1) or (B0 and B1));
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity buffer_module is
  port (
    A : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of buffer_module is
begin
  Y <= A;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity inverter is
  port (
    A : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of inverter is
begin
  Y <= not A;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity mux2 is
  port (
    A : in std_logic;
    B : in std_logic;
    S : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of mux2 is
begin
  Y <= B when S = '1' else A;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity muxi2 is
  port (
    A : in std_logic;
    B : in std_logic;
    S : in std_logic;
    Y : out std_logic
  );
end entity; 

begin
  Y <= not (B when S = '1' else A);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nand2 is
  port (
    A : in std_logic;
    B : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of nand2 is
begin
  Y <= not (A and B);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nand2b is
  port (
    A : in std_logic;
    B : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of nand2b is
begin
  Y <= not (not A and B);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nand3 is
  port (
    A : in std_logic;
    B : in std_logic;
    C : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of nand3 is
begin
  Y <= not (A and B and C);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nand4 is
  port (
    A : in std_logic;
    B : in std_logic;
    C : in std_logic;
    D : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of nand4 is
begin
  Y <= not (A and B and C and D);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nor2 is
  port (
    A : in std_logic;
    B : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of nor2 is
begin
  Y <= not (A or B);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nor2b is
  port (
    A : in std_logic;
    B : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of nor2b is
begin
  Y <= not (not A or B);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nor3 is
  port (
    A : in std_logic;
    B : in std_logic;
    C : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of nor3 is
begin
  Y <= not (A or B or C);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity nor4 is
  port (
    A : in std_logic;
    B : in std_logic;
    C : in std_logic;
    D : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of nor4 is
begin
  Y <= not (A or B or C or D);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity oa21 is
  port (
    A0 : in std_logic;
    A1 : in std_logic;
    B0 : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of oa21 is
begin
  Y <= (A0 or A1) and B0;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity oa22 is
  port (
    A0 : in std_logic;
    A1 : in std_logic;
    B0 : in std_logic;
    B1 : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of oa22 is
begin
  Y <= (A0 or A1) and (B0 or B1);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity oai21 is
  port (
    A0 : in std_logic;
    A1 : in std_logic;
    B0 : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of oai21 is
begin
  Y <= not ((A0 or A1) and B0);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity oai22 is
  port (
    A0 : in std_logic;
    A1 : in std_logic;
    B0 : in std_logic;
    B1 : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of oai22 is
begin
  Y <= not (A0 or A1) and (B0 or B1);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity or2 is
  port (
    A : in std_logic;
    B : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of or2 is
begin
  Y <= A or B;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity or3 is
  port (
    A : in std_logic;
    B : in std_logic;
    C : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of or3 is
begin
  Y <= A or B or C;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity or4 is
  port (
    A : in std_logic;
    B : in std_logic;
    C : in std_logic;
    D : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of or4 is
begin
  Y <= A or B or C or D;
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity xnor2 is
  port (
    A : in std_logic;
    B : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of xnor2 is
begin
  Y <= not (A xor B);
end architecture;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity xor2 is
  port (
    A : in std_logic;
    B : in std_logic;
    Y : out std_logic
  );
end entity; 

architecture behavior of xor2 is
begin
  Y <= A xor B;
end architecture;

