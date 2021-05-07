from modules import modules
from adder_graph import adder_graph as graph
from adder_graph import adder_node as node
import networkx as nx
import pydot

# Class that generates parallel prefix adder trees

# Trees are initialized to a serial structures (ripple-carry-like)
# Trees can morph via any of three, reversible, transforms:
# L->F, F->L, L->T, T->L, F->T, T->F

# L <-> F was discussed in
# R. Zimmermann, Binary Adder Architectures for Cell-Based VLSI and their Synthesis, PhD thesis, Swiss Federal Institute of Technology (ETH) Zurich, Hartung-Gorre Verlag, 1998
#  J. P. Fishburn. A depth-decreasing heuristic for combinational logic; or how to convert a ripple-carry adder into a carrylookahead adder or anything in-between. In Proc. 27th Design Automation Conf., pages 361–364, 1990

class adder_tree(graph):

    # Pre-condition: width is an integer
    # Post-condition: initializes serial structure

    def __init__(self,width):
        if not isinstance(width,int):
            raise TypeError("provided width must be an integer")

        super().__init__(width)

        # Initialize P/G nodes:
        for a in range(self.w):
            self.add_node(node(a,0,'pg_node'))

        # Initialize serial structure

        for a in range(1,self.w):
            for b in range(self.w):
                if b!=a:
                    self.add_node(node(b,a,'invis_node'))
                else:
                    self.add_node(node(b,a,'black'),pre=self[b-1,a-1])

        # Post-processing (in progress)

        for a in range(self.w):
            self.add_node(node(a,self.w,'xor_node'))

    # Pre-condition: n is a valid new node; pre is either None or a node in the graph
    # Post-condition: adds node into graph and connects it correctly

    def add_node(self,n,pre=None):

        if pre is not None and not isinstance(pre,node):
            raise TypeError("provided predecessor node must be a node")

    # Calls on super-method
        super().add_node(n)

    # Keeps track of group propagates/generates
        n.group=[0]*self.w
    # Initialize if node is P/G node
        if n.m in ['pg_node']:
            n.group[n.x]=1

    # Connects up
        self._add_top(n)
    # Connects diagonally
        self._add_pre(n,pre)

    # Connects down
        if self.bot(n) is not None:
            self._add_top(self.bot(n))

    # Internal helper function to prevent re-writing of code
    # Connects node to its upper neighbor

    def _add_top(self,n,pre=None):

        top = self.top(n)
        if top is None: return

        if 'pin' in n.ins and 'pout' in top.outs:
            pos=len(n.ins['pin'])-1
            self.add_edge(top,('pout',0),n,('pin',pos))
        if 'gin' in n.ins and 'gout' in top.outs:
            pos=len(n.ins['gin'])-1
            self.add_edge(top,('gout',0),n,('gin',pos))

        n.group = [x|y for x,y in zip(n.group,top.group)]

    # Internal helper function to prevent re-writing of code
    # Connects node to a predecessor

    def _add_pre(self,n,pre):

        if pre is None: return

        if 'pin' in n.ins and len(n.ins['pin'])>1:
            self.add_edge(pre,('pout',0),n,('pin',0))
        if 'gin' in n.ins and len(n.ins['pin'])>1:
            self.add_edge(pre,('gout',0),n,('gin',0))

        n.group = [x|y for x,y in zip(n.group,pre.group)]

    # Internal function to morph a buffer node to invis

    def _buf_to_invis(self,n):
        post = self.post(n)
        if not node._isbuf(n):
            return
        self.remove_node(n)
        inv = node(n.x,n.y,'invis_node')
        self.add_node(inv)
        for x in post:
            self._add_pre(x,inv)
        return inv

    # Pre-condition: n is a node in the graph; its intended destination is invis
    # Post-condition: n shifts to its intended destination with its full connections
    # n's original location now contains an invis

