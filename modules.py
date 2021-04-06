
# Note that nothing yet exists to check this file
# for checkable errors, such as inputs/outputs
# not matching the logical function

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

black['fig']='O'

# List of inputs represented by (name, bits) tuple
black['ins']=[('gin',2),('pin',2)]

# List of outputs represented by (name, bits) tuple
black['outs']=[('gout',1),('pout',1)]

# Returns function that executes the logic of the module
black['logic'] = lambda gin,pin: [
                 gin[1]|(pin[1]&gin[0]) ,
                 pin[1]&pin[0]
                 ]

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

grey['fig']='X'

# List of inputs represented by (name, bits) tuple
grey['ins']=[('gin',2),('pin',1)]

# List of outputs represented by (name, bits) tuple
grey['outs']=[('gout',1)]

# Returns function that executes the logic of the module
grey['logic'] = lambda gin,pin: [
                gin[1]|(pin&gin[0])
                ]

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

rblk['fig']='O'

# List of inputs represented by (name, bits) tuple
rblk['ins']=[('gin',2),('pin',2)]

# List of outputs represented by (name, bits) tuple
rblk['outs']=[('hout',1),('iout',1)]

# Returns function that executes the logic of the module
rblk['logic'] = lambda gin,pin: [
                gin[1]|gin[0] ,
                pin[1]&pin[0]
                ]

### Reduced Grey cell
rgry=dict()

rgry['verilog']="""
module rgry(hout, gin);

 input[1:0] gin;
 output hout;

 assign hout=gin[1]|gin[0];

endmodule
"""

rgry['fig']='X'

# List of inputs represented by (name, bits) tuple
rgry['ins']=[('gin',2)]

# List of outputs represented by (name, bits) tuple
rgry['outs']=[('hout',1)]

# Returns function that executes the logic of the module
rgry['logic'] = lambda gin: [
                gin[1]|gin[0]
                ]

### 'input' nodes
adder_input=dict()

adder_input['fig']=''

adder_input['logic'] = lambda x: [x]


### Buffer nodes
buffer_node=dict()

buffer_node['fig']='V'

buffer_node['logic'] = lambda x: [x]

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
