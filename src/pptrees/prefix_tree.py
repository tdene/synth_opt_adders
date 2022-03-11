from .modules import modules
from .prefix_graph import prefix_graph as graph
from .prefix_graph import prefix_node as node
from .util import lg, verso_pin
import networkx as nx
import pydot
from functools import reduce
from itertools import cycle
import webbrowser

class prefix_tree(graph):
    """Class that generates parallel prefix trees
    
    Trees are initialized to a serial structures (ripple-carry-like)
    Trees can morph via any of three, reversible, transforms:
    L->F, F->L, L->T, T->L, F->T, T->F
    """

    def __init__(self,width,network="ripple",node_defs={},is_idem=False):
        """Initializes a parallel prefix tree

        Pre-conditions:
            width is an integer
            network is a valid initial network choice (defaults to ripple)
            node_defs is a dictionary that defines the following nodes:
                - 'pre' (pre-processing)
                - 'post' (post-processing)
                - 'black' (prefix operation)
                - 'buffer' (identity operation)
            Optional node definitions include but are not limited to:
                - 'first_pre' (right-most pre-processing node)
                - 'grey' (prefix operation in the last row)
            is_idem is a boolean noting if the prefix operation is idempotent
        """
        if not isinstance(width,int):
            raise TypeError("provided width must be an integer")
        if not isinstance(node_defs,dict):
            raise TypeError("must provide dictionary of node definitions")
        for a in ['pre','post','black']:
            if a not in node_defs:
                raise ValueError("pre, post, and black nodes must all be defined")

        super().__init__(width)
        self.node_defs = node_defs
        self.is_idem = is_idem

        # Initialize P/G nodes:
        for a in range(self.w):
            # If first pre node is different
            # For example, due to an adder's carry-in
            if a==0 and 'first_pre' in self.node_defs:
                n = self.add_node(node(a,0,self.node_defs['first_pre']))
                n.outs['pout'][0]="$p_lsb"
                n.outs['gout'][0]="$g_lsb"
            else:
                n = self.add_node(node(a,0,self.node_defs['pre']))
                n.outs['pout'][0]="$p{0}".format(a-1)
                n.outs['gout'][0]="$g{0}".format(a-1)

        # Initialize to Sklansky
        if network=="sklansky" or network=="brent-kung":
            for a in range(1,self.w):
                num_buf = 2**(a-1)
                ctr = num_buf
                for b in range(self.w):
                    if ctr>0:
                        self.add_node(node(b,a,'invis_node'))
                        ctr-=1
                    elif ctr==-1*num_buf:
                        self.add_node(node(b,a,'invis_node'))
                        ctr = num_buf-1
                    else:
                        if a == lg(b)+1:
                            node_color = "grey"
                        else:
                            node_color = "black"
                        self.add_node(node(b,a,self.node_defs[node_color]),pre=self[b+ctr-1,a-1])
                        ctr-=1
            self.dna="sklansky"
        # Initialize to Kogge-Stone
        elif network=="kogge-stone":
            for a in range(1,self.w):
                for b in range(self.w):
                    num_buf = 2**(a-1)
                    if b>num_buf-1:
                        if a == lg(b)+1:
                            node_color = "grey"
                        else:
                            node_color = "black"
                        self.add_node(node(b,a,self.node_defs[node_color]),pre=self[b-num_buf,a-1])
                    else:
                        self.add_node(node(b,a,self.node_defs['buffer']))
            self.dna="kogge-stone"
        # Initialize serial structure
        else:
            for a in range(1,self.w):
                for b in range(self.w):
                    if b!=a:
                        self.add_node(node(b,a,'invis_node'))
                    else:
                        self.add_node(node(b,a,self.node_defs['grey']),pre=self[b-1,a-1])
            self.dna="ripple"

        # Post-processing
        for a in range(self.w):
            n = self.add_node(node(a,self.w,self.node_defs['post']))

        self.clean()

        if network=="brent-kung":
            self.harris_step('FL',lg(self.w)-1)
            self.dna="brent-kung"

    def _to_sklansky(self):
        """Internal function; transforms an ripple structure to Sklansky

        Uses transforms, as opposed to __init__ which simply places nodes
        """
        for a in range(1,n):
            if a & (a-1)==0: continue
            self.batch_transform('LF',a,n)

    def __len__(self):
        """Redefine the length property as the y-axis size of the tree"""
        return len(self.node_list)-2

    def add_node(self,n,pre=None):
        """Adds a node to the tree, optionally with a pre-defined diagonal connection"

        Pre-conditions:
            n is a valid new node
            pre is either None or a node in the graph
        """

        if pre is not None and not isinstance(pre,node):
            raise TypeError("provided predecessor node must be a node")
        if pre is not None and pre.m not in self.node_defs.values():
            raise ValueError("provided predecessor node type must be defined for this tree")

        # Calls on super-method
        n = super().add_node(n)

        # Keeps track of group propagates/generates
        n.pg=0
        # Initialize pg if node is P/G node
        if modules[n.m]['type']=='pre':
            n.pg=1<<n.x

        # Connects up
        self._add_top(n)
        # Connects diagonally
        self._add_pre(n,pre)
        # Connects down
        if self.bot(n) is not None:
            self._add_top(self.bot(n))

        # If pre_node is added, HDL connect it to input pins
        if n.m == self.node_defs['first_pre']:
            n.ins['cin'][0]='$cin'
        if n.m == self.node_defs['pre']:
            n.ins['a_in'][0]='$a[{0}]'.format(n.x-1)
            n.ins['b_in'][0]='$b[{0}]'.format(n.x-1)

        # If post_node is added, HDL connect it to output pins
        if n.m == self.node_defs['post']:
            #n.ins['gin'][0]='$c{0}'.format(n.x)
            n.outs['sum'][0]='$sum[{0}]'.format(n.x)

        return n

    def _recalc_pg(self,n):
        """Recalculates the group P/G of a node

        TO-DO: Rename P/G to a more general, addition-nonspecific, term.
        TO-DO: First check if node actually exists in tree.
        """
        if modules[n.m]['type']=='pre':
            return

        top = self.top(n)
        pre = self.pre(n)

        top_g = top.pg if top is not None else 0
        pre_g = pre.pg if pre is not None else 0

        n.pg = top_g|pre_g

        n.upstream=set()
        if top is not None:
            n.upstream.add((top.x,top.y))
            n.upstream.update(top.upstream)
        if pre is not None:
            n.upstream.add((pre.x,pre.y))
            n.upstream.update(pre.upstream)

    def _is_pg_subset(self,a,b):
        """Determines whether the P/G of b is a subset of the P/G of a

        Pre-conditions:
            a and b are both iterables
        """
        # Turn a list of nodes into a list of pg
        a = [x.pg if x is not None else 0 for x in a]
        b = [x.pg if x is not None else 0 for x in b]
        # Merge lists of pg into single comprehensive list
        a = reduce(lambda x,y: x|y, a, 0)
        b = reduce(lambda x,y: x|y, b, 0)
        # b -> a === (not b)|a
        ret = ~b|a
        # Return True if all bits are high
        return ret&(ret+1)==0

    def _is_pg_end_node(self,a,i):
        """Determines whether the set of nodes, a, is P/G equivalent with the i'th end node

        Pre-conditions:
            a is an iterable, b is an integer denoting a column
        """
        # Turn a list of nodes into a list of pg
        a = [x.pg if x is not None else 0 for x in a]
        # Merge lists of pg into single comprehensive list
        a = reduce(lambda x,y: x|y, a, 0)
        # The i'th end node will have [i:0] P/G
        i = (1<<(i+1))-1
        # b -> a === (not b)|a
        # TO-DO: Is this correct? Should we not be checking === instead of ->?
        ret = ~i|a
        # Return True if all bits are high
        return ret&(ret+1)==0

    def _remains_pg_valid(self,n,b):
        """Checks whether the node, b, can be equivalently replaced by a set of nodes

        Pre-condition:
            n is (x,y) coordinate tuple
            b is an iterable
        """
        # TO-DO:
        # This currently does F | F | T | F | T
        # It should do T & T & T & T & T
        # NEED TO FIX

        # Assume result is False
        ret = False
        # Iterate through all end-nodes
        for x in self.node_list[-1]:
            # Save the list of nodes upstream of x
            tmp = x.upstream
            # If n is not upstream of x, try the next end-node
            if n not in tmp: continue
            # Make list of all nodes that are upstream of x,
            # on a different column than n,
            # but on the same row as n
            # That is, all nodes that contribute to x without relying on n
            orig = [self[i] for i in x.upstream if i[0]!=n[0] and i[1]==n[1]]
            # Add the set b to this list
            orig.extend(b)
            # Check to see whether this new set,
            # x's upstream without n but with b
            # still leads to a valid tree
            tmp = self._is_pg_end_node(orig,x.x)
            # What is this doing. What actually is this doing.
            # This code is used nowhere
            a = [x.pg if x is not None else 0 for x in orig]
            a = reduce(lambda x,y: x|y, a, 0)
            # Or's together all the results. This logic is wrong.
            ret = ret or self._is_pg_end_node(orig,x.x)
        return ret
    
    def walk_downstream(self,n,fun=lambda x: x):
        """Traverse the graph downstream of node n, applying fun to each node"""
        # Need to go in two directions: vertical and diagonal
        bot = self.bot(n)
        post = self.post(n)

        fun(n)
        # Iterate
        if bot is not None: self.walk_downstream(bot,fun)
        for x in post: self.walk_downstream(x,fun)

    def _add_top(self,n,pre=None):
        """Internal function; connects node to its vertical predecessor"""

        # Get top if it exists
        top = self.top(n)
        if top is None: return

        # Connect top to the last pins in the node's input list
        for name,bits,num_diag in modules[n.m]['ins']:
            # Check whether the top node has a matching out for our in
            try:
                name_m,bits_m = next(x for x in modules[top.m]['outs'] if x[0]==verso_pin(name))
            # If not, just leave it unconnected and hope for the best?..
            except StopIteration:
                continue
            # Connect pins down to the allowed number of diagonal pins
            for b in range(bits-num_diag):
                pos_n = bits - b - 1
                pos_m = bits_m - b - 1
                self.add_edge(top,(name_m,pos_m),n,(name,pos_n))

        # Update pg
        n.pg = n.pg|top.pg

    def _add_pre(self,n,pre):
        """Internal function; connects node diagonally to a predecessor"""

        # If the provided "pre" is None, do nothing
        if pre is None: return

        # Connect pre to the first pins in the node's input list
        for name,bits,num_diag in modules[n.m]['ins']:
            # Check whether the pre node has a matching out for our in
            try:
                match = next(x for x in modules[pre.m]['outs'] if x[0]==verso_pin(name))
            # If not, just leave it unconnected and hope for the best?..
            except StopIteration:
                continue
            # Connect pins up to the allowed number of diagonal pins
            for b in range(num_diag):
                pos = b
                self.add_edge(pre,(match[0],pos),n,(name,pos))

        n.pg = n.pg|pre.pg

    def _morph_node(self,n,m,no_warn=False,no_pre=False):
        """Internal function to morph a node to another type

        no_warn and no_pre should NOT be set to True
        unless EXTREME care is taken

        In general, the existence and use of this function is a
        severe moral hazard, and alternatives must be investigated.
        """
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
                    raise TypeError("cannot morph node with pre to node without pre")
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

    def shift_node(self, n, fun=None, new_pre=None):
        """Shifts a node in the direction specified by fun
        
        Can only shift nodes if there is nothing in the way.
        """

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
                new_pre=self._morph_node(new_pre,self.node_defs['buffer'])
            pre = new_pre

        # if ∃ post(n):
        # add buffer instead of inv
        if len(post)>0:
            new_m=self.node_defs['buffer']
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

    def top(self,n):
        """Returns the y-1 neighbor of node n

        Pre-condition: n is a valid node in the main part of the tree
        """
        if n is None or n.y==0:
            return None
        return self[n.x,n.y-1]

    def r_top(self,n):
        """Returns the closest valid cell north of node n

        Pre-condition: n is a valid node in the main part of the tree
        """
        top = self.top(n)
        return top if (node._exists(top) or top is None) else self.r_top(top)

    def bot(self,n):
        """Returns the y+1 neighbor of node n

        Pre-condition: n is a valid node in the main part of the tree
        Note: stops before reaching post-processing logic.
        If used on the bottom row of main nodes, returns None.
        """
        if n is None or n.y>len(self.node_list)-2:
            return None
        return self[n.x,n.y+1]

    def r_bot(self,n):
        """Returns the closest valid cell south of node n

        Pre-condition: n is a valid node in the main part of the tree
        """
        bot = self.bot(n)
        return bot if (node._exists(bot) or bot is None) else self.r_bot(bot)

    def right(self,n):
        """Returns the x-1 neighbor of node n

        Pre-condition: n is a valid node in the main part of the tree
        """
        if n is None or n.x==0:
            return None
        return self[n.x-1,n.y]

    def r_right(self,n,c=[]):
        """Returns the closest valid cell east of node n

        Pre-conditions:
            n is a valid node in the main part of the tree
            c is a list of "hypothetical" valid cells that do not
                yet exist, but are treated as though they do
        """
        right = self.right(n)
        if (node._exists(right) and not node._isbuf(right)) or \
        right is None or right in c:
            return right
        return self.r_right(right,c)

    def pre(self,n):
        """Returns the diagonal predecessor of node n

        If n is a buffer, this returns the vertical predecessor.
        Or, it should, but the functionality appears to have been removed.

        Pre-condition: n is a valid node in the main part of the tree
        """
        #for x in self._possible_pres(n):
        for x in self.node_list[n.y-1][:n.x]:
            if n in self.post(x): return x
        return None

    def r_pre(self,n):
        """Traverses as far up diagonally through predecessors as possible

        Pre-condition: n is a valid node in the main part of the tree

        NOTE: This function currently has no present, nor foreseeable, use.
        Candidate for trimming.
        """
        pre = self.pre(n)
        return n if pre is None else self.r_pre(pre)

    def post(self,n):
        """Returns a list of diagonal successors for node n

        If n is a buffer, this list is empty.
        TO-DO: Investigate whether this functionality for buffers is intended.

        Pre-condition: n is a valid node in the main part of the tree
        """
        return [a for a in self.adj[n] if a.x>n.x]

    def _is_below(self,n1,n2):
        """Checks whether n2 is directly south of n1

        NOTE: This function currently has no present, nor foreseeable, use.
        Candidate for trimming.
        """
        return (n2 is None) or (n1 is not None and n2.x==n1.x and n2.y>n1.y)

    def _possible_pres(self,n,c=[],d=[]):
        """Returns of list of all valid diagonal predecessors of node n

        Pre-conditions:
            n is a valid node in the main part of the tree
            c is a list of "hypothetical" valid cells that do not
                yet exist, but are treated as though they do
            d is a list of "hypothetical" diagonal predecessors
                of each respective cell listed by c
        """
        # Figure out bounds so that wires don't cross illegaly
            # First, find the left-most right neighbor of n
        post = self.r_right(n,c)
        if post in c:
            # If this neighbor is hypothetical, its predecessor is in d
            # This is the bound
            bound = d[c.index(post)]
        else:
            # Otherwise, its predecessor is its predecessor
            # This is the bound
            bound = None if post is None else self.pre(post)
        # Convert bound from node to coordinate
        bound = 0 if bound is None else bound.x
        # Return all possible nodes in that range
        return self.node_list[n.y-1][bound:n.x]

    # TO-DO: Improve run-time performance of this function
    # One suggestion is to do a breadth-first, not depth-first, search
    def _valid_tops(self,a,a_bits,b,x,c=[],d=[],path=[],result=(None,None)):
        """Finds cells that must be created if a is disconnected from pre(a) = b

        The situation is the following. b is the diagonal predecessor of a.
        However, we want to disconnect a from b.
        Nodes must be added to preserve the tree's validity.
        The possibility tree of nodes to be added is explored via a full recursion.

        a is a node in the tree
        b is its current diagonal predecessor
        a_bits are the nodes that feed into a:
            its current top
            its new diagonal predecessor after the change (if any)
        x is the closest node north of a that is empty (available)

        c is a list of "hypothetical" cells that do not yet exist,
            but could be added in to fix the tree.
        d is a list of c's diagonal predecessor connections.
        path is the path that a specific recursive branch has taken. 
        result is the final output of a specific recursive branch

        This function explores possibilities by recursing up through
        possible branches. Each explored branch returns the smallest
        list of necessary changes it finds. Thus, the overall method
        returns one of the smallest tuples of changes needed.

        """
        # If our current solution is worse than a pre-existing one, abort
        # This cuts the search tree down significantly
        # As soon as a valid result is found, any paths longer than it
        # are not explored.
        if result[0] is not None and len(result[0])<len(c):
            return None,None

        # If we are done, we are done!
        if self._remains_pg_valid((a.x,a.y),(*d,*a_bits)):
            return c,d

        # If x is not part of the body,
        # go back up the recursive stack
        if not node._in_tree(x):
            # If we've reached the top of the stack, this fork is dead
            if len(path)==0: return None,None
            # Otherwise fork up
            return self._valid_tops(a,a_bits,b, \
                   self.top(path[-1]),c,d,path[:-1],result)

        # Forking down into the recursion tree

        # Figure out x's pre, or lack thereof
        pre = self.pre(x)
        # If x has no pre, try forking through possible pre's
        if pre is None and x not in c:
            # Iterate over all possible pre's
            possi = self._possible_pres(x,c,d)
            for y in possi:
                # Fork up through the prefix tree
                tmp = self._valid_tops(a,a_bits,b,y,c+[x],d+[y],path+[x],result)
                # Update the provisional result
                # If this fork found no valid results, nothing happens
                # If this fork found only longer results, nothing happens
                if tmp[0] is not None: result = tmp;
        # If x has a pre, try forking thru the pre chain
        elif pre is not None:
            tmp = self._valid_tops(a,a_bits,b,pre,c,d,path+[x],result)
            # Update the provisional result
            # If this fork found no valid results, nothing happens
            # If this fork found only longer results, nothing happens
            if tmp[0] is not None: result = tmp;

        # Either way, fork up through the top as well
        tmp = self._valid_tops(a,a_bits,b,self.top(x),c,d,path,result)
        if tmp[0] is not None: result = tmp;

        # Return list of candidates
        return result

    def _checkLF(self,x,y=None):
        """Checks whether an LF transform can be applied on a node

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are satisfied,
        the function returns the two transform pivots, a and b
        as well as any cells it must add and their predecessors, c and d.
        """
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
            return (None,)*4

        # Main clause of the function
        a = self[x,y]
        # ∃ b = pre(a)
        b = self.pre(a)
        if not node._exists(b):
            return (None,)*4
        # ∄ top(a)
        top = self.top(a)
        if node._exists(top):
            return (None,)*4

        pre = self.top(b) if node._isbuf(b) else self.pre(b)

        c,d = self._valid_tops(a,(self.top(top),pre),b,self.top(top))

        if c is None:
            return (None,)*4

        return (a,b,c,d)

    def _checkFL(self,x,y=None):
        """Checks whether an FL transform can be applied on a node

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are satisfied,
        the function returns the two transform pivots, a and b
        as well as any cells it must add and their predecessors, c and d.
        """
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
               (top==pre and node._isbuf(x)):

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
           modules[bot.m]['type']=='post' or \
           node._isbuf(bot)):
            return (a,b)

        return (None,None)

    def _checkTF(self,x,y=None):
        """Checks whether a TF transform can be applied on a node

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are satisfied,
        the function returns the two transform pivots, a and b
        as well as any cells it must add and their predecessors, c and d.
        """
        if not isinstance(x,int) or (y is not None and not isinstance(y,int)):
            raise TypeError("x,y values provided to the internal-use-only check function are invalid!")

        # If no y is provided, check whole column from bottom up
        if y is None:
            for a in range(len(self.node_list)-1,-1,-1):
                a,b,c,d=self._checkTF(x,a)
                if b is not None:
                    return a,b,c,d
            return (None,None,None,None)

        # Main clause of the function
        a = self[x,y]

        pre = self.pre(a)
        if pre is None:
            return (None,None,None,None)

        b = None; c = None; d = None;
        top = self.top(a)
        # ∃ b s.t. b.x > pre(a).x
        poss_b = self._possible_pres(a)
        poss_b = [x for x in poss_b if x.x>pre.x]
        if any(node._exists(x) for x in poss_b):
            poss_b = [x for x in poss_b if node._exists(x)]
        for x in poss_b:
            # Figure out if a valid remapping exists
            c,d = self._valid_tops(a,(top,x),pre,top)
            if c is not None:
                # Ignore possibilities that are immediately redundant
                if not self._is_pg_subset((*c,*d),(x,)):
                    b=x; break;

        if b is None: return (None,None,None,None)

        return (a,b,c,d)

    def _checkFT(self,x,y=None):
        """Checks whether an FT transform can be applied on a node

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are satisfied,
        the function returns the two transform pivots, a and b
        as well as any cells it must add and their predecessors, c and d.
        """
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
        poss_b = list(reversed(self._possible_pres(a)))
        poss_b = [x for x in poss_b if x.x<pre.x]
        if any(node._exists(x) for x in poss_b):
            poss_b = [x for x in poss_b if node._exists(x)]
        for x in poss_b:
            # Figure out if a valid remapping exists
            c,d = self._valid_tops(a,(top,x),pre,top)
            if c is not None:
                # Ignore possibilities that are immediately redundant
                if not self._is_pg_subset((*c,*d),(x,)):
                    b=x; break;

        if b is None:
            return (None,None,None,None)

        return (a,b,c,d)

    def _checkLT(self,x,y=None):
        """Checks whether an LT transform can be applied on a node

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are satisfied,
        the function returns the two transform pivots, a and b
        as well as any cells it must add and their predecessors, c and d.
        """
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
        """Checks whether a TL transform can be applied on a node

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are satisfied,
        the function returns the two transform pivots, a and b
        as well as any cells it must add and their predecessors, c and d.
        """
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
        """Performs an LF transform on the specified node, if possible

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are not satisfied,
        the function returns (None,None).
        Otherwise, the function returns the co-ordinates of the main
        pivot of the transform.
        """
        a,b,c,d = self._checkLF(x,y)
        if b is None:
            return None

        self.dna+="_LF{0},{1}".format(a.x,a.y)

        # create c=top(top(a)); pre(c) = top(top(b))
        for x,y in zip(c,d):
            x=self[x.x,x.y]; y=self[y.x,y.y];
            x=self._morph_node(x,self.node_defs['black'])
            if not node._exists(y):
                y=self._morph_node(y,self.node_defs['buffer'])
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

        #self.hdl('hdl/'+self.dna+'.v')

        return a,b

    def FL(self,x,y=None,clean=True):
        """Performs an FL transform on the specified node, if possible

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are not satisfied,
        the function returns (None,None).
        Otherwise, the function returns the co-ordinates of the main
        pivot of the transform.
        """
        a,b = self._checkFL(x,y)
        if b is None:
            return None

        self.dna+="_FL{0},{1}".format(a.x,a.y)

        # pre(post(a)) = b
        # pre(top(post(a))) = top(a)
        post = self.post(a)
        for x in post:
            top = self.top(x)
            if not self._is_pg_subset((top,b),(top,a)):
                top = self._morph_node(top,self.node_defs['black'])
                self._add_pre(top,self.top(a))
                if not node._exists(self.top(a)):
                    self._morph_node(self.top(a),self.node_defs['buffer'])
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

        #self.hdl('hdl/'+self.dna+'.v')

        return a,b

    def TF(self,x,y=None,clean=True):
        """Performs a TF transform on the specified node, if possible

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are not satisfied,
        the function returns (None,None).
        Otherwise, the function returns the co-ordinates of the main
        pivot of the transform.
        """
        a,b,c,d = self._checkTF(x,y)
        if b is None:
            return None

        self.dna+="_TF{0},{1}".format(a.x,a.y)

        # Make sure b is at least a buffer
        if not node._exists(b):
            b=self._morph_node(b,self.node_defs['buffer'])

        pre = self.pre(a)

        # pre(a) = b, and any other additions necessary
        pre = self.remove_all_edges(pre,a)

        if not node._exists(b):
            b = self._morph_node(b,self.node_defs['buffer'])
        self._add_pre(a,b)
        self.walk_downstream(a,fun=self._recalc_pg)
        
        # any other additions necessary
        for x,y in zip(c,d):
            x=self[x.x,x.y]; y=self[y.x,y.y];
            x=self._morph_node(x,self.node_defs['black'])
            if not node._exists(y):
                y=self._morph_node(y,self.node_defs['buffer'])
            self._add_pre(x,y)
            self.walk_downstream(x,fun=self._recalc_pg)

        if clean:
            self.clean()

        #self.hdl('hdl/'+self.dna+'.v')

        return a,b

    def FT(self,x,y=None,clean=True):
        """Performs an FT transform on the specified node, if possible

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are not satisfied,
        the function returns (None,None).
        Otherwise, the function returns the co-ordinates of the main
        pivot of the transform.
        """
        a,b,c,d = self._checkFT(x,y)
        if b is None:
            return None

        self.dna+="_FT{0},{1}".format(a.x,a.y)

        pre = self.pre(a)

        # pre(a) = b, and any other additions necessary
        pre = self.remove_all_edges(pre,a)

        if not node._exists(b):
            b = self._morph_node(b,self.node_defs['buffer'])
        self._add_pre(a,b)
        self.walk_downstream(a,fun=self._recalc_pg)
        
        # any other additions necessary
        for x,y in zip(c,d):
            x=self[x.x,x.y]; y=self[y.x,y.y];
            x=self._morph_node(x,self.node_defs['black'])
            if not node._exists(y):
                y=self._morph_node(y,self.node_defs['buffer'])
            self._add_pre(x,y)
            self.walk_downstream(x,fun=self._recalc_pg)

        if clean:
            self.clean()

        #self.hdl('hdl/'+self.dna+'.v')

        return a,b,c,d

    def LT(self,x,y=None,clean=True):
        """Performs an LT transform on the specified node, if possible

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are not satisfied,
        the function returns (None,None).
        Otherwise, the function returns the co-ordinates of the main
        pivot of the transform.
        """
        a,b = self._checkLT(x,y=y)
        if b is None:
            return None

        a,b = self.LF(a.x,a.y,clean)
        return self.FT(a.x,a.y,clean)
        #LF, followed by FT

    def TL(self,x,y=None,clean=True):
        """Performs a TL transform on the specified node, if possible

        The node is specified using its (x,y) co-ordinate
        Withholding the y-coordinate will check the entire x-column
        from bottom-up.

        If the transform's initial requirements are not satisfied,
        the function returns (None,None).
        Otherwise, the function returns the co-ordinates of the main
        pivot of the transform.
        """
        a,b = self._checkTL(x,y)
        if b is None:
            return None

        a,b = self.TF(a.x,a.y,clean)
        return self.FL(a.x,a.y,clean)
        #TF, followed by FL

    def batch_transform(self,transform,x1,x2,step=1):
        """Performs a series of identical transforms as a batch"""
        for x in range(x1,x2,step):
            if not getattr(self,transform)(x):
                err="batch transform {0} failed on {1}".format(transform,x)
                raise ValueError(err)

    def harris_step(self,transform,steps=1,bot_bit=None,top_bit=None):
        """Performs a sequence of transforms that lead to a Harris step"""
        if top_bit==None: top_bit=self.w
        if bot_bit==None: bot_bit=0
        if steps==0: return
        # Harris space is different from transform space
        # Brent-Kung is the L corner of Harris space
        # Ripple-carry is our L corner
        # So if we're moving to/from L, we need to
        # modify our transform to move towards Brent-Kung
        if transform in ['LF','FL','LT','TL']:

            for i in range(1,len(self)-lg(self.w)+1-(transform[0]=='L')+1):
                top = top_bit-1
                bot = 2**i+2**(i-1)-1

                self.batch_transform(transform,bot,top,2**i)

        self.harris_step(transform,steps-1,bot_bit=bot_bit,top_bit=top_bit)

    def clean(self):
        """Compresses the graph and eliminates redundant nodes"""
        if self.is_idem:
            while self.reduce_idem() or self.compact(): pass
        else:
            while self.compact(): pass
        self.trim_layers()

    def compact(self):
        """Shifts up all nodes it can"""
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
            if not (pre is None or node._exists(pre)):
                a = self.shift_node(a)
            # or a buffer with no top
