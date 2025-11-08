class FD:
    def __init__(self, lhs: set[str], rhs: set[str]):
        self.lhs = frozenset(lhs)
        self.rhs = frozenset(rhs)
    
    def __hash__(self):
        return hash((self.lhs, self.rhs))
    
    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs
    
    def __repr__(self):
        return f"{set(self.lhs)} -> {set(self.rhs)}"
    
    def printFD(self):
        print(f"{set(self.lhs)} -> {set(self.rhs)}")


# --- Inference Rules ---

def reflexivity(fd: FD) -> set[FD]:
    """If Y ⊆ X, then X → Y"""
    result = set()
    for attr in fd.lhs:
        result.add(FD(fd.lhs, {attr}))  # trivial FD: X → a
    return result


def augmentation(fd: FD, all_attrs: set[str]) -> set[FD]:
    """If X → Y, then XZ → YZ for any Z"""
    result = set()
    for z in all_attrs:
        if z not in fd.lhs and z not in fd.rhs:
            lhs_aug = set(fd.lhs) | {z}
            rhs_aug = set(fd.rhs) | {z}
            result.add(FD(lhs_aug, rhs_aug))
    return result


def transitivity(fd1: FD, fd2: FD) -> set[FD]:
    """If X → Y and Y → Z, then X → Z"""
    result = set()
    if not fd1.rhs.isdisjoint(fd2.lhs):  # RHS(f1) ∩ LHS(f2) ≠ ∅
        result.add(FD(fd1.lhs, fd2.rhs))
    return result
