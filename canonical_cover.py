from functional_dependency import FD
from extraneous_attribute import is_extraneous_in_lhs, is_extraneous_in_rhs

def canonical_cover(F: set[FD]) -> set[FD]:
    Fc = F.copy()

    while True:
        changed = False

        # --- Step 1: Apply Union Rule ---
        # For α → β1 and α → β2, combine into α → β1 ∪ β2
        unioned = set()
        grouped = {}

        # Group FDs by their LHS
        for fd in Fc:
            grouped.setdefault(fd.lhs, set()).update(fd.rhs)

        # Recreate the set of dependencies with combined RHS
        for lhs, rhs in grouped.items():
            unioned.add(FD(lhs, rhs))

        if len(unioned) != len(Fc):
            changed = True
        Fc = unioned

        # --- Step 2: Check for Extraneous Attributes ---
        new_Fc = set()

        for fd in Fc:
            lhs = set(fd.lhs)
            rhs = set(fd.rhs)
            modified = False

            # Check for extraneous attributes in LHS
            for attr in list(lhs):
                if is_extraneous_in_lhs(Fc, fd, attr):
                    lhs.remove(attr)
                    changed = True
                    modified = True

            # Check for extraneous attributes in RHS
            for attr in list(rhs):
                if is_extraneous_in_rhs(Fc, fd, attr):
                    rhs.remove(attr)
                    changed = True
                    modified = True

            # Add updated FD
            new_Fc.add(FD(lhs, rhs) if modified else fd)

        Fc = new_Fc

        if not changed:
            break

    return Fc


if __name__ == "__main__":
    # Example from textbook-style canonical cover problem
    F = {
        FD({'A'}, {'B'}),
        FD({'A'}, {'C'}),
        FD({'C', 'G'}, {'H'}),
        FD({'C', 'G'}, {'I'}),
        FD({'B'}, {'H'})
    }

    Fc = canonical_cover(F)
    print("Canonical Cover (Fc):")
    for fd in Fc:
        print(fd)
