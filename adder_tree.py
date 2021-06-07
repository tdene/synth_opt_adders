from modules import modules
from adder_graph import adder_graph as graph
from adder_graph import adder_node as node
from util import lg
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

    # Redefine __len__ to be the y-axis size of the tree logic
    # since this definition proves to be useful in practice
    def __len__(self):
        return len(self.node_list)-2

    # Pre-condition: n is a valid new node; pre is either None or a node in the graph
    # Post-condition: adds node into graph and connects it correctly
    def add_node(self,n,pre=None):

        if pre is not None and not isinstance(pre,node):
            raise TypeError("provided predecessor node must be a node")

    # Calls on super-method
        super().add_node(n)

    # Keeps track of group propagates/generates
        n.pg=[0]*self.w
    # Initialize if node is P/G node
        if n.m in ['pg_node']:
            n.pg[n.x]=1
    #
    # Connects up
        self._add_top(n)
    # Connects diagonally
        self._add_pre(n,pre)
    #
    # Connects down
        if self.bot(n) is not None:
            self._add_top(self.bot(n))

    # Recalculate the group P/G for a node
    def _recalc_pg(self,n):
        if n.m in ['pg_node']:
            return

        top = self.top(n)
        pre = self.pre(n)

        top_g = top.pg if top is not None else [0]*self.w
        pre_g = pre.pg if pre is not None else [0]*self.w

        n.pg = [x|y for x,y in \
                   zip(top_g,pre_g)]


    # Pre-condition: a and b are both iterables
    # Post-condition: return value is True/False

    # Determine whether a combination of nodes (b)
    # has the same group P/G as another combination (a)
    # That is, if a PG is in b, then it has to be in a
    # b -> a === (not b)|a
    def _is_pg_subset(self,a,b):
        a = [x.pg if x is not None else [0]*self.w for x in a]
        a = [any(x) for x in zip(*a)]
        b = [x.pg if x is not None else [0]*self.w for x in b]
        b = [any(x) for x in zip(*b)]
        return all([(not y)|x for x,y in zip(a,b)])

    # Traverse the graph downstream of a node
    # applying fun to every node you meet
    def walk_downstream(self,n,fun=lambda x: x):
        bot = self.bot(n)
        post = self.post(n)

        fun(n)
        if bot is not None: self.walk_downstream(bot,fun)
        for x in post: self.walk_downstream(x,fun)

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

        n.pg = [x|y for x,y in zip(n.pg,top.pg)]

    # Internal helper function to prevent re-writing of code
    # Connects node to a predecessor
    def _add_pre(self,n,pre):

        if pre is None: return

        if 'pin' in n.ins and len(n.ins['pin'])>1:
            self.add_edge(pre,('pout',0),n,('pin',0))
        if 'gin' in n.ins and len(n.ins['pin'])>1:
            self.add_edge(pre,('gout',0),n,('gin',0))

        n.pg = [x|y for x,y in zip(n.pg,pre.pg)]

    # Internal function to morph a node to another type
    # no_warn and no_pre should NOT be set to True unless
    # EXTREME care is taken
    def _morph_node(self,n,m,no_warn=False,no_pre=False):
        # Query current posts and pres
        post = self.post(n)
        pre = self.pre(n)

        # Swap nodes
        self.remove_node(n)
        new_n = node(n.x,n.y,m)
        self.add_node(new_n)

        update_flag = no_pre

        # Re-apply pre
        if (pre is not None and not no_pre):
            # Raise error if you're morphing
            # from a node with pre to one without
            if (node._exists(n) and not node._isbuf(n)) and \
               (not node._exists(new_n) or node._isbuf(new_n)):
                if no_warn:
                    update_flag = True
                else:
                    raise TypeError("cannot morph node with pre to node without")
            else:
                self._add_pre(new_n,pre)

        # Re-apply post
        for x in post:
            self._add_pre(x,new_n)

        # If no_warn/no_pre was for some reason set to True,
        # first: please re-consider doing so
        # then: update all the groups down-stream
        # Commented out as this should really not be done
        if update_flag:
            self.walk_downstream(new_n,fun=self._recalc_pg)
        return new_n

    # Shifts a node in a direction given by fun
    # Can only shift nodes if there is nothing in the way
    def shift_node(self, n, fun=None, new_pre=None):

        if fun==None:
            fun=self.top

        # Grab the invis we're swapping with
        inv=fun(n)

        if n not in self:
            raise ValueError("trying to shift a node not in the graph")
        if node._exists(inv) and not node._isbuf(inv):
            raise ValueError("can only shift node into invis or buffer")

        # Save pre/post
        pre = self.pre(n)
        post = self.post(n)

        # We need to take this opportunity to shift the wire
        # Note that this requires fun(pre).y = inv.y-1
        # This second condition will never matter if we are only shifting by 1
        # But for future support, it is still stated
        if (pre is not None):
            pre = fun(pre)

        # Run pre/post error checks
        if pre is not None and pre.y>=inv.y:
            raise ValueError("cannot shift node past predecessor")
        if inv.y > n.y:
            if len(post)>0:
                raise ValueError("cannot shift node past successor")

        # If new_pre is provided, use that, not what we calculate
        if new_pre is not None:
            if not node._exists(new_pre):
                new_pre=self._morph_node(new_pre,'buffer_node')
            pre = new_pre

        # if ∃ post(n):
        # add buffer instead of inv
        if len(post)>0:
            new_m='buffer_node'
        else:
            new_m='invis_node'

        # Morph nodes
        # Note that this sets no_pre, which is not advised
        new_n = self._morph_node(inv,n.m,no_pre=True)
        new_inv = self._morph_node(n,new_m,no_pre=True)
        self._add_pre(new_n,pre)

        self.walk_downstream(new_n,fun=self._recalc_pg)
        self.walk_downstream(new_inv,fun=self._recalc_pg)

        return new_n

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the y-1 neighbor (P/G logic if already at the top)
    def top(self,n):
        if n is None or n.y==0:
            return None
        return self[n.x,n.y-1]

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the next-highest non-invis neighbor
    def r_top(self,n):
        top = self.top(n)
        return top if (node._exists(top) or top is None) else self.r_top(top)

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the y+1 neighbor (stops before post-processing logic)
    def bot(self,n):
        if n is None or n.y>len(self.node_list)-2:
            return None
        return self[n.x,n.y+1]

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the next-lowest non-invis neighbor
    def r_bot(self,n):
        bot = self.bot(n)
        return bot if (node._exists(bot) or bot is None) else self.r_bot(bot)

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the x-1 neighbor (stops before post-processing logic)
    def right(self,n):
        if n is None or n.x==0:
            return None
        return self[n.x-1,n.y]

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the next-rightest non-invis + non-buffer neighbor
    def r_right(self,n,c=[]):
        right = self.right(n)
        if (node._exists(right) and not node._isbuf(right)) or \
        right is None or right in c:
            return right
        return self.r_right(right,c)

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the diagonal predecessor (or top(n) if n is a buffer)
    def pre(self,n):
        for x in self._possible_pres(n):
            if n in self.post(x): return x
        return None

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: goes up the chain of predecessors as far as it can
    def r_pre(self,n):
        pre = self.pre(n)
        return n if pre is None else self.r_pre(pre)

    # Pre-condition: n is a valid node in the main part of the tree (gray/black/buffer)
    # Post-condition: returns the list of diagonal successors
    def post(self,n):
        return [a for a in self.adj[n] if a.x>n.x]

    # Helper function that checks whether n2 is below n1
    # Same column, higher row, or second node straight-up does not exist
    def _is_below(self,n1,n2):
        return (n2 is None) or (n1 is not None and n2.x==n1.x and n2.y>n1.y)

    # Pre-condition: n is a valid node
    # Post-condition: returns a list of all nodes it could connect to as a pre
    def _possible_pres(self,n,c=[],d=[]):
        # Figure out bounds so that wires don't cross illegaly
        post = self.r_right(n,c)
        if post in c:
            bound = d[c.index(post)]
        else:
            bound = None if post is None else self.pre(post)
        bound = 0 if bound is None else bound.x
        # Return all possible nodes in that range
        return self.node_list[n.y-1][bound:n.x]

    # Helper function
    # Pre-condition:
    # We have a pair of nodes, a and b, such that pre(a) = b
    # We want to disconnect a from b, which makes for a new pre(a)
    # So we need to add a series of cells on top of a so that
    # is_pg([top(a),pre(a)],[top(b),pre(b)])
    # The very first term in that expression, top(a), can be further
    # broken down into tops and pres
    # Post-condition:
    # Returns a tuple of lists of tops and pres that need be created
    # Or None,None if the requirement is impossible
    # Note that in the function call, a and pre are the new a and pre
    def _valid_tops(self,a_bits,b,x,c=[],d=[],path=[],result=(None,None)):

        # If our current solution is worse than a pre-existing one, abort
        if result[0] is not None and len(result[0])<len(c):
            return None,None

        # If we are done, we are done!
        if self._is_pg_subset((*d,*a_bits),(b,)):
            return c,d

        # If x is not part of the body,
        # fork back up the recursion tree
        if not node._in_tree(x):
            # If we've reached the end, this fork is dead
            if len(path)==0: return None,None
            # Otherwise fork up
            return self._valid_tops(a_bits,b, \
                   self.top(path[-1]),c,d,path[:-1],result)

        # Forking down into the recursion tree

        # Figure out x's pre, or attempted pre
        pre = self.pre(x)
        # If x has no pre, try forking through possible pre's
        if pre is None and x not in c:
            # Iterate over all possible pre's
            for y in self._possible_pres(x,c,d):
                # Fork up through the prefix tree
                tmp = self._valid_tops(a_bits,b,y,c+[x],d+[y],path+[x],result)
                if tmp[0] is not None: result = tmp;
        # If x has a pre, try forking thru the pre chain
        elif pre is not None:
            tmp = self._valid_tops(a_bits,b,pre,c,d,path+[x],result)
            if tmp[0] is not None: result = tmp;

        # Either way, fork up through the top as well
        tmp = self._valid_tops(a_bits,b,self.top(x),c,d,path,result)
        if tmp[0] is not None: result = tmp;

        # Return list of candidates
        return result

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
                a,b,c,d=self._checkLF(x,a)
                if b is not None:
                    return a,b,c,d
            return (None,None,None,None)

        # Main clause of the function
        a = self[x,y]
        # ∃ b = pre(a)
        b = self.pre(a)
        if not node._exists(b):
            return (None,None,None,None)
        # ∄ top(a)
        top = self.top(a)
        if node._exists(top):
            return (None,None,None,None)

        pre = self.top(b) if node._isbuf(b) else self.pre(b)

        c,d = self._valid_tops((pre,self.top(top)),b,self.top(top))

        if c is None:
            return (None,None,None,None)

        return (a,b,c,d)

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

        pre = self.pre(a)
        if pre is None:
            return (None,None)

        b = None
        for x in reversed(self.node_list[y][pre.x:x]):
            top = self.top(x)
        # ∃ b s.t pre(a)=pre(b),
            if self.pre(x)==pre or \
               (top==pre and x.m in ['invis_node','buffer_node']):

        # We have to account for post(a) remapping
        # ∀ post(a), is_pg([top(post),a],[top(post),b]) or ∄ top(post)
                flag=True
                for y in self.post(a):
                    topy = self.top(y)
                    if not self._is_pg_subset((topy,x),(topy,a)) and \
                       node._exists(topy):
                        flag=False; break;
                if flag:
                    b=x; break;

        bot = self.bot(a)
        # ∄ bot(a) or bot(a) = post-processing
        if b is not None and (not node._exists(bot) or \
           bot.m in ['xor_node'] or \
           node._isbuf(bot)):
            return (a,b)

        return (None,None)

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

        pre = self.pre(a)
        if pre is None:
            return (None,None)

        b = None
        top = self.top(a)
        # ∃ b s.t. b.x > pre(a).x
        for x in self._possible_pres(a):
            if not x.x>pre.x: continue
            # Figure out if a valid remapping exists
            c,d = self._valid_tops((top,x),pre,top)
            if c is not None: b=x; break;

        if b is None: return (None,None)

        return (a,b)

    def _checkFT(self,x,y=None):
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise TypeError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b,c,d=self._checkFT(x,a)
                if b is not None:
                    return (a,b,c,d)
            return (None,None,None,None)

        # Main clause of the function
        a = self[x,y]

        pre = self.pre(a)
        if pre is None:
            return (None,None,None,None)

        b = None; c = None; d = None;
        top = self.top(a)
        # Check each possible pre
        for x in reversed(self._possible_pres(a)):
            if not x.x<pre.x: continue
            # Figure out if a valid remapping exists
            c,d = self._valid_tops((top,x),pre,top)
            if c is not None: b=x; break;

        if b is None:
            return (None,None,None,None)

        return (a,b,c,d)

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
        a,b,c,d = self._checkLF(x,y)
        if b is None:
            return None

        # create c=top(top(a)); pre(c) = top(top(b))
        for x,y in zip(c,d):
            x=self[x.x,x.y]; y=self[y.x,y.y];
            x=self._morph_node(x,'black')
            if not node._exists(y):
                y=self._morph_node(y,'buffer_node')
            self._add_pre(x,y)
            self.walk_downstream(x,fun=self._recalc_pg)

        pre = self.top(b) if node._isbuf(b) else self.pre(b)

        # pre(a) = pre(b); a -> top(a)
        # This is done at the same time, to avoid add_edge exception
        self.remove_all_edges(self.pre(a),a)
        a = self.shift_node(a, self.top, new_pre=pre)

        # pre(post(b)) = a
        post = [x for x in self.post(b) if x.x>a.x]
        for x in post:
            self.remove_all_edges(b,x)
            self._add_pre(x,a)
            self.walk_downstream(x,fun=self._recalc_pg)

        if clean:
            self.clean()

        return a,b

    def FL(self,x,y=None,clean=True):
        a,b = self._checkFL(x,y)
        if b is None:
            return None

        # pre(post(a)) = b
        # pre(top(post(a))) = top(a)
        post = self.post(a)
        for x in post:
            top = self.top(x)
            if not self._is_pg_subset((top,b),(top,a)):
                top = self._morph_node(top,'black')
                self._add_pre(top,self.top(a))
            self.remove_all_edges(a,x)
            self._add_pre(x,b)
            self.walk_downstream(top,fun=self._recalc_pg)

        # If we have space solely because this is the bottom
        if not node._in_tree(self.bot(a)):
            self.add_layer()

        # a -> bot(a); pre(a) = b
        # This is done at the same time, to avoid add_edge exception
        self.remove_all_edges(self.pre(a),a)
        a = self.shift_node(a, self.bot, new_pre=b)

        if clean:
            self.clean()

        return a,b

    def TF(self,x,y=None,clean=True):
        a,b = self._checkTF(x,y)
        if b is None:
            return None

        # Make sure b is at least a buffer
        if not node._exists(b):
            b=self._morph_node(b,'buffer_node')

        #pre(a) = b
        pre = self.pre(a)
        pre = self.remove_all_edges(pre,a)
        self._add_pre(a,b)
        self.walk_downstream(b,fun=self._recalc_pg)

        if clean:
            self.clean()

        return a,b

    def FT(self,x,y=None,clean=True):
        a,b,c,d = self._checkFT(x,y)
        if b is None:
            return None

        pre = self.pre(a)

        # pre(a) = b, and any other additions necessary
        self.remove_all_edges(pre,a)
        c=[a]+c
        d=[b]+d
        for x,y in zip(c,d):
            x=self[x.x,x.y]; y=self[y.x,y.y];
            x=self._morph_node(x,'black')
            if not node._exists(y):
                y=self._morph_node(y,'buffer_node')
            self._add_pre(x,y)
            self.walk_downstream(x,fun=self._recalc_pg)

        if clean:
            self.clean()

        return a,b,c,d

    def LT(self,x,y=None,clean=True):
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

    def batch_transform(self,transform,x1,x2,step=1):
        for x in range(x1,x2,step):
            if not getattr(self,transform)(x):
                err="batch transform {0} failed on {1}".format(transform,x)
                raise ValueError(err)

    def harris_step(self,transform,steps=1):
        if steps==0: return
        # Harris space is different from transform space
        # Brent-Kung is the L corner of Harris space
        # Ripple-carry is our L corner
        # So if we're moving to/from L, we need to
        # modify our transform to move towards Brent-Kung
        if transform in ['LF','FL','LT','TL']:

            step = 2*lg(self.w)-len(self)-(transform[1]=='L')
            top  = self.w-1
            bot  = top-1 - (lg(self.w)-1)*step

        self.batch_transform(transform,bot,top,step)

        self.harris_step(transform,steps-1)

    # Compresses, eliminates nodes using idempotence,
    # and trims extraneous layers
    def clean(self):
        while self.reduce_idem() or self.compact(): pass
        self.trim_layers()

    # Shifts all possible nodes up
    def compact(self):
        # Note: don't change data structure while iterating over it
        changed = False
        for a in self:
            # Only pick non-invis nodes inside the prefix logic,
            if not node._exists(a) or not node._in_tree(a):
                continue
            # that do not have a top,
            if node._exists(self.top(a)):
                continue
            # whose pre is invis
            pre = self.pre(a)
            if pre is None or node._exists(pre):
                continue
            a = self.shift_node(a)
            changed=True; break;
        if changed:
            return 1+self.compact()
        else:
            return 0

    # Cancels out logically-equivalent nodes/edges
    # As of commit 194923b83, this relies on node group P/G
    def reduce_idem(self):
        modified=None
        for a in self:
            # Filter out invis nodes
            if not node._exists(a): continue
            # Filter out pre/post-processing nodes
            if not node._in_tree(a): continue

            # Filter out buffers that have a purpose
            # That is, either the buffer has more than 1 post
            # Or the buffer has 1 post and no black cells under

            # Do not filter out any buffers that are at the
            # top of the tree and have black cells under
            if node._isbuf(a):
                tmp=[x[a.x] for x in self.node_list[a.y+1:-1]]
                tmp=[not node._exists(x) or node._isbuf(x) for x in tmp]
                black_under = not all(tmp)
                in_the_way = black_under and not node._in_tree(self.top(a))
                if len(self.post(a))>1 and not in_the_way: continue
                if len(self.post(a))==1 and not black_under: continue

            # If node does not introduce anything new, flag
            rtop = self.r_top(a)
            rbot = self.r_bot(a)
            pre = self.pre(a)

            # Case 1: This node gives no more than rtop
            if self._is_pg_subset((rtop,),(a,)):
                modified=a
            # Case 2: This node provides nothing to rbot
            # and has no posts?
            elif not node._isbuf(rbot) and \
            len(self.post(a))==0 and \
            self._is_pg_subset((self.pre(rbot),rtop),(pre,rtop)):
                modified=a

        # Reduce any nodes that are flagged
        if modified is not None:
            pre = self.pre(modified)
            # If node has post, it can only reduce down to buffer
            # Otherwise it can reduce down to invis
            if len(self.post(modified))==0 or node._isbuf(modified):
                m = 'invis_node'
            else:
                m = 'buffer_node'
            self._morph_node(modified,m,True)
            return 1+self.reduce_idem()
        return 0

    # If the last row of the tree is just buffers
    # Shortens the tree by one layer
    def trim_layer(self):
        # Check if last row is just buffers
        if any([ \
               (node._exists(self.top(x)) and not node._isbuf(self.top(x))) \
               for x in self.node_list[-1] \
               ]): return False
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
        pg.set_splines("false")
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
                rights = iter([x for x in row if self.pre(x)==pre and x.x<n.x and \
                               (node._exists(x) and not node._isbuf(x))])
                r1 = next(rights,None)
                r2 = next(rights,None)

                if pre is not None and r1 is not None:

                    pos_n="{0},{1}!".format(-1*(n.x-0.5),-1*(n.y-0.5))
                    py_n1=pydot.Node(pos_n,style='invis',pos=pos_n,label="")
                    if len(pg.get_node(wrap(pos_n)))==0:
                        pg.add_node(py_n1)

                    pos_r1="{0},{1}!".format(-1*(r1.x-0.5),-1*(r1.y-0.5))
                    py_n2=pydot.Node(pos_r1,style='invis',pos=pos_r1,label="")
                    if len(pg.get_node(wrap(pos_r1)))==0:
                        pg.add_node(py_n2)

                    if r2 is None:
                        tail = 's' if node._isbuf(pre) else 'sw'
                        pg.add_edge(pydot.Edge(str(pre),pos_r1,
                            headclip="false",arrowhead="none",
                            tailport=tail))
                        pg.add_edge(pydot.Edge(pos_r1,str(r1),
                            headclip="false",tailclip="false",arrowhead="none",
                            headport='ne'))
                    pg.add_edge(pydot.Edge(pos_r1,pos_n,
                        headclip="false",tailclip="false",arrowhead="none"))
                    #    headport='n',tailport='s'))
                    pg.add_edge(pydot.Edge(pos_n,str(n),
                        headclip="false",tailclip="false",arrowhead="none",
                        headport='ne'))

                    pg.del_edge(wrap(pre),wrap(n))
                    pg.del_edge(wrap(pre),wrap(r1))

        pg.write_png(fname,prog='neato')

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")

