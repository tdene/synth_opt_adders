# Note that nothing yet exists to check this file
# for checkable errors, such as inputs/outputs
# not matching the logical function

modules={}

### Black cell
ppa_black=dict()

ppa_black['verilog']="""
module ppa_black(gin, pin, gout, pout);

\tinput [1:0] gin, pin;
\toutput gout, pout;

\tassign pout=pin[1]&pin[0];
\tassign gout=gin[1]|(pin[1]&gin[0]);

endmodule
"""

ppa_black['shape']='square'
ppa_black['fillcolor']='black'

# List of inputs represented by (name, bits) tuple
ppa_black['ins']=[('gin',2),('pin',2)]

# List of outputs represented by (name, bits) tuple
ppa_black['outs']=[('gout',1),('pout',1)]

# Returns function that executes the logic of the module
ppa_black['logic'] = lambda gin,pin: [
                 gin[1]|(pin[1]&gin[0]),
                 pin[1]&pin[0]
                 ]

# What section of the tree is this cell in?
# Pre, post, or main?
ppa_black['type']='main'

# Is this cell a buffer?
ppa_black['buf']=False

# Is this just a fake, helper, cell?
ppa_black['exists']=True

# Logical effort
ppa_black['pd'] = 7.5/3
ppa_black['le'] = 5.0/3
ppa_black['diag_le'] = 6.0/3

modules['ppa_black']=ppa_black

### Grey cells
ppa_grey=dict()

ppa_grey['verilog']="""
module ppa_grey(gin, pin, gout);

\tinput[1:0] gin;
\tinput pin;
\toutput gout;

\tassign gout=gin[1]|(pin&gin[0]);

endmodule
"""

ppa_grey['shape']='square'
ppa_grey['fillcolor']='grey'

# List of inputs represented by (name, bits) tuple
ppa_grey['ins']=[('gin',2),('pin',1)]

# List of outputs represented by (name, bits) tuple
ppa_grey['outs']=[('gout',1)]

# Returns function that executes the logic of the module
ppa_grey['logic'] = lambda gin,pin: [
                gin[1]|(pin&gin[0])
                ]

ppa_grey['pd'] = 7.5/3
ppa_grey['le'] = 2

# What section of the tree is this cell in?
# Pre, post, or main?
ppa_grey['type']='main'

# Is this cell a buffer?
ppa_grey['buf']=False

# Is this just a fake, helper, cell?
ppa_grey['exists']=True

modules['ppa_grey']=ppa_grey

### Reduced Black cell
ppaL_black=dict()

ppaL_black['verilog']="""
module ppaL_black(hout, iout, gin, pin);

\tinput [1:0] gin, pin;
\toutput hout, iout;

\tassign iout=pin[1]&pin[0];
\tassign hout=gin[1]|gin[0];

endmodule
"""

ppaL_black['shape']='square'
ppaL_black['fillcolor']='ppa_black'

# List of inputs represented by (name, bits) tuple
ppaL_black['ins']=[('gin',2),('pin',2)]

# List of outputs represented by (name, bits) tuple
ppaL_black['outs']=[('hout',1),('iout',1)]

# Returns function that executes the logic of the module
ppaL_black['logic'] = lambda gin,pin: [
                gin[1]|gin[0],
                pin[1]&pin[0]
                ]

ppaL_black['pd'] = 5/3
ppaL_black['le'] = 2

# What section of the tree is this cell in?
# Pre, post, or main?
ppaL_black['type']='main'

# Is this cell a buffer?
ppaL_black['buf']=False

# Is this just a fake, helper, cell?
ppaL_black['exists']=True

modules['ppaL_black']=ppaL_black

### Reduced Grey cell
ppaL_grey=dict()

ppaL_grey['verilog']="""
module ppaL_grey(hout, gin);

\tinput[1:0] gin;
\toutput hout;

\tassign hout=gin[1]|gin[0];

endmodule
"""

ppaL_grey['shape']='square'
ppaL_grey['fillcolor']='ppa_grey'

