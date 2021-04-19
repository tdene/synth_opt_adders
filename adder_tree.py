from modules import modules
from adder_graph import adder_graph as graph
from adder_graph import adder_node as node

# Class that generates parallel prefix adder trees

# Trees are initialized to a serial structures (ripple-carry-like)
# Trees can morph via any of three, reversible, transforms:
# L->F, F->L (R. Zimmermann, Binary Adder Architectures for Cell-Based VLSI and their Synthesis, PhD thesis, Swiss Federal Institute of Technology (ETH) Zurich, Hartung-Gorre Verlag, 1998), L->T, T->L, F->T, T->F

class adder_tree(graph):

    # Pre-condition: width is an integer
    # Post-condition: initializes serial structure

    def __init__(self,width):
        if not isinstance(width,int):
            raise ValueError("provided width must be an integer")
        self.w=width;

        super().__init__(self.w)

        # Initialize P/G nodes:
        for a in range(self.w):
            self.add_node(node(a,0,'pg_node'))

        # Initialize serial structure

        for a in range(1,self.w):
            for b in range(self.w):
                if b!=a:
                    self.add_node(node(b,a,'buffer_node'))
                    self.add_edge(self[b,a-1],('pout',0),self[b,a],('pin',0))
                    self.add_edge(self[b,a-1],('gout',0),self[b,a],('gin',0))
                else:
                    self.add_node(node(b,a,'black'))
                    self.add_edge(self[b-1,a-1],('pout',0),self[b,a],('pin',0))
                    self.add_edge(self[b,a-1],('pout',0),self[b,a],('pin',1))
                    self.add_edge(self[b-1,a-1],('gout',0),self[b,a],('gin',0))
                    self.add_edge(self[b,a-1],('gout',0),self[b,a],('gin',1))

        # Post-processing (in progress)

        for a in range(self.w):
            self.add_node(node(a,self.w,'xor_node'))
            self.add_edge(self[a,self.w-1],('pout',0),self[a,self.w],('pin',0))
            self.add_edge(self[a,self.w-1],('gout',0),self[a,self.w],('gin',0))


    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the y-1 neighbor (P/G logic if already at the top)

    def top(self,n):
        return self[n.x,n.y-1]

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the y+1 neighbor (post-processing logic if already at the bot)

    def bot(self,n):
        return self[n.x,n.y+1]

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the diagonal predecessor (None if this node is a buffer)

    def pre(self,n):
        return [a for a in self.adj[n] if a.x<n.x and a.y<n.y][0]

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the diagonal successor (None if does not exist)

    def post(self,n):
        return [a for a in self.adj[n] if a.x>n.x and a.y>n.y][0]
