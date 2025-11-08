from functional_dependency import FD, reflexivity, augmentation, transitivity

def closure_of_FDs(F: set[FD]) -> set[FD]:
    F_plus = F.copy()

    while True:
        new_FDs = set()

        # Collect all attributes from F+
        all_attrs = set().union(*(f.lhs | f.rhs for f in F_plus))

        # Apply Reflexivity & Augmentation
        for fd in F_plus:
            new_FDs |= reflexivity(fd)
            new_FDs |= augmentation(fd, all_attrs)

        # Apply Transitivity
        for f1 in F_plus:
            for f2 in F_plus:
                new_FDs |= transitivity(f1, f2)

        # Merge and check if closure changed
        before = len(F_plus)
        F_plus |= new_FDs
        after = len(F_plus)

        if before == after:  # no new FDs → stable
            break

    return F_plus


if __name__ == "__main__":
    f = {
        FD({'A'}, {'B'}),
        FD({'A'}, {'C'}),
        FD({'C', 'G'}, {'H'}),
        FD({'C', 'G'}, {'I'}),
        FD({'B'}, {'H'})
    }

    F_plus = closure_of_FDs(f)
    print("Closure of F (F+):")
    for fd in F_plus:
        print(fd)
