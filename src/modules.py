
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
black['fillcolor']='black'

# List of inputs represented by (name, bits) tuple
black['ins']=[('gin',2),('pin',2)]

# List of outputs represented by (name, bits) tuple
black['outs']=[('gout',1),('pout',1)]

# Returns function that executes the logic of the module
black['logic'] = lambda gin,pin: [
                 gin[1]|(pin[1]&gin[0]) ,
                 pin[1]&pin[0]
                 ]

black['pd'] = 7.5/3
black['le'] = 5.0/3
black['diag_le'] = 6.0/3

modules['black']=black

### Grey cells
grey=dict()

grey['verilog']="""
module grey(gin, pin, gout);

    input[1:0] gin;
    input pin;
    output gout;

    assign gout=gin[1]|(pin&gin[0]);

endmodule
"""

grey['shape']='square'
grey['fillcolor']='grey'

# List of inputs represented by (name, bits) tuple
grey['ins']=[('gin',2),('pin',1)]

# List of outputs represented by (name, bits) tuple
grey['outs']=[('gout',1)]

# Returns function that executes the logic of the module
grey['logic'] = lambda gin,pin: [
                gin[1]|(pin&gin[0])
                ]

grey['pd'] = 7.5/3
grey['le'] = 2

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
rblk['fillcolor']='black'

# List of inputs represented by (name, bits) tuple
rblk['ins']=[('gin',2),('pin',2)]

# List of outputs represented by (name, bits) tuple
rblk['outs']=[('hout',1),('iout',1)]

# Returns function that executes the logic of the module
rblk['logic'] = lambda gin,pin: [
                gin[1]|gin[0] ,
                pin[1]&pin[0]
                ]

rblk['pd'] = 5/3
rblk['le'] = 2

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
rgry['fillcolor']='grey'

# List of inputs represented by (name, bits) tuple
rgry['ins']=[('gin',2)]

# List of outputs represented by (name, bits) tuple
rgry['outs']=[('hout',1)]

# Returns function that executes the logic of the module
rgry['logic'] = lambda gin: [
                gin[1]|gin[0]
                ]

rgry['pd'] = 5/3
rgry['le'] = 2

modules['rgry']=rgry

### Buffer nodes
buffer_node=dict()

buffer_node['verilog']="""
module buffer_node(pin, gin, pout, gout);

    input pin, gin;
    output pout, gout;

    assign pout=pin;
    assign gout=gin;

endmodule
"""

buffer_node['shape']='invtriangle'
buffer_node['fillcolor']='white'

buffer_node['ins']=[('gin',1),('pin',1)]
buffer_node['outs']=[('gout',1),('pout',1)]

buffer_node['logic'] = lambda pin,gin: [pin,gin]

buffer_node['pd'] = 0
buffer_node['le'] = 0

modules['buffer_node']=buffer_node

### Invis nodes
invis_node=dict()

invis_node['verilog']=buffer_node['verilog'].replace('buffer','invis')

#invis_node['style']='invis'
invis_node['shape']='point'
invis_node['fixedsize']='shape'
invis_node['width']=0
invis_node['height']=0
invis_node['fillcolor']='black'

invis_node['ins']=[('gin',1),('pin',1)]
invis_node['outs']=[('gout',1),('pout',1)]

invis_node['logic'] = lambda pin,gin: [pin,gin]

invis_node['pd'] = buffer_node['pd']
invis_node['le'] = buffer_node['le']

modules['invis_node']=invis_node

### Pre-processing node
pre_node=dict()

pre_node['verilog']="""
module pre_node(a_in, b_in, pout, gout);

    input a_in, b_in;
    output pout, gout;

    assign pout=a_in^b_in;
    assign gout=a_in&b_in;

endmodule
"""

pre_node['shape']='square'
pre_node['fillcolor']='white'
pre_node['label']='pre'
pre_node['style']='dashed'

pre_node['ins']=[('a_in',1),('b_in',1)]
pre_node['outs']=[('pout',1),('gout',1)]

pre_node['logic'] = lambda a,b: [
                   a^b,
                   a&b
                   ]

pre_node['pd'] = 9/3
pre_node['le'] = 9/3

modules['pre_node']=pre_node

### Fake pre-processing node
fake_pre=dict(pre_node)

fake_pre['verilog']="""
module fake_pre(cin, pout, gout);

    input cin;
    output pout, gout;

    assign pout=1'b0;
    assign gout=cin;

endmodule
"""

fake_pre['ins']=[('cin',1)]

fake_pre['logic'] = lambda cin: [0,cin]

modules['fake_pre']=fake_pre

### XOR node

xor_node=dict()

xor_node['verilog']="""
module xor_node(pin, gin, sum);

    input pin, gin;
    output sum;

    assign sum=pin^gin;

endmodule
"""

xor_node['shape']='invtrapezium'
xor_node['fillcolor']='white'
xor_node['style']='dashed'
xor_node['label']='XOR'
xor_node['fixedsize']='shape'

xor_node['ins']=[('pin',1),('gin',1)]
xor_node['outs']=[('sum',1)]

xor_node['logic'] = lambda pin,gin: [pin^gin]
 
xor_node['pd'] = 9/3
xor_node['le'] = 9/3

modules['xor_node']=xor_node

### Post-processing node

post_node=dict(xor_node)

post_node['verilog']=post_node['verilog'].replace('xor_node','post_node')
post_node['label']='post'

modules['post_node']=post_node


if __name__=="__main__":

# Note that nothing yet exists to check this file
# for checkable errors, such as inputs/outputs
# not matching the logical function
    raise RuntimeError("This file is importable, but not executable")
