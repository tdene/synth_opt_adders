from .util import change_in_nets


class EquivClass:
    """Defines an equivalence class of ExpressionNodes

    This represents nodes that are mathematically distinct,
    but physically equivalent.

    Attributes:
        nodes (set of ExpressionNode): The nodes in this equivalence class
        rep (ExpressionNode): The representative of this equivalence class
        out_nets (dict): The output nets of this equivalence class
        parents (set of EquivClass): The parents of this equivalence class
    """

    def __init__(self, rep):
        """Initializes an EquivClass object

        Args:
            rep (ExpressionNode): The representative of this equivalence class
            nodes (list of ExpressionNode): The nodes in this equivalence class
        """
        self.rep = rep
        self.nodes = {rep}
        self.out_nets = rep.out_nets
        self.parents = set()

    def __len__(self):
        """Returns the number of nodes in this equivalence class"""
        return len(self.nodes)

    def __iter__(self):
        """Iterates over the nodes in this equivalence class"""
        return iter(self.nodes)

    def equiv(self, other):
        """Returns whether this equivalence class is equivalent to another

        Args:
            other (EquivClass): The equivalence class to compare to
        """
        if not isinstance(other, EquivClass):
            raise TypeError("other must be an EquivClass")

        other_rep = other.rep
        # Check whether the two representatives are equivalent
        if self.rep > other.rep or self.rep < other.rep:
            return False
        if self.rep.value != other.rep.value:
            return False

        # Check whether their subtrees are also equivalent
        for a in range(len(self.rep.children)):
            this_c = self.rep[a]
            if this_c is not None:
                try:
                    other_c = other_rep[a]
                except IndexError:
                    return False
                if not this_c.equiv_class == other_c.equiv_class:
                    return False

        return True

    def __str__(self):
        """Returns a string representation of this equivalence class"""
        return "ec({}@{})#{}".format(self.rep, self.rep.graph, len(self))

    def __repr__(self):
        return str(self)

    def _recalculate_parents(self):
        """Recalculates the parents of this equivalence class"""
        self.parents = set()
        for node in self:
            parent = node.parent
            if parent is None:
                self.parents.add(None)
            else:
                self.parents.add(parent.equiv_class.rep)
        return

    def change_rep(self, new_rep):
        """Changes the representative of this equivalence class"""
        if new_rep not in self.nodes:
            raise ValueError("new_rep must be in this equivalence class")

        for node in self:
            parent = node.parent
            index = parent.children.index(node)
            change_in_nets(parent, self.out_nets, new_rep.out_nets, index)
        self.rep = new_rep
        self.out_nets = new_rep.out_nets
        return

    def merge(self, other, check_equiv=True):
        """Merges this equivalence class with another equivalence class

        Args:
            other (EquivClass): The equivalence class to merge with
        """
        if not isinstance(other, EquivClass):
            raise TypeError("other must be an EquivClass")
        if check_equiv and not self.equiv(other):
            raise ValueError("Cannot merge non-equivalent equivalence classes")

        # Merge the equivalence classes
        self.nodes |= other.nodes
        self.parents |= other.parents

        # Merge the out_nets
        for k, v in self.out_nets.items():
            if v is [None]:
                self.out_nets[k] = other.out_nets[k]

        # Assign the correct equivalence class to new nodes
        # Overwrite input nets of new nodes
        for node in other.nodes:
            node.equiv_class = self
            parent = node.parent
            index = parent.children.index(node)
            change_in_nets(parent, node.out_nets, self.rep.out_nets, index)

        return self

    def is_bifurcation(self):
        """Returns whether this equivalence class bifurcates

        That is to say, this answers ∃n ≡ self s.t n.parent !≡ self.parent
        """
        return len(self.parents) > 1

    def reset(self):
        """Resets the equivalence classes of all nodes in this class"""
        for node in self:
            node.equiv_class = EquivClass(node)
            parent = node.parent
            index = parent.children.index(node)
            change_in_nets(parent, self.rep.out_nets, node.out_nets, index)
        return


if __name__ == "__main__":
    raise RuntimeError("This module is not intended to be run directly")