# As of the invis/buffer overhaul of commit c0363d063, wire_remaps are automatic
#    def shift_node(self, n, fun=None, new_pre=None, wire_remap=False):
    def shift_node(self, n, fun=None, new_pre=None):

        if fun==None:
            fun=self.top

        # Grab the invis we're swapping with
        inv=fun(n)

        if n not in self:
            raise ValueError("trying to shift a node not in the graph")
        if node._exists(inv):
            raise ValueError("can only shift node into invis")

        # Save pre/post
        pre = self.pre(n)
        post = self.post(n)
        invpost = self.post(inv)

        # We need to take this opportunity to shift the wire
        # Note that this requires fun(pre).y = inv.y-1
        # This second condition will never matter if we are only shifting by 1
        # But for future support, it is still stated
        if (pre is not None):
            pre = fun(pre)

        # Run pre/post error checks
        if pre is not None and pre.y>=inv.y:
            raise ValueError("cannot shift node past predecessor")
        for x in post:
            if x.y<=inv.y:
                raise ValueError("cannot shift node past successor")

        # Remove nodes from graph
        self.remove_node(n)
        self.remove_node(inv)

        # Re-label x/y of nodes
        tmp = n.x; n.x = inv.x; inv.x = tmp; del tmp;
        tmp = n.y; n.y = inv.y; inv.y = tmp; del tmp;

        # Clean edge info (should be re-written to use remove_edge)
        inv.ins={x:[None]*len(inv.ins[x]) for x in inv.ins}
        inv.outs={x:[None]*len(inv.outs[x]) for x in inv.outs}
        n.ins={x:[None]*len(n.ins[x]) for x in n.ins}
        n.outs={x:[None]*len(n.outs[x]) for x in n.outs}

        # If new_pre is provided, use that, not what we calculate
        pre = new_pre if new_pre is not None else pre

        # if ∃ post(n):
        # add buffer instead of inv; pre(post(n))=buf
        if len(post)>0:
            inv = node(inv.x,inv.y,'buffer_node')

        # Re-add nodes into graph
        if inv.y>n.y:
            self.add_node(n,pre=pre)
            self.add_node(inv)
        else:
            self.add_node(inv)
            self.add_node(n,pre=pre)

        # Re-draw connections to node
        for x in post:
            self._add_pre(x,inv)
        for x in invpost:
            self._add_pre(x,n)

        return n

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the y-1 neighbor (P/G logic if already at the top)

    def top(self,n):
        if n is None or n.y==0:
            return None
        return self[n.x,n.y-1]

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the next-highest non-invis neighbor

    def r_top(self,n):
        return (self.top(n) if node._exists(self.top(n)) else self.r_top(self.top(n)))

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the y+1 neighbor (post-processing logic if already at the bot)

    def bot(self,n):
        if n is None or n.y+1==len(self.node_list):
            return None
        return self[n.x,n.y+1]

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the next-lowest non-invis neighbor

    def r_bot(self,n):
        return (self.bot(n) if node._exists(self.bot(n)) else self.r_bot(self.bot(n)))

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the diagonal predecessor (or top(n) if n is a buffer)

    def pre(self,n):
        return next(iter([a for a in self.adj[n] if a.y<n.y and (a.x<n.x or node._isbuf(n))]),None)

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the list of diagonal successors

    def post(self,n):
        return [a for a in self.adj[n] if a.y>n.y and a.x>n.x]

    # Helper function that checks whether a node is "below" a second node
    # Same column, higher row, or second node straight-up does not exist

    def _is_below(self,n1,n2):
        return (n2 is None) or (n1 is not None and n2.x==n1.x and n2.y>n1.y)

    # Pre-condition: x,y are valid co-ordinates
    # (if y is not provided, searches entire column from bottom-up)
    # Post-condition: checks whether the given x,y node satisfies the transform's
    # initial requirements; if so, returns the two transform pivots

    def _checkLF(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise TypeError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                if not node._exists(self[x,a]):
                    continue
                a,b=self._checkLF(x,a)
                if b is not None:
                    return a,b
            return (None,None)

        # Main clause of the function
        a = self[x,y]
        # ∃ b = pre(a)
        b = self.pre(a)
        if not node._exists(b):
            return (None,None)
        # ∄ top(a), top(top(a))
        if node._exists(self.top(a)) or node._exists(self.top(self.top(a))):
            return (None,None)
#        # ∄ top(b)
#        if node._exists(self.top(b)):
#            return (None,None)
        return (a,b)

    def _checkFL(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise TypeError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=self._checkFL(x,a)
                if b is not None:
                    return a,b
            return (None,None)

        # Main clause of the function
        a = self[x,y]
        # ∃ b s.t pre(a)=pre(b),
        if self.pre(a) is None:
            return (None,None)
        b = None
        for x in self.post(self.pre(a)):
            if x is a:
                continue
        # ∃ c s.t a is below c and b is below pre(c)
            c=a
            while c.y>0:
                c = self.top(c)
                if self._is_below(self.pre(c),x):
                    b=x; break;
        if b is None:
            return (None,None)
        # ∄ bot(a) or (∄ top(b) and pre(b).y>top(b))
        if node._exists(self.bot(a)) and \
          (node._exists(self.top(b)) or not self.pre(b).y>self.top(b).y):
            return (None,None)

        return (a,b)

    def _checkTF(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise TypeError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=self._checkTF(x,a)
                if b is not None:
                    return a,b
            return (None,None)

        # Main clause of the function
        a = self[x,y]

        ### Ugly condition
        # ∃ b s.t pre^n(top(b))=top^n(pre(a)),
        pre = self.pre(a)
        if pre is None or self.top(pre) is None:
            return (None,None)
        b = None
        for x in self.node_list[a.y][::-1]:
            if (not node._exists(x)) or \
                x.y != a.y or \
                x.x >= a.x or \
                self.top(x) is None or \
                self.bot(x) is None or \
                self.pre(self.top(x)) is None:
                continue
            srb=self.r_bot(x)
            tmp1,tmp2=(self.top(x),pre)
            while (tmp1 is not None) and (tmp2 is not None):
                tmp1=self.pre(tmp1); tmp2=self.top(tmp2);
                if tmp1 is tmp2:
                    b=self[srb.x,a.y]; break;
            if b is None:
                return (None,None)
            b=None
        # ∄ b or pre^n(r_top(b))=top^n(pre(b))
            if not node._exists(self[srb.x,a.y]):
                b=self[srb.x,a.y]; break;
            tmp1,tmp2,tmp3=(self.pre(x),pre,pre)
            while (tmp1 is not None):
                tmp1=self.top(tmp1)
                swap=tmp2
                if tmp3 is not None:
                    tmp2=self.pre(tmp3)
                if tmp2 is not None:
                    tmp3=self.top(swap)
                if tmp1 is tmp2 or tmp1 is tmp3:
                    b=self[srb.x,a.y]; break
            if b is not None:
                break
        if b is None:
            return (None,None)

        return (a,b)

    def _checkFT(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise TypeError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b,z=self._checkFT(x,a)
                if b is not None:
                    return (a,b,z)
            return (None,None,None)

        # Main clause of the function
        a = self[x,y]
        # ∃ b s.t pre(a)=pre(b),
        if self.pre(a) is None:
            return (None,None,None)
        b = None
        for x in self.post(self.pre(a)):
            if x is a:
                continue
        # ∄ top(b) or pre^n(top(b))=top^n(pre(b))
            if not node._exists(self.top(x)):
                b=x; z=self.top(self.pre(x)); break;
            tmp1,tmp2=(self.top(x),self.pre(x))
            while (tmp1 is not None) and (tmp2 is not None):
                tmp1=self.pre(tmp1); tmp2=self.top(tmp2);
                if tmp1 is tmp2:
                    b=x; z=tmp1; break;
        if b is None:
            return (None,None,None)

        return (a,b,z)

    def _checkLT(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise TypeError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=self._checkLT(x,a)
                if b is not None:
                    return a,b
            return (None,None)

        # Main clause of the function
        a = self[x,y]
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
            raise TypeError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b=self._checkTL(x,a)
                if b is not None:
                    return a,b
            return (None,None)

        # Main clause of the function
        a = self[x,y]

        ### Ugly condition
        # ∃ b s.t pre(a) is below pre(b), r_bot(b).y>=a.y
        # (second part means that we can only pick the b right above a, no buried b's)
        b = None; tmp = self.pre(a)
        if tmp is None:
            return (None,None)
        while tmp.y>0:
            tmp = self.top(tmp)
            for x in self.post(tmp):
                if self.r_bot(x).y >= a.y:
                    b=x; break;
        if b is None:
            return (None,None)
        # ∄ r_bot(b) s.t r_bot(b).y==a.y or top^n(pre(r_bot(b)))=pre^n(pre(a)):
        # (that is to say, either the node to the left of a should not exist
        # or things get complicated)
        srb=self.r_bot(b)
        if srb.y==a.y:
            b=None
            tmp1,tmp2=(self.pre(srb),self.pre(a))
            while (tmp1 is not None) and (tmp2 is not None):
                tmp1=self.top(tmp1); tmp2=self.pre(tmp2);
                if tmp1 is tmp2:
                    b=x; break;
        if b is None:
            return (None,None)

        return (a,b)

    def LF(self,x,y=None,clean=True):
        a,b = self._checkLF(x,y)
        if b is None:
            return None

        # create c=top(top(a)); pre(c) = top(top(b))
        c=self.top(self.top(a))
        post=self.post(c)
        self.remove_node(c)

        c=node(c.x,c.y,'black')
        self.add_node(c,pre=self.top(self.top(b)))
        for x in post:
            self._add_pre(x,c)

        # pre(a) = pre(b); a -> top(a)
        # This is done at the same time, to avoid add_edge exception
        self.remove_all_edges(a,self.pre(a))
        self.shift_node(a, self.top, new_pre=self.pre(b))

        if clean:
            self.clean()

        return a,b

    def FL(self,x,y=None,clean=False):
# As of the invis/buffer overhaul of commit c0363d063, below comment is false
# Need to implement ∄ bot(a) by shifting in-place if ∄ top(b) and pre(b).y>top(b)
        a,b = self._checkFL(x,y)
        if b is None:
            return None

        #a -> bot(a)
        self.shift_node(a, self.bot)

## Unnecessary del statements from transforms have been commented out
## To be performed by reduce_idem instead
#        #del c = top(top(a))
#        c=self.top(self.top(a))
#        self.remove_node(c)
#
#        c=node(c.x,c.y,'buffer_node')
#        self.add_node(c)

        #pre(a) = b
        self.remove_all_edges(a,self.pre(a))

        self._add_pre(a,b)

        if clean:
            self.clean()

        return a,b

    def TF(self,x,y=None,clean=False):
        a,b = self._checkTF(x,y)
        if b is None:
            return None

        #pre(b) = pre(a)
        if node._exists(b):
            pre=self.pre(b)
            self.remove_all_edges(b,pre)
            self._add_pre(b,self.pre(a))
        else:
            c=node(b.x,b.y,'black')
            self.add_node(c,pre=self.pre(a))

        if clean:
            self.clean()

        return a,b

    def FT(self,x,y=None,clean=False):
        a,b,z = self._checkFT(x,y)
        if b is None:
            return None

        # note: pre = self.pre(b) = self.pre(a)
        pre = self.pre(b)

        #pre(b) = top(pre(b))
        self.remove_all_edges(b,pre)

        self._add_pre(b,self.top(pre))

        #b -> top(b)
        post=self.post(b)
        c=node(b.x,b.y,'black')

        # This is the only transformation where the node/net
        # being created might already exist, even optimized
        if node._exists(self.top(b)):
            self.remove_node(b)
        else:
            self.shift_node(b, self.top)

        #if pre(pre(a)) exists
        #create c = bot(b); pre(c)=bot(pre(pre(a)))
        if self.pre(pre) is not None or z is not self.top(pre):
            if self[c.x,c.y] is not None:
                self.remove_node(self[c.x,c.y])
            tmp=self.pre(self.bot(z))
            while tmp.y<pre.y:
                tmp=self.bot(tmp)
            self.add_node(c,pre=tmp)

        # Note to self:
        # post(b) has to attach to the original b spot
        # I think this is, like the rest of the complication,
        # only when pre(pre(a)) exists
        # Will need to revisit this and draw it out

            for x in post:
                self.remove_all_edges(x,b)
                self._add_pre(x,c)

        if clean:
            self.clean()

        return a,b

    def LT(self,x,y=None,clean=False):
        a,b = self._checkLT(x,y=y)
        if b is None:
            return None

        a,b = self.LF(a.x,a.y,clean)
        return self.FT(a.x,a.y,clean)
        #LF, followed by FT

    def TL(self,x,y=None,clean=True):
        a,b = self._checkTL(x,y)
        if b is None:
            return None

        a,b = self.TF(a.x,a.y,clean)
        return self.FL(a.x,a.y,clean)
        #TF, followed by FL


    # Compresses, eliminates nodes using idempotence, and trims
    # extraneous layers

    def clean(self):
        self.compress()
        self.reduce_idem()
        self.trim_layers()

    # Shifts all possible nodes up

    def compress(self,changed=False):
        # Note: don't change data structure while iterating over it
        for a in self:
            # Only pick non-invis nodes,
            if not node._exists(a):
                continue
            # that do not have a top,
            if node._exists(self.top(a)):
                continue
            # whose pre does not exist
            pre = self.pre(a)
            if pre is None or node._exists(pre):
                continue
            # and whose post(top) is empty
            if len(self.post(self.top(a)))!=0:
                continue
            self.shift_node(a)
            changed=True
            break
        if changed:
            return self.compress()

    # Cancels out logically-equivalent nodes/edges

    def reduce_idem(self):
        modified=[]
        for a in self:
            for b in self:

                # If two nodes and their predecessors are parallel
                if self.pre(a) is not None and \
                   self.pre(b) is not None and \
                   a is not b and \
                   self.pre(a) is not self.pre(b) and \
                   self.pre(a).x==self.pre(b).x and \
                   a.x==b.x and \
                   a.y>0 and b.y>0:

                    # Figure out which one is on top
                    if (self.r_top(a)==b) and not node._exists(self.pre(a)):
                        c = a
                    elif (self.r_top(b)==a) and not node._exists(self.pre(b)):
                        c = b
                    else:
                        continue

                    # Remove the lower pair's edge
                    self.remove_all_edges(c,self.pre(c))
                    modified.append(c)
                    modified.append(self.pre(c))

        # Filter out any modified buffers
        modified = [x for x in modified if node._exists(x)]
        # Delete any nodes that no longer have predecessors
        for a in modified:
            if self.pre(a) is not None:
                continue
            post = self.post(a)
            self.remove_node(a)
            n=node(a.x,a.y,'invis_node')
            self.add_node(n)
            for b in post:
                self._add_pre(b,n)

    # If the last row of the tree is just buffers
    # Shortens the tree by one layer

    def trim_layer(self):
        # Check if last row is just buffers
        if any([ \
               (node._exists(self.top(x)) and not node._isbuf(self.top(x))) \
               for x in self.node_list[-1] \
               ]): return False
        [self._buf_to_invis(self.top(x)) for x in self.node_list[-1]]
        [self.shift_node(x) for x in self.node_list[-1]]
        [self.remove_node(x) for x in self.node_list[-1]]
        del self.node_list[-1]
        return True

    # Adds an extra layer at the bottom of the tree

    def add_layer(self):
        y=len(self.node_list)
        for a in range(self.w):
            self.add_node(node(a,y,'invis_node'))
        for x in self.node_list[-2]:
            self.shift_node(x,self.bot)

    # Shortens the tree by as many layers as it can

    def trim_layers(self):
        while(self.trim_layer()): pass

    # Prints a png

    def png(self,fname='out.png'):

        def wrap(s):
            return('"'+str(s)+'"')

        pg=nx.drawing.nx_pydot.to_pydot(self)
        pg.set_splines("polyline")
        pg.set_concentrate("true")

    # Make fan-out pretty:
    # Go through each node
    # Check for fan-out
    # Create invisible, png-only, nodes

        for row in self.node_list:
            for n in row:
                if n.x==0 or n.y in [0,len(self.node_list)-1] or not node._exists(n):
                    continue
                pre = self.pre(n)
                rights = iter([x for x in row if self.pre(x)==pre and x.x<n.x])
                r1 = next(rights,None)
                r2 = next(rights,None)

                if pre is not None and r1 is not None and not node._isbuf(r1):

                    pos_n="{0},{1}!".format(-1*(n.x-0.5),-1*(n.y-0.5))
                    py_n1=pydot.Node(pos_n,style='invis',pos=pos_n,label="")
                    if len(pg.get_node(wrap(pos_n)))==0:
                        pg.add_node(py_n1)

                    pos_r1="{0},{1}!".format(-1*(r1.x-0.5),-1*(r1.y-0.5))
                    py_n2=pydot.Node(pos_r1,style='invis',pos=pos_r1,label="")
                    if len(pg.get_node(wrap(pos_r1)))==0:
                        pg.add_node(py_n2)

                    if r2 is None:
                        pg.add_edge(pydot.Edge(str(pre),pos_r1,headclip="false"))
                        pg.add_edge(pydot.Edge(pos_r1,str(r1),headclip="false",tailclip="false"))
                    pg.add_edge(pydot.Edge(pos_r1,pos_n,headclip="false",tailclip="false"))
                    pg.add_edge(pydot.Edge(pos_n,str(n),headclip="false",tailclip="false"))

                    pg.del_edge(wrap(pre),wrap(n))
                    pg.del_edge(wrap(n),wrap(pre))
                    pg.del_edge(wrap(pre),wrap(r1))
                    pg.del_edge(wrap(r1),wrap(pre))

        pg.write_png(fname,prog='neato')
