from .ExpressionNode import ExpressionNode


class EquivClass:
    """Defines an equivalence class of ExpressionNodes

    This represents nodes that are mathematically distinct,
    but physically equivalent.

    Attributes:
        nodes (set of ExpressionNode): The nodes in this equivalence class
        rep (ExpressionNode): The representative of this equivalence class
        parents (set of EquivClass): The parents of this equivalence class
        wires (set of strings): The set of wires that are output by the
            representative node of this equivalence class
    """

    def __init__(self, rep):
        """Initializes an EquivClass object

        Args:
            rep (ExpressionNode): The representative of this equivalence class
            nodes (list of ExpressionNode): The nodes in this equivalence class
        """
        if not isinstance(rep, ExpressionNode):
            raise TypeError("rep must be an ExpressionNode")

        self.rep = rep
        self.nodes = {rep}
        self.wires = {wire for net in rep.out_nets.values() for wire in net}
        self.parents = {rep.parent}

    def __len__(self):
        """Returns the number of nodes in this equivalence class"""
        return len(self.nodes)

    def __iter__(self):
        """Iterates over the nodes in this equivalence class"""
        return iter(self.nodes)

    def __eq__(self, other):
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
        if self.value != other.value:
            return False

        # Check whether their subtrees are also equivalent
        for a in range(len(self.rep.children)):
            this_c = self.rep[a]
            if this_c is not None:
                try:
                    other_c = other_rep[a]
                except IndexError:
                    return False
                if not this_c.equiv_class.is_equiv(other_c.equiv_class):
                    return False

        return True

    def merge(self, other):
        """Merges this equivalence class with another equivalence class

        Args:
            other (EquivClass): The equivalence class to merge with
        """
        if not isinstance(other, EquivClass):
            raise TypeError("other must be an EquivClass")
        if not self == other:
            raise ValueError("Cannot merge non-equivalent equivalence classes")

        # Merge the equivalence classes
        self.nodes |= other.nodes
        self.parents |= other.parents

        # Assign the correct equivalence class to all nodes
        for node in other.nodes:
            node.equiv_class = self

        return self

    def is_bifurcation(self):
        """Returns whether this equivalence class bifurcates

        That is to say, this answers ∃n ≡ self s.t n.parent !≡ self.parent
        """
        return len(self.parents) > 1


if __name__ == "__main__":
    raise RuntimeError("This module is not intended to be run directly")