# List of inputs represented by (name, bits) tuple
ppaL_grey['ins']=[('gin',2)]

# List of outputs represented by (name, bits) tuple
ppaL_grey['outs']=[('hout',1)]

# Returns function that executes the logic of the module
ppaL_grey['logic'] = lambda gin: [
                gin[1]|gin[0]
                ]

ppaL_grey['pd'] = 5/3
ppaL_grey['le'] = 2

# What section of the tree is this cell in?
# Pre, post, or main?
ppaL_grey['type']='main'

# Is this cell a buffer?
ppaL_grey['buf']=False

# Is this just a fake, helper, cell?
ppaL_grey['exists']=True

modules['ppaL_grey']=ppaL_grey

### Buffer nodes
buffer_node=dict()

buffer_node['verilog']="""
module buffer_node(pin, gin, pout, gout);

\tinput pin, gin;
\toutput pout, gout;

\tassign pout=pin;
\tassign gout=gin;

endmodule
"""

buffer_node['shape']='invtriangle'
buffer_node['fillcolor']='white'

buffer_node['ins']=[('gin',1),('pin',1)]
buffer_node['outs']=[('gout',1),('pout',1)]

buffer_node['logic'] = lambda pin,gin: [pin,gin]

buffer_node['pd'] = 0
buffer_node['le'] = 0

# What section of the tree is this cell in?
# Pre, post, or main?
buffer_node['type']='main'

# Is this cell a buffer?
buffer_node['buf']=True

# Is this just a fake, helper, cell?
buffer_node['exists']=True

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

# What section of the tree is this cell in?
# Pre, post, or main?
invis_node['type']='main'

# Is this cell a buffer?
invis_node['buf']=True

# Is this just a fake, helper, cell?
invis_node['exists']=False

modules['invis_node']=invis_node

### Pre-processing node
ppa_pre=dict()

ppa_pre['verilog']="""
module ppa_pre(a_in, b_in, pout, gout);

\tinput a_in, b_in;
\toutput pout, gout;

\tassign pout=a_in^b_in;
\tassign gout=a_in&b_in;

endmodule
"""

ppa_pre['shape']='square'
ppa_pre['fillcolor']='white'
ppa_pre['label']='pre'
ppa_pre['style']='dashed'

ppa_pre['ins']=[('a_in',1),('b_in',1)]
ppa_pre['outs']=[('pout',1),('gout',1)]

ppa_pre['logic'] = lambda a,b: [
                   a^b,
                   a&b
                   ]

ppa_pre['pd'] = 9/3
ppa_pre['le'] = 9/3

# What section of the tree is this cell in?
# Pre, post, or main?
ppa_pre['type']='pre'

# Is this cell a buffer?
ppa_pre['buf']=False

# Is this just a fake, helper, cell?
ppa_pre['exists']=True

modules['ppa_pre']=ppa_pre

### Fake pre-processing node
ppa_first_pre=dict(ppa_pre)

ppa_first_pre['verilog']="""
module ppa_first_pre(cin, pout, gout);

\tinput cin;
\toutput pout, gout;

\tassign pout=1'b0;
\tassign gout=cin;

endmodule
"""

ppa_first_pre['ins']=[('cin',1)]

ppa_first_pre['logic'] = lambda cin: [0,cin]

modules['ppa_first_pre']=ppa_first_pre

### XOR node

xor_node=dict()

xor_node['verilog']="""
module xor_node(pin, gin, sum);

\tinput pin, gin;
\toutput sum;

\tassign sum=pin^gin;

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

ppa_post=dict(xor_node)

ppa_post['verilog']=ppa_post['verilog'].replace('xor_node','ppa_post')
ppa_post['label']='post'

# What section of the tree is this cell in?
# Pre, post, or main?
ppa_post['type']='post'

# Is this cell a buffer?
ppa_post['buf']=False

# Is this just a fake, helper, cell?
ppa_post['exists']=True

modules['ppa_post']=ppa_post


if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
