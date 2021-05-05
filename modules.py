
# Note that nothing yet exists to check this file
# for checkable errors, such as inputs/outputs
# not matching the logical function

modules={}

### Black cells
black=dict()

black['verilog']="""
module black(gin, pin, gout, pout);

 input [1:0] gin, pin;
 output gout, pout;

 assign pout=pin[1]&pin[0];
 assign gout=gin[1]|(pin[1]&gin[0]);

endmodule
"""

black['shape']='square'
black['color']='black'

# List of inputs represented by (name, bits) tuple
black['ins']=[('gin',2),('pin',2)]

# List of outputs represented by (name, bits) tuple
black['outs']=[('gout',1),('pout',1)]

# Returns function that executes the logic of the module
black['logic'] = lambda gin,pin: [
                 gin[1]|(pin[1]&gin[0]) ,
                 pin[1]&pin[0]
                 ]

modules['black']=black

### Grey cells
grey=dict()

grey['verilog']="""
module grey(gout, gin, pin);

 input[1:0] gin;
 input pin;
 output gout;

 assign gout=gin[1]|(pin&gin[0]);

endmodule
"""

grey['shape']='square'
grey['color']='grey'

# List of inputs represented by (name, bits) tuple
grey['ins']=[('gin',2),('pin',1)]

# List of outputs represented by (name, bits) tuple
grey['outs']=[('gout',1)]

# Returns function that executes the logic of the module
grey['logic'] = lambda gin,pin: [
                gin[1]|(pin&gin[0])
                ]

modules['grey']=grey

### Reduced Black cell
rblk=dict()

rblk['verilog']="""
module rblk(hout, iout, gin, pin);

 input [1:0] gin, pin;
 output hout, iout;

 assign iout=pin[1]&pin[0];
 assign hout=gin[1]|gin[0];

endmodule
"""

rblk['shape']='square'
rblk['color']='black'

# List of inputs represented by (name, bits) tuple
rblk['ins']=[('gin',2),('pin',2)]

# List of outputs represented by (name, bits) tuple
rblk['outs']=[('hout',1),('iout',1)]

# Returns function that executes the logic of the module
rblk['logic'] = lambda gin,pin: [
                gin[1]|gin[0] ,
                pin[1]&pin[0]
                ]

modules['rblk']=rblk

### Reduced Grey cell
rgry=dict()

rgry['verilog']="""
module rgry(hout, gin);

 input[1:0] gin;
 output hout;

 assign hout=gin[1]|gin[0];

endmodule
"""

rgry['shape']='square'
rgry['color']='grey'

# List of inputs represented by (name, bits) tuple
rgry['ins']=[('gin',2)]

# List of outputs represented by (name, bits) tuple
rgry['outs']=[('hout',1)]

# Returns function that executes the logic of the module
rgry['logic'] = lambda gin: [
                gin[1]|gin[0]
                ]

modules['rgry']=rgry

### Buffer nodes
buffer_node=dict()

buffer_node['verilog']="""
module buf(pin, gin, pout, gout);

  input pin, gin;
  output pout, gout;

  assign pout=pin;
  assign gout=gin;

endmodule
"""

buffer_node['shape']='invtriangle'
buffer_node['color']='white'

buffer_node['ins']=[('gin',1),('pin',1)]
buffer_node['outs']=[('gout',1),('pout',1)]

buffer_node['logic'] = lambda x: [x]

modules['buffer_node']=buffer_node

### Invis nodes
invis_node=dict(buffer_node)

invis_node['style']='invis'

modules['invis_node']=invis_node

### P/G generation node
pg_node=dict()

pg_node['verilog']="""
module pg_node(a, b, pout, gout);

    input a, b;
    output pout, gout;

    assign pout=a^b;
    assign gout=a&b;

endmodule
"""

pg_node['shape']='square'
pg_node['color']='white'
pg_node['label']='P/G'
pg_node['style']='dashed'

pg_node['ins']=[('a',1),('b',1)]
pg_node['outs']=[('pout',1),('gout',1)]

pg_node['logic'] = lambda a,b: [
                   a^b,
                   a&b
                   ]

modules['pg_node']=pg_node

### XOR node

xor_node=dict()

xor_node['verilog']="""
    assign s=pin^gin;
"""

xor_node['shape']='invtrapezium'
xor_node['color']='white'
xor_node['style']='dashed'

xor_node['ins']=[('pin',1),('gin',1)]
xor_node['outs']=[('s',1)]

xor_node['logic'] = lambda pin,gin: [pin^gin]

modules['xor_node']=xor_node

###

if __name__=="__main__":

# Note that nothing yet exists to check this file
# for checkable errors, such as inputs/outputs
# not matching the logical function
    raise RuntimeError("This file is importable, but not executable")
