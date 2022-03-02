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

\tand2 U1(pout,pin[1],pin[0]);
\tao21 U2(gout,gin[0],pin[1],gin[1]);

endmodule
"""

ppa_black['shape']='square'
ppa_black['fillcolor']='black'

# List of inputs represented by (name, bits, diagonal_bits) tuple
ppa_black['ins']=[('gin',2,1),('pin',2,1)]

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

\tao21 U1(gout,gin[0],pin,gin[1]);

endmodule
"""

ppa_grey['shape']='square'
ppa_grey['fillcolor']='grey'

# List of inputs represented by (name, bits, diagonal_bits) tuple
ppa_grey['ins']=[('gin',2,1),('pin',1,1)]

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
module ppaL_black(gout, pout, gin, pin);

\tinput [1:0] gin, pin;
\toutput gout, pout;

\tand2 U1(pout,pin[0],pin[1]);
\tor2 U2(gout,gin[0],gin[1]);

endmodule
"""

ppaL_black['shape']='square'
ppaL_black['fillcolor']='ppa_black'

# List of inputs represented by (name, bits, diagonal_bits) tuple
ppaL_black['ins']=[('gin',2,1),('pin',2,1)]

# List of outputs represented by (name, bits) tuple
ppaL_black['outs']=[('gout',1),('pout',1)]

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
module ppaL_grey(gout, gin);

\tinput[1:0] gin;
\toutput gout;

\tor2 U1(gout,gin[0],gin[1]);

endmodule
"""

ppaL_grey['shape']='square'
ppaL_grey['fillcolor']='ppa_grey'

# List of inputs represented by (name, bits, diagonal_bits) tuple
ppaL_grey['ins']=[('gin',2,1)]

# List of outputs represented by (name, bits) tuple
ppaL_grey['outs']=[('gout',1)]

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

\tbuffer U1(pout,pin);
\tbuffer U2(gout,gin);

endmodule
"""

buffer_node['shape']='invtriangle'
buffer_node['fillcolor']='white'

buffer_node['ins']=[('gin',1,0),('pin',1,0)]
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

invis_node['verilog']="""
module invis_node(pin, gin, pout, gout);

\tinput pin, gin;
\toutput pout, gout;

\tassign pout = pin;
\tassign gout = gin;

endmodule
"""

#invis_node['style']='invis'
invis_node['shape']='point'
invis_node['fixedsize']='shape'
invis_node['width']=0
invis_node['height']=0
invis_node['fillcolor']='black'

invis_node['ins']=[('gin',1,0),('pin',1,0)]
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

\txor2 U1(pout,a_in,b_in);
\tand2 U2(gout,a_in,b_in);

endmodule
"""

ppa_pre['shape']='square'
ppa_pre['fillcolor']='white'
ppa_pre['label']='pre'
ppa_pre['style']='dashed'

ppa_pre['ins']=[('a_in',1,0),('b_in',1,0)]
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

ppa_first_pre['ins']=[('cin',1,0)]

ppa_first_pre['logic'] = lambda cin: [0,cin]

modules['ppa_first_pre']=ppa_first_pre

### Post-processing node

ppa_post=dict()

ppa_post['verilog']="""
module ppa_post(pin, gin, sum);

\tinput pin, gin;
\toutput sum;

\txor2 U1(sum,pin,gin);

endmodule
"""

ppa_post['shape']='invtrapezium'
ppa_post['fillcolor']='white'
ppa_post['label']='post'
ppa_post['style']='dashed'
ppa_post['fixedsize']='shape'

ppa_post['ins']=[('gin',1,0),('pin',1,1)]
ppa_post['outs']=[('sum',1)]

ppa_post['logic'] = lambda pin,gin: [pin^gin]
 
ppa_post['pd'] = 9/3
ppa_post['le'] = 9/3

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