#            elif node._isbuf(pre) and not node._exists(self.top(pre)):
#                pre = self.shift_node(pre)
#                a = self.shift_node(a,new_pre=pre)
            else:
                continue
            changed=True; break;
        if changed:
            return 1+self.compact()
        else:
            return 0

    def reduce_idem(self):
        """Eliminates redundant nodes
        
        As of commit 194923b83, this relies on node group P/G
        """
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
                m = self.node_defs['buffer']
            self._morph_node(modified,m,True)
            return 1+self.reduce_idem()
        return 0

    def trim_layer(self):
        """Trims the last row of the tree if it is empty"""
        # Check if last row is just buffers
        if any([ \
               (node._exists(self.top(x)) and not node._isbuf(self.top(x))) \
               for x in self.node_list[-1] \
               ]): return False
        [self.shift_node(x) for x in self.node_list[-1]]
        [self.remove_node(x) for x in self.node_list[-1]]
        del self.node_list[-1]
        return True

    def trim_layers(self):
        """Repeatedly calls trim_layer until no more can be trimmed"""
        while(self.trim_layer()): pass

    def add_layer(self):
        """Adds an extra layer at the bottom of the tree"""
        y=len(self.node_list)
        for a in range(self.w):
            self.add_node(node(a,y,'invis_node'))
        for x in self.node_list[-2]:
            self.shift_node(x,self.bot)
        return True

    def check_tree(self):
        """Check if tree is valid"""
        # Re-calculate the tree
        pre_processing = self.node_list[0]
        for n in pre_processing:
            self.walk_downstream(n,fun=self._recalc_pg)

        # Check that tree remains valid
        post_processing = self.node_list[-1]
        for i in range(len(post_processing)):
            pg = post_processing[i].pg
            # Return True if all bits are high
            try:
                assert pg&(pg+1)==0
                assert modules[post_processing[i].m]['type']=='post'
            except AssertionError as e:
                print("\nTree check failed on bit {0}\n".format(i))
                raise e

    # TO-DO: Provide way to adjust the approximation based on tech node
    def recalc_weights(self):
        """Calculates the weights of all edges

        This returns a rough approximation of their delay.
        The calculation is performed using logical effort
        and approximated coupling capacitance.
        """
        for e in self.edges.data():
            p = modules[e[1].m]['pd']
            g = modules[e[1].m]['le']
            diag_le = modules[e[1].m].get('diag_le',None)
            if diag_le is not None and e[0].x!=e[1].x:
                g = diag_le
            fanout = len(self.post(e[1]))+1
            tracks = 1
            e[2]['weight'] = p + g*(fanout+tracks)

    def png(self,fname='out.png'):
        """Creates a PNG of the prefix tree"""

        # Helper function to format node name for pyDot
        def wrap(s):
            return('"'+str(s)+'"')

        # Helper function to convert between pos string and tuple
        def parse_pos(n,flag=True):
            if flag:
                return [float(x) for x in n[:-1].split(',')]
            else:
                return ','.join([str(x) for x in n])+'!'

        # Helper function to sort the nodes of a block in order
        def sort_block(l):
            return sorted(l,key=lambda x: (-x[1],-x[0]))

        # Helper function to add invis node next to node
        def add_invis(orig_pos,x_dir=1,y_dir=1):
            if not orig_pos[1].is_integer():
                y_space_ = y_space / 2
            else:
                y_space_ = y_space
            new_pos = [orig_pos[0]+x_space*x_dir,orig_pos[1]+y_space_*y_dir]
            new_pos = parse_pos(new_pos,False)
            new_n = pydot.Node(new_pos,style='invis',pos=new_pos,label="")
            if len(pg.get_node(wrap(new_pos)))==0: pg.add_node(new_n)
            return new_pos

        pg=nx.drawing.nx_pydot.to_pydot(self)
        pg.set_splines("false")
        pg.set_concentrate("true")

        # Make local copy of list of blocks
        blocks = []
        for x in self.blocks:
            if x is not None:
                blocks.append(x.copy())
            else:
                blocks.append(None)

        # Flag gets set if fan-out group has a block
        block_flags = set()

    # Make fan-out pretty:
    # Go through each node
    # Check for fan-out
    # Create invisible, png-only, nodes

        for row in self.node_list:
            for n in row:

                # Select nodes in the main part of the graph
                if n.x==0 or n.y in [0,len(self.node_list)-1] or not node._exists(n):
                    continue

                # Get pre
                pre = self.pre(n)
                # Get all nodes to the right that are attached to the same pre
                rights = iter([x for x in row if self.pre(x)==pre and x.x<n.x and \
                               (node._exists(x) and not node._isbuf(x))])
                # Get the 1st node to the right
                r1 = next(rights,None)

                # If this node shares a pre with at least one other node
                if pre is not None and r1 is not None:

                    # Make a new, invis, node next to this node
                    pos_n="{0},{1}!".format(-1*(n.x-0.5),-1*(n.y-0.5))
                    py_n1=pydot.Node(pos_n,style='invis',pos=pos_n,label="")
                    if len(pg.get_node(wrap(pos_n)))==0:
                        pg.add_node(py_n1)
                        # If this node and the pre are part of the same block
                        # This invis node also needs to join the block
                        if pre.block is not None and pre.block==n.block:
                            blocks[n.block].add(pos_n)
                            block_flags.add(pre)

                    # Make a new, invis, node next to the 1st right
                    pos_r1="{0},{1}!".format(-1*(r1.x-0.5),-1*(r1.y-0.5))
                    py_n2=pydot.Node(pos_r1,style='invis',pos=pos_r1,label="")
                    if len(pg.get_node(wrap(pos_r1)))==0:
                        pg.add_node(py_n2)
                        # If this node and the pre are part of the same block
                        # This invis node also needs to join the block
                        if pre.block is not None and pre.block==r1.block:
                            blocks[r1.block].add(pos_r1)
                            block_flags.add(pre)

                    # If there are no more rights
                    if next(rights,None) is None:
                        # Add edge from pre to this fan-out group
                        tail = 's' if node._isbuf(pre) else 'sw'
                        pg.add_edge(pydot.Edge(str(pre),pos_r1,
                            headclip="false",arrowhead="none",
                            tailport=tail))
                        pg.add_edge(pydot.Edge(pos_r1,str(r1),
                            headclip="false",tailclip="false",arrowhead="none",
                            headport='ne'))

                    # Add edge from 1st right to this node
                    pg.add_edge(pydot.Edge(pos_r1,pos_n,
                        headclip="false",tailclip="false",arrowhead="none"))
                    pg.add_edge(pydot.Edge(pos_n,str(n),
                        headclip="false",tailclip="false",arrowhead="none",
                        headport='ne'))
                    # Add parent invis node to block if needed
                    if pre in block_flags:
                        blocks[pre.block].add(pos_r1)

                    # Delete edge from pre to this node
                    # Delete edge from pre to the 1st right
                    pg.del_edge(wrap(pre),wrap(n))
                    pg.del_edge(wrap(pre),wrap(r1))

