from functional_dependency import FD
from closure_of_attribute import aPlus

def is_extraneous_in_lhs(F: set[FD], fd: FD, A: str) -> bool:
    """
    Checks if attribute A is extraneous in the LHS of fd (α → β).
    """
    if A not in fd.lhs:
        return False

    gamma = set(fd.lhs) - {A}  # α - {A}
    gamma_plus = aPlus(F, gamma)

    # If (α - {A})+ includes all of β, then A is extraneous in α
    return fd.rhs.issubset(gamma_plus)


def is_extraneous_in_rhs(F: set[FD], fd: FD, A: str) -> bool:
    """
    Checks if attribute A is extraneous in the RHS of fd (α → β).
    """
    if A not in fd.rhs:
        return False

    # Create F' = (F - {α → β}) ∪ {α → (β - {A})}
    F_prime = F.copy()
    F_prime.discard(fd)
    F_prime.add(FD(fd.lhs, set(fd.rhs) - {A}))

    alpha_plus = aPlus(F_prime, set(fd.lhs))

    # If α+ includes A, then A is extraneous in β
    return A in alpha_plus


if __name__ == "__main__":
    # Example
    F = {
        FD({'A', 'B'}, {'C'}),
        FD({'A'}, {'B'}),
        FD({'B'}, {'D'})
    }

    fd = FD({'A', 'B'}, {'C'})
    print(f"Checking extraneous attributes in: {fd}\n")

    for attr in fd.lhs:
        if is_extraneous_in_lhs(F, fd, attr):
            print(f"→ {attr} is extraneous in LHS")
        else:
            print(f"→ {attr} is NOT extraneous in LHS")

    for attr in fd.rhs:
        if is_extraneous_in_rhs(F, fd, attr):
            print(f"→ {attr} is extraneous in RHS")
        else:
            print(f"→ {attr} is NOT extraneous in RHS")
