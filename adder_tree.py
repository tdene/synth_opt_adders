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
    # Post-condition: returns the next-highest non-buffer neighbor

    def r_top(self,n):
        return (self.top(n) if self.top(n).m!="buffer_node" else self.r_top(self.top(n)))

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the y+1 neighbor (post-processing logic if already at the bot)

    def bot(self,n):
        return self[n.x,n.y+1]

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the next-lowest non-buffer neighbor

    def r_bot(self,n):
        return (self.bot(n) if self.bot(n).m!="buffer_node" else self.r_bot(self.bot(n)))

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the diagonal predecessor (None if this node is a buffer)

    def pre(self,n):
        return next(iter([a for a in self.adj[n] if a.x<n.x and a.y<n.y]),None)

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the list of diagonal successors

    def post(self,n):
        return [a for a in self.adj[n] if a.x>n.x and a.y>n.y]

    # Helper function that checks whether a node is "below" a second node
    # Same column, higher row, or second node straight-up does not exist

    def _is_below(self,n1,n2):
        return (n2 is None) or (n1 is not None and n2.y==n1.y and n2.x>n1.x)

    # Pre-condition: x,y are valid co-ordinates
    # (if y is not provided, searches entire column from bottom-up)
    # Post-condition: checks whether the given x,y node satisfies the transform's
    # initial requirements; if so, returns the two transform pivots

    def _checkLF(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise ValueError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=_checkLF(self,x,a)
                if b is not None:
                    return a,b

        # Main clause of the function
        a = self[x][y]
        # ∃ b = pre(a)
        b = self.pre(a)
        if not node._exists(b):
            return (None,None)
        # ∄ top(a), top(top(a))
        if node._exists(self.top(a)) or node._exists(self.top(self.top(a))):
            return (None,None)
        # ∄ top(b)
        if node._exists(self.top(b)):
            return (None,None)

        return (a,b)

    def _checkFL(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise ValueError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=_checkFL(self,x,a)
                if b is not None:
                    return a,b

        # Main clause of the function
        a = self[x][y]
        # ∃ b s.t pre(a)=pre(b),
        b = next(iter([x for x in self.post(a) if x is not a]),None)
        if b is None:
            return (None,None)
        # b is below pre(top(a))
        if not self._is_below(pre(top(a)),b):
            return (None,None)
        # ∄ bot(a) or ∄ pre(a)
        if node._exists(self.bot(a)) and node._exists(self.pre(a)):
            return (None,None)

        return (a,b)

    def _checkTF(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise ValueError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=_checkTF(self,x,a)
                if b is not None:
                    return a,b

        # Main clause of the function
        a = self[x][y]

        ### Ugly condition
        # ∃ b s.t pre(a) is below pre(b), r_bot(b).y>=a.y
        b = None; tmp = self.pre(a)
        while tmp.y>0:
            tmp = self.top(tmp)
            for x in self.post(tmp):
                if self.r_bot(x).y >= a.y:
                    b=x; break;
        if b is None:
            return (None,None)
        # if r_bot(b).y==a.y, pre(r_bot(a)) is below pre(pre(a)):
        if self.r_bot(b).y==a.y and not self._is_below(self.pre(self.pre(a)),self.pre(r_bot(a))):
            return (None,None)

        return (a,b)

    def _checkFT(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise ValueError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=_checkFT(self,x,a)
                if b is not None:
                    return a,b

        # Main clause of the function
        a = self[x][y]
        # ∃ b s.t pre(a)=pre(b),
        b = next(iter([x for x in self.post(a) if x is not a]),None)
        if b is None:
            return (None,None)
        # ∄ top(b)
        if node._exists(self.top(b)):
            return (None,None)

        return (a,b)

    def _checkLT(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise ValueError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=_checkLT(self,x,a)
                if b is not None:
                    return a,b

        # Main clause of the function
        a = self[x][y]
        # ∃ b = pre(a)
        b = self.pre(a)
        if not node._exists(b):
            return (None,None)
        # ∄ top(a), top(top(a))
        if node._exists(self.top(a)) or node._exists(self.top(self.top(a))):
            return (None,None)
        # ∄ top(b)
        if node._exists(self.top(b)):
            return (None,None)

        return (a,b)

    def _checkTL(self,x,y=None): 
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise ValueError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=_checkTL(self,x,a)

                if b is not None:
                    return a,b

        # Main clause of the function
        a = self[x][y]

        ### Ugly condition
        # ∃ b s.t pre(a) is below pre(b), r_bot(b).y>=a.y
        b = None; tmp = self.pre(a)
        while tmp.y>0:
            tmp = self.top(tmp)
            for x in self.post(tmp):
                if self.r_bot(x).y >= a.y:
                    b=x; break;
        if b is None:
            return (None,None)
        # if r_bot(b).y==a.y, pre(r_bot(a)) is below pre(pre(a)):
        if self.r_bot(b).y==a.y and not self._is_below(self.pre(self.pre(a)),self.pre(r_bot(a))):
            return (None,None)
        # ∄ bot(a) or ∄ pre(a)
        if node._exists(self.bot(a)) and node._exists(self.pre(a)):
            return (None,None)

        return (a,b)