# Clusters don't draw boundaries well
#        for b in self.blocks:
#            if b is None: continue
#            sg = pydot.Cluster(str(b),shape="oval",fillcolor="gray90",style='dashed')
#            for n in b:
#                sg.add_node(pg.get_node(wrap(n))[0])
#            pg.add_subgraph(sg)
        block_colors = cycle(['seagreen2','red','darkorchid1','blue'])
        for block in blocks:
            color = next(block_colors)
            if block is None: continue
#            if len(block)<2: continue
            # Define how far out the outlines sit
            x_space = 0.3
            y_space = 0.3
            # Get list of nodes in block and sort it
            orig_list=[]
            for n in block:
                # Get position of nodes
                orig_list.append(parse_pos(pg.get_node(wrap(n))[0].get('pos')))
            orig_list = sort_block(orig_list)
            # Make list of invisible side nodes
            left_list = []
            right_list = []
            for i,orig_pos in enumerate(orig_list):
                if i==0:
                    new_n = add_invis(orig_pos,1,1)
                    right_list.append(new_n)
                new_n = add_invis(orig_pos,-1,1)
                left_list.append(new_n)
                new_n = add_invis(orig_pos,1,-1)
                right_list.append(new_n)
                if i==len(orig_list)-1:
                    new_n = add_invis(orig_pos,-1,-1)
                    left_list.append(new_n)
            # Add edges
            for i,x in enumerate(left_list):
                if i==0: continue
                pg.add_edge(pydot.Edge(left_list[i-1],x,
                                       arrowhead="none",style="dashed",color=color,penwidth="3",
                                       headclip="false",tailclip="false"))
            for i,x in enumerate(right_list):
                if i==0: continue
                pg.add_edge(pydot.Edge(right_list[i-1],x,
                                       arrowhead="none",style="dashed",color=color,penwidth="3",
                                       headclip="false",tailclip="false"))
            pg.add_edge(pydot.Edge(left_list[0],right_list[0],
                                   arrowhead="none",style="dashed",color=color,penwidth="3",
                                   headclip="false",tailclip="false"))
            pg.add_edge(pydot.Edge(left_list[-1],right_list[-1],
                                   arrowhead="none",style="dashed",color=color,penwidth="3",
                                   headclip="false",tailclip="false"))
        pg.write_png(fname,prog='neato')
#        webbrowser.open_new(fname)

if __name__=="__main__":
    raise RuntimeError("This file is importable, but not executable")
